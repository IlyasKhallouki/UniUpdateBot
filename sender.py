import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os
import aiosmtplib
import pandas as pd

load_dotenv()
password = os.getenv("EMAIL_PASSWORD")

excel_file_path = './emails.xlsx'

def extract_emails_from_excel(file_path):
    try:
        df = pd.read_excel(file_path, header=0, names=['Emails'], usecols=[0])
        unique_emails = df['Emails'].unique()

        return unique_emails

    except Exception as e:
        print(f"An error occurred: {e}")


async def send_email(email, title, body, attachment_paths):
    msg = MIMEMultipart()
    msg['From'] = 'umiestsender@gmail.com'  
    msg['To'] = email
    msg['Subject'] = title
    msg.attach(MIMEText(body, 'plain'))

    for file in attachment_paths:
        with open(file, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name=file)
            part['Content-Disposition'] = f'attachment; filename={file}'
        msg.attach(part)

    try:
        smtp = aiosmtplib.SMTP(hostname='smtp.gmail.com', port=587, start_tls=True)
        await smtp.connect()
        await smtp.login('umiestsender@gmail.com', password)
        await smtp.send_message(msg)
        await smtp.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

async def main(title, body, attachment_names):
    email_addresses = extract_emails_from_excel(excel_file_path)
    
    tasks = [send_email(email, title, body, attachment_names) for email in email_addresses]

    await asyncio.gather(*tasks)

def send(title, body, names):
    asyncio.run(main(title, body, names))