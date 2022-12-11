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

    # Get the app handler function for the requested app
    appHandler = appList.get(app)

    # If the app handler function was found, call it and create a response
    if appHandler:
        resp = make_response(appHandler(request.args["Body"]), 200)
    else:
        resp = make_response("App not found!", 404)
        
    resp.mimetype = "text/plain"

    print (resp.data)
    return resp


