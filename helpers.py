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

def openSheet(gdrive_secrets):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(gdrive_secrets, scope)
    return gspread.authorize(creds)


def recurringEventIsToday(recurrenceString, today = datetime.datetime.now()):
    matches = [
        "Daily",
        today.strftime("%A"),   # day of week
        today.strftime("%dst"), # day of month
        today.strftime("%dnd"),
        today.strftime("%drd"),
        today.strftime("%dth"),
    ]

    return any(x in recurrenceString for x in matches)


def dailyTaskRoundup(recurringEvents, recurringLogged):
    # TODO: these could probably be replaced with something referencing header values
    list_eventName = 0
    list_shorthandEventName = 1
    list_recurrence = 2
    list_morningReminder = 3
    list_eveningReminder = 4
    
    log_shorthandEventName = 0
    log_datetime = 1
    log_requirementMet = 2
    
    completeTasks = []
    todaysTasks = {}
    
    for event in recurringEvents:
        if recurringEventIsToday(event[list_recurrence]):
            todaysTasks[event[list_eventName]] = False
        
        for loggedEvent in recurringLogged:
            if loggedEvent[log_datetime].split(' ')[0] == datetime.datetime.now().strftime("%Y/%m/%d"):
                
                if loggedEvent[log_shorthandEventName] == event[list_shorthandEventName]:
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