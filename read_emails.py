import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"
KEYWORDS = "received OR \"in touch\" OR \"update soon\" OR \"proceed with another candidate\" OR \"all the best\" OR \"carefully considering your experience and skills\" OR \"first interview\" OR \"availability\" OR \"next step\" OR \"proceed\" OR \"schedule\" OR \"get to know you\" OR \"book\" OR \"conversation\" OR \"stage\" OR \"offer\" OR \"contract\""



def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds and creds.valid:
        pass
    elif creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
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

def main():
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", q=KEYWORDS, maxResults=50).execute()
    messages = results.get("messages", [])
    
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        headers = msg_data["payload"]["headers"]
        sender = get_header(headers, "From")
        subject = get_header(headers, "Subject")
        date = get_header(headers, "Date")  
        snippet = msg_data.get("snippet")
        print(sender, subject, date, snippet)

if __name__ == "__main__":
    main()




