#!/usr/bin/python3

import cgi
from todo import *
from rng import *
from timer import *
from recur import *

form = cgi.FieldStorage()

print ("Content-Type: text/plain")
print ("")

# First keyword in the message is the app
appRequest = form.getvalue("Body").split(' ')[0]

def test(body):
    return "Test successful!"


# Define our apps here
appList = {'Todo': todo,
           'RNG': rng,
           'Timer': timer,
           'Recur': recur,
           'Test': test}


# See if the app request is in the app list
appFound = False
for appName, appHandler in appList.items():
    if appRequest == appName:
        appFound = True
        print (appHandler(form.getvalue("Body")))

if appFound == False:
    print ("App not found!")


