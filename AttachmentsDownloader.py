import requests
from re import sub
import os

def download_attachment(attachment_links):
    for link in attachment_links:
        filename = os.path.join(os.getcwd(), 'Attachments', sub(r'[^\w.-]', '_', link.split('/')[-1]))
        if os.path.exists(filename):
                print(f"File {filename} already exists. Skipping download.")
                continue
        req = requests.get(link)
        if req.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    f.write(chunk)