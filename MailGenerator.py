from openai import OpenAI
from dotenv import load_dotenv
import os
import tempfile
import subprocess

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)
prompt_file = "./prompt.txt"

def get_prompt(path):
    with open(path, 'r') as f:
        return f.read()

def check_for_mistakes(email):
    try:
        with tempfile.NamedTemporaryFile(mode='w+', suffix=".txt", delete=False) as temp_file:
            temp_file.write(email)
            temp_file_path = temp_file.name

        command = ["C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE", temp_file_path]
        subprocess.run(command)

        input("Edit the text in VSCode. Press Enter when done...")

        with open(temp_file_path, 'r') as edited_file:
            edited_text = edited_file.read()

        return edited_text

    except Exception as e:
        print(f"An error occurred: {e}")

def generate_email(title, body, attachments, Targets):
    prompt = get_prompt(prompt_file)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"Title: {title}\nBody: {body}\nAttachements names: {attachments}\Targets: {Targets}"
            }
        ],
        temperature=1,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    generated_email = response.choices[0].message.content.encode('utf-8').decode('utf-8')

    email = check_for_mistakes(generated_email)

    return email
