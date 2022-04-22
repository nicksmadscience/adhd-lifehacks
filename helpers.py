#!/usr/bin/python3

import gspread, datetime
from oauth2client.service_account import ServiceAccountCredentials
from config import *
from twilio.rest import Client



def sendTwilioTextMessage(twClient, from_, to, message):
    '''Allows you to send an SMS message from / to the number you specify,
    using the power of Twilio SMS.'''
    message = twClient.messages \
        .create(
                body = message,
                from_ = from_,
                to = to
            )

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


def dailyTaskRoundup(recurringEvents, recurringLogged):
    
    list_eventName = 0
    list_shorthandEventName = 1
    list_recurrence = 2
    list_morningReminder = 3
    list_eveningReminder = 4
    
    log_shorthandEventName = 0
    log_datetime = 1
    log_requirementMet = 2
    
    
    # print ("The following tasks are complete today...")
    
    completeTasks = []
    todaysTasks = {}
    
    for event in recurringEvents:
        # print (event)
        if recurringEventIsToday(event[list_recurrence]):
            todaysTasks[event[list_eventName]] = False
        
        # 1. see if there is an entry in the log matching today's date and this task
        
        for loggedEvent in recurringLogged:
            if loggedEvent[log_datetime].split(' ')[0] == datetime.datetime.now().strftime("%Y/%m/%d"):
                # print ("found matching event for today: ", loggedEvent)
                
                if loggedEvent[log_shorthandEventName] == event[list_shorthandEventName]:
                    # print ("HOLY CRAP MATCH FOUND", loggedEvent, loggedEvent[log_shorthandEventName])
                    if loggedEvent[log_shorthandEventName] not in completeTasks:
                        todaysTasks[event[list_eventName]] = True
    
    return todaysTasks


def streakFinder(event, recurringLogged):
    
    streak = 0
    broken = False
    for log in reversed(recurringLogged):
        # print (log)
        if log[0] == event:
            if log[2] == "met" and broken == False:
                streak += 1
            elif log[2] == "missed":
                broken = True
                
    return streak
        
        
    



# if __name__ == "__main__":
#     print ("Content-Type: text/html")
#     print ("Cache-Control: no-cache")
#     print ("")
#     print ("<html><body<h1>nunya bidness</h1></body></html>")