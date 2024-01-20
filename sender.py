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
email_address= os.getenv("EMAIL_ADDRESS")

excel_file_path = './emails.xlsx'

def excel_to_dict(file_path):
    df = pd.read_excel(file_path)

    excel_dict = {}

    headers = df.columns.tolist()

    for header in headers:
        excel_dict[header] = df[header].tolist()

    excel_dict["ALL"] = df.values.flatten().tolist()

    return excel_dict


async def send_email(email, title, body, attachment_paths):
    msg = MIMEMultipart()
    msg['From'] = email_address 
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

async def main(title, body, attachment_names, targets):
    email_addresses_dict = excel_to_dict(excel_file_path)
    email_addresses = []

    for target in targets:
        for email in email_addresses_dict[target]:
            email_addresses.append(email)

    tasks = [send_email(email, title, body, attachment_names) for email in email_addresses]

    await asyncio.gather(*tasks)

def send(title, body, names):
    asyncio.run(main(title, body, names))
