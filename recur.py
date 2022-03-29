#!/usr/bin/python3

from helpers import *
import datetime

def recur(body):
    event = body.split(' ')[1]
    
    client = openSheet()
    
    recurringEventLog = client.open("Recurring Event Log").sheet1
    datetime_string = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
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
    requirementMet = "?"
    for recurringEvent in recurringEvents:
        
        # print (recurringEvent[list_shorthandEventName])
        
        if recurringEvent[list_shorthandEventName] == event:
            
            if recurringEventIsToday(recurringEvent[list_recurrence]):
                print ("Hey congrats, you completed {taskfullname} for today!  Your streak is X days!".format(taskfullname = recurringEvent[list_eventName]))
                
                # if so, mark in log as daily requirement met
                requirementMet = "met"
            else:
                print ("Good job! {taskfullname} was not due today, but I've logged your progress as having gone above and beyond!".format(taskfullname = recurringEvent[list_eventName]))
                requirementMet = "extra"
            
 
    
    
    recurringEventLog.append_row([event, datetime_string, requirementMet])
    
    
    
    # if it was met, respond to user saying it was met
    
    
    
    return ""
    