#!/usr/bin/python3

# this script will run once a minute (by way of cronjob).  if any active timers have expired,
# this will send a notification to the user and mark said timer as expired.

import gspread, json, argparse
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from twilio.rest import Client
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--secretsfile", "-s", nargs='?', default="twilio-secrets.json")
args = parser.parse_args()




# Secrets file needs to include "twilio-sid" and "twilio-token"; you can grab these
# from your Twilio console.  From and To numbers are also specified here so you're
# not hard-coding your private numbers
with open(args.secretsfile, "r") as secrets_file:
    secrets = json.load(secrets_file)

twilioClient = Client(secrets["twilio-sid"], secrets["twilio-token"])

def sendTwilioTextMessage(twClient, message):
    '''Allows you to send an SMS message from / to the number you specify,
    using the power of Twilio SMS.'''
    message = twClient.messages \
        .create(
                body = message,
                from_ = secrets["from"],
                to = secrets["to"]
            )

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/nick/adhd-lifehacks/client-secrets.json', scope)
gClient = gspread.authorize(creds)

sheet = gClient.open("Timers").sheet1


timers = sheet.get_all_values()

# pprint.pprint (timers)

currentTime = datetime.now()
print (currentTime)


timerRow = 0
for timer in timers:
    timerRow += 1
    
    minutes   = timer[0]
    message   = timer[1]
    timestamp = timer[2]
    active    = timer[3]
    
    
    if active == "active":
        print ("found an active timer!", str(timer))
        
        # 2022-03-21 18:58:30.139443
        expirationTime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        
        if currentTime > expirationTime:
            print ("OMG EXPIRED")
            
            print (twilioClient)

            sendTwilioTextMessage(twilioClient, message)
            
            sheet.update_cell(timerRow, 4, "expired")
        