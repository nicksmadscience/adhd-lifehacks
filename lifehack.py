#!/usr/bin/python3

from flask import Flask, request, make_response
from todo import *
from rng import *
from timer import *
from recur import *

def test(body):
    return "Test successful!"

# Define our apps here
appList = {'Todo': todo,
           'RNG': rng,
           'Timer': timer,
           'Recur': recur,
           'Test': test}

app = Flask(__name__)

@app.route("/")
def hello_world():
    print (request.args["Body"])

    appRequest = request.args["Body"].split(' ')[0]

    # See if the app request is in the app list
    appFound = False
    for appName, appHandler in appList.items():
        if appRequest == appName:
            appFound = True
            resp = make_response(appHandler(request.args["Body"]), 200)

    if appFound == False:
        resp = make_response("App not found!", 404)
        
    resp.mimetype = "text/plain"

    print (resp.data)
    return resp


