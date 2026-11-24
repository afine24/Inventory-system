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
import os
import sys 
import time
import logger
import spidev as SPI
sys.path.append("..")
import LCD_2inch
from PIL import Image,ImageDraw,ImageFont


# RPi pin config
RST = 27
DC = 22
BL = 18
bus = 0 
device = 0 

disp = LCD_2inch.LCD_2inch()
# Initialize library.
disp.Init()
# Clear display.
disp.clear()
# Set the backlight to 50%
disp.bl_DutyCycle(50)

fancyFont = ImageFont.truetype("./Font/fancyfont.ttf",25)
srcsans = ImageFont.truetype("./Font/srcSans3.ttf",25)
digitalFont = ImageFont.truetype("./Font/digitalfont.ttf",25)

def getDispObject():
	return disp


class screen:
	def drawHome():
		disp.clear()
		image = Image.open("assets/homePage.png")
		logger.log("drawing home screen")
		disp.ShowImage(image)
		return 
	
	def drawReadyScan(remove):
		disp.clear()
		if remove:
			image = Image.open("assets/readyToScan-Remove.png")
			logger.log("drawing ready screen - Remove")
		else:
			image = Image.open("assets/readyToScan-Add.png")
			logger.log("drawing ready screen - Add")
		disp.ShowImage(image)
		return

	def drawFound(remove, currentQuantity):
		disp.clear()
		if remove:
			image = Image.open("assets/foundItem-Remove.png")
			draw = ImageDraw.Draw(image)
			logger.log("drawing found screen - Remove")
		else:
			image = Image.open("assets/foundItem-Add.png")
			draw = ImageDraw.Draw(image)
			logger.log("drawing found screen - Add")

		draw.text((145, 109), str(currentQuantity), fill = "BLACK",font=srcsans)
		disp.ShowImage(image)
		return image

	def drawNotFound(remove):
		disp.clear()
		if remove:
			image = Image.open("assets/notFoundItem-Remove.png")
			logger.log("drawing not found screen - Remove")
		else:
			image = Image.open("assets/notFoundItem-Add.png")
			logger.log("drawing not found screen - Add")

		disp.ShowImage(image)
		return

		
			