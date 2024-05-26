import os.path
import logging
import re
import base64
import time
import email.utils
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup
from constants import SCOPES, TOKEN_FILE
from email_db_handler.email_db_utils import add_email_in_db


def fetch_service_object():
    creds = None
    if os.path.exists(TOKEN_FILE):
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
        service = build("gmail", "v1", credentials=creds)
        return service
    except Exception as error:
        logging.error(f"Error occurred in fetching gmail service {str(error)}")
        raise error

class UserEmailService():
    def __init__(self) -> None:
        self.user_id = "me"
        self.service = fetch_service_object()
        self.user_email = None
        self.labels = ['INBOX', 'UNREAD']

    def get_user_email(self):
        try:
            user_info = self.service.users().getProfile(userId=self.user_id).execute()
            self.user_email = user_info['emailAddress']
        except HttpError as error:
            logging.error(f"Error in fetching user's email address: {error}")
            raise error


    def get_unread_message_ids_from_inbox(self):
        unread_email_ids = self.service.users().messages().list(userId='me',labelIds=self.labels).execute()
        return unread_email_ids["messages"]
    

    def process_email_headers(self, headers, fetch_header_name):
        for header in headers:
            if header["name"] == fetch_header_name:
                return header["value"]

    def process_email_body(self, payload):
        try:
            mssg_parts = payload['parts'] # fetching the message parts
            part_one  = mssg_parts[0] # fetching first element of the part 
            part_body = part_one['body'] # fetching body of the message
            part_data = part_body['data'] # fetching data from the body
            clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
            clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
            clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
            soup = BeautifulSoup(clean_two , "lxml" )
            mssg_body = soup.body()
            return mssg_body
        except :
            pass


    def get_messages_from_email_ids(self, unread_email_ids):
        for email_id in unread_email_ids:
            email_message = dict()
            message = self.service.users().messages().get(userId=self.user_id, id=email_id["id"]).execute()
            payload = message['payload']
            header = payload['headers']
            email_message["email_id"] = email_id["id"]
            email_message["reciever"] = self.process_email_headers(header, "Delivered-To")
            email_message["sender"] = self.process_email_headers(header, "From")
            email_message["subject"] = self.process_email_headers(header, "Subject")
            email_message["received_date"] = email.utils.parsedate_to_datetime(self.process_email_headers(header, "Date"))
            email_message["email_body"] = self.process_email_body(payload)
            add_email_in_db(email_message)
            self.service.users().messages().modify(userId=self.user_id, id=email_id["id"],body={ 'removeLabelIds': ['UNREAD']}).execute() 


def fetch_email_from_gmail():
    es = UserEmailService()
    es.get_user_email()
    unread_email_ids = es.get_unread_message_ids_from_inbox()
    es.get_messages_from_email_ids(unread_email_ids)


if __name__ == "__main__":
    fetch_email_from_gmail()
