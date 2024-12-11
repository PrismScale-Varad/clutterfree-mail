from db import save_emails_to_db
import imaplib
import email
from email.header import decode_header
import os
import re
import json
from bs4 import BeautifulSoup

def load_config(config_path="config.json"):
    """ Load email configuration from a JSON file. """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    config_file_path = os.path.join(current_directory, config_path)
    
    try:
        with open(config_file_path, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: {config_file_path} not found!")
        return None


def connect_to_email(config):
    """ Connect to the IMAP email server using the provided credentials. """
    mail = imaplib.IMAP4_SSL(config['email']['imap_server'])
    mail.login(config['email']['email_address'], config['email']['password'])
    return mail

def fetch_unread_emails(mail):
    """ Fetch unread emails from the inbox. """
    mail.select("inbox")
    
    status, messages = mail.search(None, 'UNSEEN')
    
    if status != "OK":
        print("No unread emails found!")
        return []

    email_ids = messages[0].split()
    emails = []

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        
        if status != "OK":
            print(f"Failed to fetch email ID {email_id}")
            continue
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                sender, encoding = decode_header(msg.get("From"))[0]
                if isinstance(sender, bytes):
                    sender = sender.decode(encoding if encoding else "utf-8")
                
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if "attachment" not in content_disposition:
                            if content_type == "text/plain":
                                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                break
                            elif content_type == "text/html":
                                html_content = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                soup = BeautifulSoup(html_content, "html.parser")
                                body = soup.get_text(strip=True)  # Extract plaintext from HTML
                                break
                else:
                    payload = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                    if msg.get_content_type() == "text/html":
                        soup = BeautifulSoup(payload, "html.parser")
                        for element in soup(["script", "style", "span", "div"]):  # Exclude common tags for styling and scripts
                            element.decompose()
                        body = soup.get_text(separator="\n", strip=True)
                        body = re.sub(r'\\[^\s]*', '', body)
                        body = re.sub(r'\s+', ' ', body).strip()


                    else:
                        body = payload

                email_data = {
                    "subject": subject,
                    "sender": sender,
                    "body": body,
                    "date": msg["Date"]
                }
                
                emails.append(email_data)
    save_emails_to_db(emails)

    return emails

def main():
    config = load_config()

    mail = connect_to_email(config)
    
    unread_emails = fetch_unread_emails(mail)
    
    if unread_emails:
        print(f"Found {len(unread_emails)} unread emails:")
        for email_data in unread_emails:
            print(f"Subject: {email_data['subject']}, From: {email_data['sender']}, Date: {email_data['date']}")
    else:
        print("No unread emails found.")

if __name__ == "__main__":
    main()
