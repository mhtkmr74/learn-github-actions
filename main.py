from email_handler.fetch_email import fetch_email_from_gmail
from email_handler.email_processor import get_emails

def main():
    fetch_email_from_gmail()
    get_emails()

if __name__ == "__main__":
    main()