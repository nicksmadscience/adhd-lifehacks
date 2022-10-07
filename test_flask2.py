#!/usr/bin/python3

from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client-secrets.json', scope)
client = gspread.authorize(creds)

app = Flask(__name__)

@app.route("/")
def test():
    sheet = client.open("Todo").sheet1
    body = request.args["Body"]

    sheet.append_row([body])
    
    return body