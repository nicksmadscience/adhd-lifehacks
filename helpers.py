#!/usr/bin/python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import *

def openSheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(config_gdrive_secrets, scope)
    return gspread.authorize(creds)


if __name__ == "__main__":
    print ("Content-Type: text/html")
    print ("Cache-Control: no-cache")
    print ("")
    print ("<html><body<h1>nunya bidness</h1></body></html>")