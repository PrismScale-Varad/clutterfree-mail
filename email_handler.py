from db import save_emails_to_db
import imaplib
import email
from email.header import decode_header
import os
import json


def load_config(config_path="config.json"):
    """ Load email configuration from a JSON file. """
    # Get the current working directory (the directory the script is run from)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to the config file
    config_file_path = os.path.join(current_directory, config_path)
    
    # Load the config file
    try:
        with open(config_file_path, "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: {config_file_path} not found!")
        return None


def connect_to_email(config):
    """ Connect to the IMAP email server using the provided credentials. """
    # Set up the connection to the IMAP server
    mail = imaplib.IMAP4_SSL(config['email']['imap_server'])
    mail.login(config['email']['email_address'], config['email']['password'])
    return mail

def fetch_unread_emails(mail):
    """ Fetch unread emails from the inbox. """
    # Select the mailbox you want to check (in this case, 'inbox')
    mail.select("inbox")
    
    # Search for all unread emails
    status, messages = mail.search(None, 'UNSEEN')
    
    if status != "OK":
        print("No unread emails found!")
        return []

    # Split the email IDs into a list
    email_ids = messages[0].split()
    emails = []

    # Fetch each email by ID
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        
        if status != "OK":
            print(f"Failed to fetch email ID {email_id}")
            continue
        
        # Parse the email content
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                # Decode the sender's email address
                sender, encoding = decode_header(msg.get("From"))[0]
                if isinstance(sender, bytes):
                    sender = sender.decode(encoding if encoding else "utf-8")
                
                # Save the email data
                email_data = {
                    "subject": subject,
                    "sender": sender,
                    "date": msg["Date"]
                }
                
                # Add email to the list
                emails.append(email_data)
    save_emails_to_db(emails)

    return emails

def main():
    # Load the email config
    config = load_config()

    # Connect to the email account
    mail = connect_to_email(config)
    
    # Fetch unread emails
    unread_emails = fetch_unread_emails(mail)
    
    if unread_emails:
        print(f"Found {len(unread_emails)} unread emails:")
        for email_data in unread_emails:
            print(f"Subject: {email_data['subject']}, From: {email_data['sender']}, Date: {email_data['date']}")
    else:
        print("No unread emails found.")

if __name__ == "__main__":
    main()
