from tinydb import TinyDB, Query
import os

# Initialize TinyDB (data.json is the database file)
db_path = "data.json"
db = TinyDB(db_path)

def save_emails_to_db(emails):
    """ Save list of emails to the TinyDB database. """
    if not emails:
        print("No emails to save!")
        return

    # Access the 'emails' table (TinyDB automatically creates this table)
    emails_table = db.table('emails')

    # Add each email to the database
    for email_data in emails:
        emails_table.insert(email_data)

    print(f"Saved {len(emails)} emails to {db_path}")

def fetch_all_emails_from_db():
    """ Fetch all saved emails from the database. """
    emails_table = db.table('emails')
    return emails_table.all()

def search_email_by_subject(subject):
    """ Search for emails by subject in the database. """
    emails_table = db.table('emails')
    Email = Query()
    return emails_table.search(Email.subject == subject)

# Example usage:
# save_emails_to_db(emails)
