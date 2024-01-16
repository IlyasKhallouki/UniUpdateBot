import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("EMAIL_PASSWORD")

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

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('umiestsender@gmail.com', password)
        server.send_message(msg)

async def main(title, body, attachement_names):
    email_addresses = ['ilyaskhallouki1337@gmail.com', 'khallouki1337@gmail.com']

    tasks = [send_email(email, title, body, attachement_names) for email in email_addresses]

    await asyncio.gather(*tasks)

def send(title, body, names):
    asyncio.run(main(title, body, names))
