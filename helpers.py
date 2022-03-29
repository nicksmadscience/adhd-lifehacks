#!/usr/bin/python3

import gspread, datetime
from oauth2client.service_account import ServiceAccountCredentials
from config import *

def openSheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(config_gdrive_secrets, scope)
    return gspread.authorize(creds)


def recurringEventIsToday(recurrenceString, today = datetime.datetime.now()):
    
    # daily
    if recurrenceString.find("Daily") != -1:
        return True
    
    # days of week
    if recurrenceString.find(today.strftime("%A")) != -1:
        return True
    
    # day of month
    if recurrenceString.find(today.strftime("%d")) != -1:
        return True
    
    return False


if __name__ == "__main__":
    print ("Content-Type: text/html")
    print ("Cache-Control: no-cache")
    print ("")
    print ("<html><body<h1>nunya bidness</h1></body></html>")