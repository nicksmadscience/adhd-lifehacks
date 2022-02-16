#!/usr/bin/env python

import cgi, cgitb, datetime, traceback

form = cgi.FieldStorage()

cgitb.enable()



import gspread, datetime
from oauth2client.service_account import ServiceAccountCredentials


print ("Content-Type: text/plain")
print ("Cache-Control: no-cache")
print ("")

import platform
print(platform.python_version())

try:
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/nick/adhd-lifehacks/client-secrets.json', scope)
    client = gspread.authorize(creds)

    # use multiple sheets if you want!
    sheet_name = form.getvalue("Body").split('|') #first field is sheet name in this case (remember to share each sheet)
    sheet = client.open(sheet_name[0]).sheet1  # You could also put it in a different tab


    dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    today = datetime.datetime.now().strftime("%Y/%m/%d")
    toAdd = [dt]

    for field in form.getvalue("Body").split('|'):
        print (field)
        toAdd.append(field)

    sheet.append_row(toAdd)


    # entries = sheet.get_all_records()
except Exception as e:
    print (e)
else:
    print ("Logged!")

