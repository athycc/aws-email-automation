import os
import smtplib
import csv
import time
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Email sending function
def send_email(subject, recipient_email, template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Setup the MIME
    message = MIMEMultipart("alternative")
    message['From'] = EMAIL_ADDRESS
    message['To'] = recipient_email
    message['Subject'] = subject

    # Attach HTML content
    message.attach(MIMEText(html_content, 'html'))

    # Send Email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(message)
        print(f"[OK] Sent to: {recipient_email}")

# Main logic
def send_bulk_emails(csv_path, template_name, subject):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipient = row['email']
            send_email(subject, recipient, f'template/{template_name}')


# Read emails from TXT file
def read_emails_from_txt(txt_path):
    """Read email addresses from a plain text file (one email per line)."""
    emails = []
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            email = line.strip()
            if email and email_pattern.match(email):
                emails.append(email)
            elif email:
                print(f"[!] Skipping invalid email: {email}")

    return emails


# Send bulk emails from TXT file with rate limiting
def send_bulk_emails_from_txt(txt_path, template_name, subject, delay=1.5):
    """Send bulk emails to addresses listed in a TXT file."""
    emails = read_emails_from_txt(txt_path)

    if not emails:
        print("[X] No valid emails found in the file.")
        return

    total = len(emails)
    sent = 0
    failed = 0

    print(f"\n{'='*50}")
    print(f"Starting bulk email send...")
    print(f"Template: {template_name}")
    print(f"Recipients: {total}")
    print(f"{'='*50}\n")

    for i, recipient in enumerate(emails, 1):
        try:
            print(f"[{i}/{total}] Sending to {recipient}...", end=" ")
            send_email(subject, recipient, f'template/{template_name}')
            sent += 1

            # Rate limiting - wait between emails (except for last one)
            if i < total:
                time.sleep(delay)

        except Exception as e:
            print(f"[X] Failed: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Summary: {sent} sent, {failed} failed")
    print(f"{'='*50}\n")

# Example usage
if __name__ == '__main__':
    # ===== INTERNSHIP INQUIRY EMAILS =====
    # Using TXT file for email list
    txt_path = 'emails.txt'
    template_name = 'internship-inquiry.html'
    subject = 'Inquiry on Internship Opportunities – AWS Learning Club Alpha'

    send_bulk_emails_from_txt(txt_path, template_name, subject)

    # ===== ALTERNATIVE: CSV-based sending =====
    # csv_path = 'contacts.csv'
    # template_name = 'congratulatory.html'
    # subject = '🎉 Congratulations & Welcome to AWS Learning Club Alpha!'
    # send_bulk_emails(csv_path, template_name, subject)
