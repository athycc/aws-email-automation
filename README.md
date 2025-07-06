# aws-email-automation



Automated email sender for AWS Learning Club Alpha with HTML templates and image support.

## 📂 Project Structure

aws-email-automation/
├── email_sender.py
├── contacts.csv
├── .env.example
├── requirements.txt
├── template/
│ ├── congratulatory.html
│ ├── rejection.html
│ ├── partnership.html
│ ├── sponsorship.html
│ └── speakers.html
└── email-assets/
├── banner.png
└── Footer.png


## 🚀 Setup Guide

### 1. Clone the Repo

git clone https://github.com/athycc/aws-email-automation.git
cd aws-email-automation

2.Install Requirements

pip install -r requirements.txt

3. Configure .env
Copy .env.example → .env and fill it:

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
Use an App Password if using Gmail with 2FA.

4. Add Contacts
Edit contacts.csv:

email
applicant@example.com

5. Choose Template & Send
Edit email_sender.py:


template_name = 'congratulatory.html'
subject = '🎉 Congratulations & Welcome to AWS Learning Club Alpha!'

Then run:


python email_sender.py
📩 Available Templates
congratulatory.html

rejection.html

partnership.html

sponsorship.html

speakers.html

Each uses GitHub-hosted images:

banner.png → top header

Footer.png → footer/logo

📌 License
This project is open source and built with 💚 for AWS Learning Club Alpha.