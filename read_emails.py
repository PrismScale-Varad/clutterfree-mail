from email_handler import load_config, connect_to_email, fetch_unread_emails
from db import fetch_all_emails_from_db, save_emails_to_db, update_email_summary_in_db
from process_articles import summarize

def main():
    # Load the configuration from the JSON file
    config = load_config()

    if not config:
        print("Error loading config. Exiting...")
        return

    # Connect to the email server
    mail = connect_to_email(config)

    # Fetch unread emails
    unread_emails = fetch_unread_emails(mail)

    if unread_emails:
        print(f"Found {len(unread_emails)} unread emails. Saving to database...")
        # Save the emails to the database
        save_emails_to_db(unread_emails)
    else:
        print("No unread emails found.")

    # Summarize and update emails in the database
    all_emails = fetch_all_emails_from_db()

    if not all_emails:
        print("No emails found in the database to summarize!")
        return

    # Filter emails without a summary
    emails_without_summary = [email for email in all_emails if not email.get('summary')]

    if not emails_without_summary:
        print("All emails already have summaries.")
        return

    for email in emails_without_summary:
        if 'body' in email and email['body']:
            summary = summarize(email['body'])
            update_email_summary_in_db(email.doc_id, summary)

    print(f"Summarized and updated {len(emails_without_summary)} emails in the database.")


if __name__ == "__main__":
    main()
