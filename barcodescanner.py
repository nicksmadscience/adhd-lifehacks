import gspread, datetime, subprocess, requests, serial, traceback
from termcolor import colored
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client-secrets.json', scope)
client = gspread.authorize(creds)

sheet = client.open("NMS Inventory")
sheets = sheet.worksheets()

sheetList = {}

for sheet in sheets:
    sheetList[sheet.title.split("/")[0]] = sheet

# state
lastCell = None
lastSheet = None
# lastAction = oh god i dunno i'm trying to build a way to add new entries for an existing barcode

# TODO: View contents of everything with this item as its location

def barcode(code):
	out = ""
	global lastCell, lastSheet, sheetList, sheet, sheets, client
	cmd = code.upper()
 
	cmdSplit = cmd.split("-")
	if cmdSplit[0] in sheetList:
		targetSheet = sheetList[cmdSplit[0]]
		# print (targetSheet)

		cell = targetSheet.find(cmd)
		# print (cell)
		if cell != None:
			rowProperties = targetSheet.row_values(1)
			rowValues = targetSheet.row_values(cell.row)
			for i in range(0, len(targetSheet.row_values(cell.row))):
				out += "{property}: {value}\n".format(property=rowProperties[i], value=rowValues[i])
				print (colored("{property}: {value}".format(property=rowProperties[i], value=rowValues[i]), "cyan"))
    
			# find out if this is a storage entry
			if "Storage" in rowProperties:
				# print ("has a storage field")
				if lastCell != None:
					lastRowProperties = lastSheet.row_values(1)
					if "Location" in lastRowProperties:
						# print ("has a Location field")
						locationColumn = lastRowProperties.index("Location") + 1  # hey I learned about .index() today
						if cell.value != lastCell.value and targetSheet != lastSheet:  # don't store this item inside itself or in another of its kind!
							lastSheet.update_cell(lastCell.row, locationColumn, cell.value)
							print ("{item} is now stored in {storage}".format(item = lastCell.value, storage = cell.value))
							out += "{item} is now stored in {storage}\n".format(item = lastCell.value, storage = cell.value)
							subprocess.Popen(["afplay", "barcode-success.wav"])
							if "LocationDatetime" in lastRowProperties:
								locationDatetimeColumn = lastRowProperties.index("LocationDatetime") + 1  # hey I learned about .index() today
								lastSheet.update_cell(lastCell.row, locationDatetimeColumn, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			else:
				# print ("does not have a storage field")
				subprocess.Popen(["afplay", "barcode-chime.wav"])
    

   
			lastCell = cell
			lastSheet = targetSheet
   
	return out
   
if __name__ == "__main__":
    while True:
        code = input()
        barcode(code)