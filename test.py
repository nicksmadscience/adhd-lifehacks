#!/usr/bin/python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# FieldStorage allows us to read GET variables.  Twilio SMS sends the body of a text message as "Body".
import cgi
form = cgi.FieldStorage()
incomingText = form.getvalue("Body")

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client-secrets.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Todo").sheet1

print ("Content-Type: text/plain") # change 
print ("")
print ("Received: {message}".format(message = incomingText))

sheet.append_row([incomingText])