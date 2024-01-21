# UniUpdateBot README for School Staff

## Introduction
UniUpdateBot is a user-friendly, automated web scraper designed for school staff to monitor the university's website for real-time updates. It simplifies the process of disseminating timely information by extracting updates and sending structured email notifications to students and professors. No advanced technical knowledge is required; simply set up the `emails.xlsx` and `Date Tracker.csv` files, configure the `.env` file, and the `Attachments` folder to get started.

## Setup and Configuration

### 1. emails.xlsx
This Excel file should contain the list of email recipients. Make sure to structure the Excel file with appropriate column headers for names and email addresses and change `sender.py` accordingly.

### 2. Date Tracker.csv
The `Date Tracker.csv` file keeps track of the last update times to avoid duplicate notifications. Update the file with the latest dates as needed.

### 3. .env File Configuration
The `.env` file is where sensitive information such as login credentials and the OpenAI API keys are stored. Follow the template provided to fill out the necessary fields:

```plaintext
OPENAI_API_KEY= Your OpenAI API key
EMAIL_ADDRESS= Your email address
EMAIL_PASSWORD= Your email's 2F password
```
### 4. Attachments Folder
Create a folder named `Attachments` where attachments will be stored.

## Tags Syntax
Every article set to be published needs to contain tags that will allow the bot to detect it and send it.

- ##### For sending an article: `#SEND#`
- ##### For specifying who the email is targeted to: `#TO:TARGET,SEPERATED,BY,COMMAS`
- ##### Available Targets: ALL, GC, GI, IATE, DWM, GIM, GTE, GE, CPA, TCC, GRH, FBA, LM, LP, PROF
- ##### HTML Syntax for adding tags
```html
<p id="invisible-text" style="display: none;">#SEND# #TO:(Targets)#</p>
```

## Usage and Maintainance
To run the bot, simply execute `scraper.py`. Unfortunately, OpenAI's GPT is not reliable enough to run autonomously, that's why the bot needs a person to act as a supervisor.
Whenever a new email is written, a new MSWord window is opened to allow the supervisor to apply changes if necessary.
