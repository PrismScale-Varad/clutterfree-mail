from email_handler import load_config, send_summary_email, fetch_email_summaries_from_last_7_days

def get_email_summaries_and_send():
    # Load the configuration from the JSON file
    config = load_config()

    if not config:
        print("Error loading config. Exiting...")
        return

    # Fetch email summaries from the last 7 days
    summaries = fetch_email_summaries_from_last_7_days(config)

    if summaries:
        # Send the summary email
        send_summary_email(config, summaries)
    else:
        print("No summaries to send.")

if __name__ == "__main__":
    get_email_summaries_and_send()
