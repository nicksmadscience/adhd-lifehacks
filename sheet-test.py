import gspread, datetime
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client-secrets.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Shot logger").sheet1



dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
today = datetime.datetime.now().strftime("%Y/%m/%d")

sheet.append_row([dt, "test"])


entries = sheet.get_all_records()

shotcounter = 0
for entry in entries:
    if (entry["datetime"][0:10] == today):
        shotcounter += 1

print (shotcounter)

