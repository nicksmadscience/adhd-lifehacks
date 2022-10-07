#!/usr/bin/python3

from flask import Flask

app = Flask(__name__)

@app.route("/")
def test():
    return "<h1>Hello world!</h1>"