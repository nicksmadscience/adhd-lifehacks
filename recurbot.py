#!/usr/bin/python

import argparse, datetime
from helpers import *

parser = argparse.ArgumentParser()
parser.add_argument("--secretsfile", "-s", nargs='?', default="twilio-secrets.json",
                    help="Absolute path to the Twilio secrets file if running from, say, a Cron job.")
parser.add_argument("--botmode", "-b", nargs='?', default="twilio-secrets.json",
                    help="'morning', 'evening', or 'midnight'.")
args = parser.parse_args()




def morning():
    """The job of morning is to simply look at all tasks on deck today, and remind the user
    of said tasks."""
    
    # TODO: this is going to need to be sent using sendTwilioTextMessage
    print ("Good morning!  Here are the recurring tasks on deck for you today...")
    
    client = openSheet()
    
    list_eventName = 0
    list_shorthandEventName = 1
    list_recurrence = 2
    list_morningReminder = 3
    list_eveningReminder = 4
    
    recurringEventList = client.open("Recurring Event List").sheet1
    recurringEvents = recurringEventList.get_all_values()
    
    for event in recurringEvents:
        if recurringEventIsToday(event[list_recurrence]):
            print (event[list_eventName])
        
    
    

def evening():
    """More than just looking at the tasks on deck today, we need to see which of them have
    not been fulfilled yet."""
    
    client = openSheet()
    
    list_eventName = 0
    list_shorthandEventName = 1
    list_recurrence = 2
    list_morningReminder = 3
    list_eveningReminder = 4
    
    log_shorthandEventName = 0
    log_datetime = 1
    log_requirementMet = 2
    
    recurringEventList = client.open("Recurring Event List").sheet1
    recurringEvents = recurringEventList.get_all_values()
    
    print ("Hey-o, eveningbot here!")
    print ("The following tasks are complete today...")
    
    completeTasks = []
    
    # look through the recurring event list and
    for event in recurringEvents:
        
        # 1. see if there is an entry in the log matching today's date and this task
        recurringEventLog = client.open("Recurring Event Log").sheet1
        recurringLogged = recurringEventLog.get_all_values()
        
        for loggedEvent in recurringLogged:
            if loggedEvent[log_datetime].split(' ')[0] == datetime.datetime.now().strftime("%Y/%m/%d"):
                # print ("found matching event for today: ", loggedEvent)
                
                if loggedEvent[log_shorthandEventName] == event[list_shorthandEventName]:
                    # print ("HOLY CRAP MATCH FOUND", loggedEvent, loggedEvent[log_shorthandEventName])
                    if loggedEvent[log_shorthandEventName] not in completeTasks:
                        completeTasks.append(loggedEvent[log_shorthandEventName])
                    
    print (completeTasks)
            
            
            
            
            # if True...
            # congratulate user probably
            # else
            # remind user that this task is unfinished
    
    
    
    
    
def midnight():
    """Mark today's tasks as met or missed so that an accurate streak count can be made.""" 
    print ("it is (just before) midnight")



if args.botmode == "morning":
    morning()
elif args.botmode == "evening":
    evening()
elif args.botmode == "midnight":
    midnight() 
else:
    print ("Bot mode ('morning', 'evening', or 'midnight' must be specified using the --botmode argument!")