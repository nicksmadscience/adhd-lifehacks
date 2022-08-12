#!/usr/bin/python

import argparse, datetime, json
from helpers import *



def morning():
    """The job of morning is to simply look at all tasks on deck today, and remind the user
    of said tasks."""
    
    out = "Good morning!  Here are the recurring tasks on deck for you today...\n"
    
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
            out += event[list_eventName] + "\n"
            
    print (out)
    return out


        
    
    

def evening():
    """More than just looking at the tasks on deck today, we need to see which of them have
    not been fulfilled yet."""
    
    out = "Hey-o, eveningbot here!  Here's where today's recurring tasks stand...\n"
    
    client = openSheet()
    recurringEventList = client.open("Recurring Event List").sheet1
    recurringEvents = recurringEventList.get_all_values()
    recurringEventLog = client.open("Recurring Event Log").sheet1
    recurringLogged = recurringEventLog.get_all_values()
    
    for task, status in dailyTaskRoundup(recurringEvents, recurringLogged).items():
        if status:
            out += "{task}: Complete\n".format(task = task)
        else:
            out += "{task}: Incomplete\n".format(task = task)
            
    print (out)
    return out
        
        
            
            
            
            
            # if True...
            # congratulate user probably
            # else
            # remind user that this task is unfinished
    
    
    
    
    
def midnight():
    """Mark today's tasks as met or missed so that an accurate streak count can be made.""" 
    print ("it is (just before) midnight")
    
    client = openSheet()
    recurringEventList = client.open("Recurring Event List").sheet1
    recurringEvents = recurringEventList.get_all_values()
    recurringEventLog = client.open("Recurring Event Log").sheet1
    recurringLogged = recurringEventLog.get_all_values()
    
    datetime_string = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    for task, status in dailyTaskRoundup(recurringEvents, recurringLogged).items():
        if status == False:
            print ("Marking as missed: ", task)
            recurringEventLog.append_row([task, datetime_string, "missed"])
        else:
            print ("Not marking as missed: ", task)
            
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--secretsfile", "-s", nargs='?', default="twilio-secrets.json",
                        help="Absolute path to the Twilio secrets file if running from, say, a Cron job.")
    parser.add_argument("--botmode", "-b", nargs='?', default="twilio-secrets.json",
                        help="'morning', 'evening', or 'midnight'.")
    args = parser.parse_args()
    
    with open(args.secretsfile, "r") as secrets_file:
        secrets = json.load(secrets_file)
        print (secrets)

    twilioClient = Client(secrets["twilio-sid"], secrets["twilio-token"])



    if args.botmode == "morning":
        sendTwilioTextMessage(twilioClient, secrets["from"], secrets["to"], morning())
    elif args.botmode == "evening":
        sendTwilioTextMessage(twilioClient, secrets["from"], secrets["to"], evening())
    elif args.botmode == "midnight":
        midnight() 
    else:
        print ("Bot mode ('morning', 'evening', or 'midnight' must be specified using the --botmode argument!")