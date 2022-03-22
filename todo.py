#!/usr/bin/python3


import gspread, datetime, traceback, sys, os, cgi
from oauth2client.service_account import ServiceAccountCredentials


def todo(body):
    print ("todo()")
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('/home/nick/adhd-lifehacks/client-secrets.json', scope)
        client = gspread.authorize(creds)

        # use multiple sheets if you want!
        # sheet_name = body.split('|')[1] #first field is sheet name in this case (remember to share each sheet)
        # print ("sheet name: ", sheet_name)
        sheet = client.open("Inbox").sheet1  # You could also put it in a different tab


        dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        today = datetime.datetime.now().strftime("%Y/%m/%d")
        toAdd = [dt]

        for field in body[5:].split('|'):
            print (field)
            toAdd.append(field)

        sheet.append_row(toAdd)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    else:
        return "Logged!"

