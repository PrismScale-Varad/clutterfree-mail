from tinydb import TinyDB, Query
from datetime import datetime, timedelta

# Initialize TinyDB (data.json is the database file)
db_path = "data.json"
db = TinyDB(db_path)

def save_email_to_db(email_data, table_name="emails"):
    """ Save a single email to the TinyDB database. """
    emails_table = db.table(table_name)
    emails_table.insert(email_data)
    print(f"Saved email: {email_data.get('subject', 'No Subject')}")

def save_emails_to_db(emails):
    """ Save list of emails to the TinyDB database. """
    if not emails:
        print("No emails to save!")
        return

    for email_data in emails:
        save_email_to_db(email_data)

    print(f"Saved {len(emails)} emails to {db_path}")

def fetch_all_emails_from_db(table_name="emails"):
    """ Fetch all emails from the TinyDB database. """
    emails_table = db.table(table_name)
    return emails_table.all()

def update_email_summary_in_db(email_id, summary, table_name="emails"):
    """ Update the summary of a specific email in the database. """
    emails_table = db.table(table_name)
    emails_table.update({'summary': summary}, doc_ids=[email_id])
    print(f"Updated summary for email ID {email_id}")

def fetch_emails_from_last_7_days(table_name="emails"):
    """ Fetch emails from the last 7 days. """
    emails_table = db.table(table_name)
    seven_days_ago = datetime.now() - timedelta(days=7)
    # Filter emails by date (assuming 'date' is stored in a datetime-compatible format)
    emails = emails_table.search(Query().date > seven_days_ago.strftime('%Y-%m-%d'))
    return emails
