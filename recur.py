#!/usr/bin/python3

from helpers import *
import datetime

def recur(body):
    client = openSheet("client-secrets.json")

    recurringEventList = client.open("Recurring Event List").sheet1
    recurringEvents = recurringEventList.get_all_values()
    recurringEventLog = client.open("Recurring Event Log").sheet1
    recurringLogged = recurringEventLog.get_all_values()
    
    event = body.split(' ')[1]
    
    if event == "status":
        out = "Here's today's recurring task breakdown so far...\n"
        for task, status in dailyTaskRoundup(recurringEvents, recurringLogged).items():
            if status:
                out += "{task}: Complete\n".format(task = task)
            else:
                out += "{task}: Incomplete\n".format(task = task)
                
        # print (out)
        return (out)
        
    else:
        
        datetime_string = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
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
        
        # see if there's a matching shorthand events name for today
        requirementMet = "?"
        out = ""
        for recurringEvent in recurringEvents:
            
            # print (recurringEvent[list_shorthandEventName])
            
            if recurringEvent[list_shorthandEventName] == event:
                
                if recurringEventIsToday(recurringEvent[list_recurrence]):
                    out += "Hey congrats, you completed {taskfullname} for today!  Your streak is {streak} days!".format(
                        taskfullname = recurringEvent[list_eventName], 
                        streak = streakFinder(recurringEvent[list_shorthandEventName], recurringLogged))
                    
                    # if so, mark in log as daily requirement met
                    requirementMet = "met"
                else:
                    out += "Good job! {taskfullname} was not due today, but I've logged your progress as having gone above and beyond!".format(taskfullname = recurringEvent[list_eventName])
                    requirementMet = "extra"
                
        
        recurringEventLog.append_row([event, datetime_string, requirementMet])
        

        print (out)
        return out
    