#!/usr/bin/python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from helpers import *



def timer(body):
    print ("timer")
    
    
    # STEP 2:  add it to the timer database
    client = openSheet()
    
    # print (str(client))
    
    # return str(client)

    minutes = int(body.split(' ')[1])
    message = body.split(' ', 2)[2]
    
    now = datetime.now()
    expirationTime = now + timedelta(minutes = minutes)
    
    

    # use multiple sheets if you want!
    # sheet_name = body.split('|')[1] #first field is sheet name in this case (remember to share each sheet)
    # print ("sheet name: ", sheet_name)
    sheet = client.open("Timers").sheet1  # You could also put it in a different tab
    
    sheet.append_row([minutes, message, str(expirationTime), 'active'])

    
    # STEP 3 (handled externally): 
    
    return "You have requested a timer for {minutes} minutes, with the message '{message}'".format(minutes = minutes, message = message)



if __name__ == "__main__":
    timer("timer 1 test")