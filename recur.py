#!/usr/bin/python3

from helpers import *
import datetime

def recur(body):
    event = body.split(' ')[1]
    
    client = openSheet()
    
    recurringEventLog = client.open("Recurring Event Log").sheet1
    datetime_string = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    # Shorthand Event Name	   Datetime
    recurringEventLog.append_row([event, datetime_string])
    
    # next steps
    # cross reference the recurring event list
    list_eventName = 0
    list_shorthandEventName = 1
    list_recurrence = 2
    list_morningReminder = 3
    list_eveningReminder = 4
    
    # Shorthand Event Name	Datetime	Requirement Met
    log_shorthandEventName = 0
    log_datetime = 1
    log_requirementMet = 2
    
    recurringEventList = client.open("Recurring Event List").sheet1
    
    recurringEvents = recurringEventList.get_all_values()
    
    
    
    
    # see if there's a matching shorthand events name for today
    recurringEventLogRow = 0
    for recurringEvent in recurringEvents:
        recurringEventLogRow += 1
        
        print (recurringEvent[list_shorthandEventName])
        
        if recurringEvent[list_shorthandEventName] == event:
            print ("HOLY CRAP EVENT FOUND")
    
    
    # if so, mark in log as daily requirement met
        recurringEventLog.update_cell(recurringEventLogRow, log_requirementMet, "expired")
    
    
    # if it was met, respond to user saying it was met
    
    
    
    return event
    