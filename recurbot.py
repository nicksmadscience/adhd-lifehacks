#!/usr/bin/python

import argparse, datetime, json
from helpers import *

def morning(recurringEventList, recurringEvents, recurringEventLog, recurringLogged):
    """The job of morning is to simply look at all tasks on deck today, and remind the user
    of said tasks."""
    
    out = "Good morning!  Here are the recurring tasks on deck for you today...\n"
    
    list_eventName = 0
    list_shorthandEventName = 1
    list_recurrence = 2
    list_morningReminder = 3
    list_eveningReminder = 4
    
    for event in recurringEvents:
        if recurringEventIsToday(event[list_recurrence]):
            out += event[list_eventName] + "\n"
            
    print (out)
    return out


def evening(recurringEventList, recurringEvents, recurringEventLog, recurringLogged):
    """More than just looking at the tasks on deck today, we need to see which of them have
    not been fulfilled yet."""
    
    out = "Hey-o, eveningbot here!  Here's where today's recurring tasks stand...\n"
    
    roundup = dailyTaskRoundup(recurringEvents, recurringLogged).items()
    for task, status in roundup:
        if status:
            out += "{task}: Complete\n".format(task = task)
        else:
            out += "{task}: Incomplete\n".format(task = task)
            
    print (out)
    return out
        
    
    
def midnight(recurringEventList, recurringEvents, recurringEventLog, recurringLogged):
    """Mark today's tasks as met or missed so that an accurate streak count can be made.""" 
    
    datetime_string = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    for task, status in dailyTaskRoundup(recurringEvents, recurringLogged).items():
        if status == False:
            print ("Marking as missed: ", task)
            recurringEventLog.append_row([task, datetime_string, "missed"])
        else:
            print ("Not marking as missed: ", task)
            
            

if __name__ == "__main__":
    # Command line params mainly exist to allow cron jobs to know where the config files are located
    parser = argparse.ArgumentParser()
    parser.add_argument("--twiliosecrets", "-t", nargs='?', default="twilio-secrets.json",
                        help="Absolute path to the Twilio secrets file if running from, say, a Cron job.")
    parser.add_argument("--gdrivesecrets", "-g", nargs='?', default="client-secrets.json",
                        help="Absolute path to the Gdrive secrets file if running from, say, a Cron job.")
    parser.add_argument("botmode", nargs='?', default="twilio-secrets.json",
                        help="'morning', 'evening', or 'midnight'.")
    args = parser.parse_args()
    
    # get twilio and gspread set up
    with open(args.twiliosecrets, "r") as secrets_file:
        secrets = json.load(secrets_file)
    twilioClient = Client(secrets["twilio-sid"], secrets["twilio-token"])
    
    gClient = client = openSheet(args.gdrivesecrets)

    recurringEventList = gClient.open("Recurring Event List").sheet1
    recurringEvents = recurringEventList.get_all_values()
    recurringEventLog = gClient.open("Recurring Event Log").sheet1
    recurringLogged = recurringEventLog.get_all_values()


    if args.botmode == "morning":
        sendTwilioTextMessage(twilioClient, secrets["from"], secrets["to"], morning(recurringEventList, recurringEvents, recurringEventLog, recurringLogged))
    elif args.botmode == "evening":
        sendTwilioTextMessage(twilioClient, secrets["from"], secrets["to"], evening(recurringEventList, recurringEvents, recurringEventLog, recurringLogged))
    elif args.botmode == "midnight":
        midnight(recurringEventList, recurringEvents, recurringEventLog, recurringLogged) 
    else:
        print ("Bot mode ('morning', 'evening', or 'midnight' must be specified using the --botmode argument!")