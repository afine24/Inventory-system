"""
	Copyright (C) 2026 Alan Fine

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
from time import sleep
sys.path.append(".venv/lib/python3.12/site-packages/")
sys.path.append("./lib")
import serial
import logger
import requests
import DBhandler
import LCD_2inch
import RPi.GPIO as GPIO
import twoinch_LCD_draw as lcd
from PIL import Image,ImageDraw,ImageFont


email = 'jm85nhsxzc@privaterelay.appleid.com' # PUT YOUR EMAIL HERE
	                                          # doing this will allow OpenFoodFacts to contact you if they need to

L1 = 25
L2 = 23
L3 = 24
L4 = 1

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(L2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(L3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(L4, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

Font1 = ImageFont.truetype("./Font/srcSans3.ttf",30)
srcsans = ImageFont.truetype("./Font/srcSans3.ttf",25)

disp = lcd.getDispObject()

def apiCall(UPCcode):
	logger.log("attempting api call of code " + UPCcode)
	# plug scanned UPC code into url for api call
	url = 'https://world.openfoodfacts.net/api/v2/product/' + UPCcode + '?product_type=all&cc=us&lc=en&fields=product_name,quantity,brands&blame=0'
	useragent = 'InventorySystem/0.2 (' + email + ')'
	headers = {'accept': 'application/json', 'User-Agent': useragent}
	response = requests.get(url, headers=headers)

	if response.status_code == 200:
		# Parse JSON data automatically
		data = response.json()
		# log all successful api calls to aid with troubleshooting failiures due to rate limiting
		logger.log("api call successful, code: " + data.get("code") + " name: " + data.get("product", {}).get("product_name", "null"))
		return(data)
	else:
		# log http errors
		logger.log(f"[Warning!] api call failed with status code: {response.status_code}")
		return 'error'

def pollInput():
	line = ''
	char1 = 'X'
	char2 = 'X'
	char3 = 'X'
	char4 = 'X'
	with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:
		logger.log(f"Successfully connected to /dev/ttyACM0. Ready to scan!")
		while True:
			char1 = readLine(L1, [";1",";2",";3",";A"])
			char2 = readLine(L2, [";4",";5",";6",";B"])
			char3 = readLine(L3, [";7",";8",";9",";C"])
			char4 = readLine(L4, [";*",";0",";#",";D"])
			if (char1 != 'X'):
				sleep(0.2)
				return(char1)
			elif(char2 != 'X'):
				sleep(0.2)
				return(char2)
			elif(char3 != 'X'):
				sleep(0.2)
				return(char3)
			elif(char4 != 'X'):
				sleep(0.2)
				return(char4)

			else:
				pass
			try:
				if ser.in_waiting > 0:
					# Read all available bytes immediately, regardless of newlines
					raw_data = ser.read(ser.in_waiting)
					scanned_barcode = raw_data.decode('utf-8', errors='ignore').strip()
					if scanned_barcode:
						logger.log(f"Scanned Barcode: {scanned_barcode}")
						return(scanned_barcode)
		                    
					time.sleep(0.01)
			except KeyboardInterrupt:    # if a scan somehow throws a keyboard interrupt, catch it
				print("Keyboard Interrupt caught, logged and program resuming")
				logger.log("Keyboard interrupt intercepted, exiting program")
				return
			except serial.SerialException as e:
				print(f"\nError: Could not open or maintain connection to {SERIAL_PORT}.")
				print(f"Details: {e}")
				sys.exit(1)

def readLine(line, characters):
	GPIO.output(line, GPIO.HIGH)
	if(GPIO.input(C1) == 1):
		result = characters[0]
	elif(GPIO.input(C2) == 1):
		result = characters[1]
	elif(GPIO.input(C3) == 1):
		result = characters[2]
	elif(GPIO.input(C4) == 1):
		result = characters[3]
	else:
		result = 'X'
	GPIO.output(line, GPIO.LOW)
	return(result)


requesthome = True
selection = ''

# begin the main loop here
while (True):
	if requesthome:
		lcd.screen.drawHome()
		selection = pollInput()
	match selection:
		case ';1':
			lcd.screen.drawReadyScan(0)
			readcode = pollInput()
			if readcode == ';*':
				requesthome = True
				continue
			data = DBhandler.queryData(readcode)
			# check if code was found in DB
			if data == None:
				lcd.screen.drawNotFound(0)
				selection = pollInput()
				# get selction from within notFound screen
				if selection == ';1':
					# if selected perform api call
					apidata = apiCall(readcode)
					print(apidata)
				elif selection == ';2':
					# quit iteration and prepare for scan again
					requesthome = False
					selection = ';1'
					continue
			else:
				button = ''
				cleantext = ''
				image = lcd.screen.drawFound(0, data[5])
				draw = ImageDraw.Draw(image)
				# write name of product to screen then display it
				draw.text((20, 45), data[2], fill = "BLACK",font=Font1)
				disp.ShowImage(image2)
				# continually ask user for input then when they press enter, make it into an int and pass it to the DBhandler
				# if user presses back at any point, send them back to the ready to scan screen and await scan
				while (button != ';#' or button != ';*'):
					button = pollInput()
					if button[0] != ';':
						continue
					else:
						number = button.replace(";", "")
						if number == 'A':
							continue
						elif number == 'B':
							continue
						elif number == 'C':
							continue
						elif number == 'D':
							continue
						elif number == '*':
							requesthome = False
							selection = ';1'
							continue
						elif number == '#':
							continue
						cleantext = cleantext + number
						draw.text((145, 150), cleantext, fill = "BLACK",font=srcsans)
						disp.ShowImage(image)
				if (len(cleantext) != 0 and button != ';*'):
					DBhandler.editData(readcode, int(cleantext))
				else:
					pass


		
		
			





