import time
import os.path
import base64
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from google import genai

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"
KEYWORDS = "received OR \"in touch\" OR \"update soon\" OR \"proceed with another candidate\" OR \"all the best\" OR \"carefully considering your experience and skills\" OR \"first interview\" OR \"availability\" OR \"next step\" OR \"proceed\" OR \"schedule\" OR \"get to know you\" OR \"book\" OR \"conversation\" OR \"stage\" OR \"offer\" OR \"contract\""

load_dotenv()

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except RefreshError:
            creds = None

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def get_header(headers, name):
    for header in headers:
        if header["name"] == name:
            return header["value"]

def get_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"]["data"]
                return base64.urlsafe_b64decode(data).decode("utf-8")
    else:
        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data).decode("utf-8")
    return ""

def main():
    client = genai.Client()
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", q=KEYWORDS, maxResults=15).execute()
    messages = results.get("messages", [])
    
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]
        sender = get_header(headers, "From")
        subject = get_header(headers, "Subject")
        date = get_header(headers, "Date")  
        body = get_body(msg_data["payload"])
        result = classify_email(client, sender, subject, body)
        category, ai_date, company, role = parse_classification(result)
        print(sender, subject, category, ai_date, company, role)
        time.sleep(15)


def classify_email(client, sender, subject, body):
    prompt = f"""
Among the emails select the ones that are job related and sort them out through the 5 categories below.

Classify the email by status (the categories) and key dates (e.g. interview date mentioned in the email)

Applied: We've received your application, We're currently reviewing your application, will be in touch with next steps, We'll carefully review your profile and be in touch with an update soon, your application was sent, We just got your application
Process ongoing: I would like to set up a first digital interview, Please give me a few options when you are available for next week. It went well and would like for you to continue. Next step is to have a digital call with me. We would like for you to proceed and do the case. We would like to schedule a Phone Interview. Please click the Schedule Interview button below. After reviewing your application documents, I would like to get to know you better. Please book an appointment for a phone call. I look forward to our conversation! Our recruiting team is delighted to invite you to proceed to the assessment stage.
Rejected: Unfortunately, After careful consideration, we don't feel this role is likely to be a perfect fit. Wish you the very best of luck in your future endeavours. You didn't go all the way in this recruitment process. In the face of strong competition, we have decided to proceed with another candidate.
Offer: Congratulations! We are excited to provide you with an offer of employment. You have given us the privilege to be a part of your career. We would like to welcome you to a digital contract signing.
Not Job-related (false positive): Emails from Glassdoor, JobLeads, Github, Indeed, bootcamp

Respond in exactly this format:
Category: <one of the 5 categories>
Date: <any date mentioned, or "None">
Company: <the company name>
Role: <the job title/role mentioned, or "None" if unclear>

Email details:
Sender: {sender}
Subject: {subject}
Email body: {body}
"""
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )
    return response.text

def parse_classification(response_text):
    lines = response_text.strip().split("\n")
    category = lines[0].split(":", 1)[1].strip()
    date = lines[1].split(":", 1)[1].strip()
    company = lines[2].split(":", 1)[1].strip()
    role = lines[3].split(":", 1)[1].strip()
    return category, date, company, role


if __name__ == "__main__":
    main()








