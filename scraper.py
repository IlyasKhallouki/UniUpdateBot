import requests
from bs4 import BeautifulSoup
import re
import csv
import os
from AttachmentsDownloader import download_attachment
from MailGenerator import generate_email
from sender import send

file_path = 'Date Tracker.csv'

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            return row
        
def write_csv_date(file_path, new_date):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_date])

def check_date(date1, date2):
    if date1[0]>date2[0] or (date1[0]==date2[0] and date1[1]>date2[1]) or (date1[0]==date2[0] and date1[1]==date2[1] and date1[2]>date2[2]): return True
    else: return False

def check_tags(content):
    to_send = False
    targets = []

    if "#SEND#" in content: to_send = True

    match = re.search(r'#TO:\s*([A-Z,\s]+)#', content)

    if match:
        targets = [target.strip() for target in match.group(1).split(',')]

    return to_send, targets

def scrape_uni_website(old_date:list[str]):
    global content, attachments
    base_url = 'https://www.est-umi.ac.ma/'
    url = base_url + 'actualite.php'
    response = requests.get(url)


    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('h5', class_='event-title')


        for article in articles:
            date_str = article.find_previous('span', class_='event-place').text.strip()
            title = article.find('a').text

            date = date_str.split('-')

            if check_date(date, old_date):
                article_link = article.find('a')['href']

                article_response = requests.get(base_url + article_link)
                article_response.raise_for_status()  

                if article_response.status_code == 200:
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    content_p = article_soup.find('div', class_='blog-post-inner').find('p')
                    content = content_p.text.strip() if content_p else 'None'
                    targets_element = article_soup.find('p', id='invisible-text')

                    attachments = article_soup.find_all('a', rel='tag')

                    if targets_element:
                        targets = content = targets_element.get_text(strip=True)

                process_and_store_article(title, date_str, content, attachments, targets)
        write_csv_date(file_path, articles[0].find_previous('span', class_='event-place').text.strip())


def process_and_store_article(title, date_str, content, attachments, targets):
    encoded_title = title.encode('utf-8').decode('utf-8').title()

    print(f"Date: {date_str}, Title: {encoded_title}")
    print(f"Content: {content}")

    for attachment in attachments:
        attachment_name = attachment.text
        attachment_link = 'https://www.est-umi.ac.ma/'+attachment['href']
        print(f"Attachment: {attachment_name} - {attachment_link}")
    print()

    attachment_id = ', '.join([attachment['href'].split('/')[-1] for attachment in attachments])
    attachment_links = ['https://www.est-umi.ac.ma/'+attachment['href'] for attachment in attachments]
    file_names = []
    for link in attachment_links:
        file_names.append(os.path.join(os.getcwd(), 'attachments', re.sub(r'[^\w.-]', '_', link.split('/')[-1])))

    to_send, targets = check_tags(targets)
    
    if to_send:
        email = generate_email(encoded_title, content, attachment_id, ', '.join(targets))
        download_attachment(attachment_links)
        send(encoded_title, email, file_names, targets)

parsed_date = read_csv_file(file_path)[-1].split('-')
scrape_uni_website(parsed_date)