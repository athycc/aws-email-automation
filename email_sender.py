import os
import smtplib
import csv
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
        print(f"✅ Sent to: {recipient_email}")

# Main logic
def send_bulk_emails(csv_path, template_name, subject):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipient = row['email']
            send_email(subject, recipient, f'template/{template_name}')

# Example usage
if __name__ == '__main__':
    # Customize these
    csv_path = 'contacts.csv'
    template_name = 'congratulatory.html'  # change this to the desired template
    subject = '🎉 Congratulations & Welcome to AWS Learning Club Alpha!'
    
    send_bulk_emails(csv_path, template_name, subject)
