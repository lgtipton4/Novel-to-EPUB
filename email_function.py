import base64
import os
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# What the program requires of the user's account
SCOPES = ["https://www.googleapis.com/auth/gmail.compose", "https://www.googleapis.com/auth/gmail.send"]

def send_email(address, filename):
    # Credentials created or read in here
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        # Create email message with attachment, encode in base64 as Gmail expects
        with open(filename, "rb") as f:
            part = MIMEBase("application", "epub+zip")
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        message = MIMEMultipart()
        message['Subject'] = "Convert"
        message['From'] = "me"
        message['To'] = address
        html_part = MIMEText("This is an automated email.")
        message.attach(html_part)
        message.attach(part)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': raw_message}

        # Send the message via Gmail's API
        send_message = service.users().messages().send(userId='me', body=create_message).execute()
        print(f'Message Id: {send_message["id"]}')

    except HttpError as error:
        print(f"An error occurred: {error}")
    return