#!/usr/bin/python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

def timer(body):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client-secrets.json', scope)
    client = gspread.authorize(creds)

    try:
        minutes = int(body.split(' ')[1])
    except IndexError:
        return "Please specify a time in minutes!  Syntax:  'Timer [minutes] [expiration message]"
    
    try:
        message = body.split(' ', 2)[2]
    except IndexError:
        return "Please specify a message to be sent to you upon expiration!  Syntax:  'Timer [minutes] [expiration message]"
    
    
    now = datetime.now()
    expirationTime = now + timedelta(minutes = minutes)
 
    sheet = client.open("Timers").sheet1
    
    sheet.append_row([minutes, message, str(expirationTime), 'active'])

    return "You have requested a timer for {minutes} minutes, with the message '{message}'".format(minutes = minutes, message = message)
