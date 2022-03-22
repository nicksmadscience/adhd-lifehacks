#!/usr/bin/python3

import cgi
from todo import *
from rng import *
from timer import *

form = cgi.FieldStorage()

print ("Content-Type: text/plain")
print ("Cache-Control: no-cache")
print ("")

appRequest = form.getvalue("Body").split(' ')[0]
# print ("appRequest: ", appRequest)

# appList = {'Todo': 'todo'}

# print (todo("Todo Inbox|check test"))

# for appName, appHandler in appList.items():
#     print ("appName: ", appName)
#     print ("appHandler: ", appHandler)
#     if appRequest == appName:
#         print ("match")
#         print (appHandler(form.getvalue("Body")))


if appRequest == "Todo":
    print (todo(form.getvalue("Body")))
elif appRequest == "RNG":
    print (rng(form.getvalue("Body")))
elif appRequest == "Timer":
    print (timer(form.getvalue("Body")))
else:
    print ("App not found!")


