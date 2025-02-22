import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  global msg_id
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created autoatically when tmhe authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results_mail = service.users().messages().list(userId="luca.wagensommer@gmail.com", maxResults=1, includeSpamTrash=False, q="from:noreply@vrchat.com subject:Your One-Time*").execute()

    print(results_mail)
    ids = results_mail.get("messages", [])


    if not ids:
      print("No labels found.")
      return
    for id in ids:
      msg_id = id["id"]
      print(msg_id)

    if not msg_id == "":
      results_mail_single = service.users().messages().get(userId="luca.wagensommer@gmail.com", id=msg_id).execute()
      headers = results_mail_single.get("payload", {}).get("headers", [])
      subject = None

      for header in headers:
        if header["name"] == "Subject":
          subject = header["value"]
          break
      print(subject.split("Your One-Time Code is ", 1)[1])


  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()