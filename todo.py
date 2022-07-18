#!/usr/bin/python3

import gspread, datetime
from oauth2client.service_account import ServiceAccountCredentials

def todo(body):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client-secrets.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Todo").sheet1

    # Timestamp our entry
    dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    toAdd = [dt]

    # Add a pipe | symbol to split the message into multiple columns.
    # Can be useful as a means of categorizing your entries.
    for field in body[5:].split('|'):
        toAdd.append(field)

    sheet.append_row(toAdd)

    return "Logged: {message}".format(message = body)

