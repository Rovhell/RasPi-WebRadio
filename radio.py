#!/usr/bin/python
# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN! We do not want the LCD to send anything to the Pi @ 5v
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V
# 16: LCD Backlight GND (Red)
# 17: LCD Backlight GND (Green)
# 18: LCD Backlight GND (Blue)

#import
import RPi.GPIO as GPIO
import time
import os
import datetime

# Define GPIO to LCD mapping
LCD_RS = 25
LCD_E  = 24
LCD_D4 = 23 
LCD_D5 = 17
LCD_D6 = 27
LCD_D7 = 22

# Defomte GPIO for Radio Controls
NEXT = 18
PREV = 4

# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line 

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def main():
	# Main program block
	
	GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
	GPIO.setup(LCD_E, GPIO.OUT)  # E
	GPIO.setup(LCD_RS, GPIO.OUT) # RS
	GPIO.setup(LCD_D4, GPIO.OUT) # DB4
	GPIO.setup(LCD_D5, GPIO.OUT) # DB5
	GPIO.setup(LCD_D6, GPIO.OUT) # DB6
	GPIO.setup(LCD_D7, GPIO.OUT) # DB7
	
	GPIO.setup(NEXT, GPIO.IN) # Next Channel button
	GPIO.setup(PREV, GPIO.IN) # Previous Channel button
	
	# Initialise display
	lcd_init()
	
	lcd_byte(LCD_LINE_1, LCD_CMD)
	lcd_string("",2)
	lcd_byte(LCD_LINE_2, LCD_CMD)
	lcd_string("",2)
	lcd_byte(LCD_LINE_3, LCD_CMD)
	lcd_string("",2)
	lcd_byte(LCD_LINE_4, LCD_CMD)
	lcd_string("", 2)	 
	time.sleep(0.1) 
	currentTrack = 5
	currentName = ["Error","OuiFM  ","FIP  ","France Inter  ","France Culture  "]
	os.system("mpc play %d" % (currentTrack, ))
	time.sleep(1)
	while 1:
		
		
		if ( GPIO.input(NEXT) == False):
			currentTrack = currentTrack + 1
			if ( currentTrack >= 8 ):
				currentTrack = 1
			if ( currentTrack == 7 ):
				os.system("mpc stop")
			else:
				os.system("mpc play %d" % (currentTrack, ))
		
		
		if ( GPIO.input(PREV) == False):
			currentTrack = currentTrack - 1
			if ( currentTrack <= 0 ):
				currentTrack = 7
			if ( currentTrack == 7 ):
				os.system("mpc stop")
			else:
				os.system("mpc play %d" % (currentTrack, ))
		
		
		# Send some text
		if ( currentTrack == 1 ):
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string(datetime.datetime.now().strftime('%H:%M   OuiFM Rock <'),3)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string("Nova  ",3)
			lcd_byte(LCD_LINE_3, LCD_CMD)
			lcd_string("France Inter  ",3)
			lcd_byte(LCD_LINE_4, LCD_CMD)
			lcd_string("France Culture  ",3)
		elif ( currentTrack == 2 ):
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string(datetime.datetime.now().strftime('%H:%M   OuiFM Rock  '),3)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string("Nova <",3)
			lcd_byte(LCD_LINE_3, LCD_CMD)
			lcd_string("France Inter  ",3)
			lcd_byte(LCD_LINE_4, LCD_CMD)
			lcd_string("France Culture  ",3)
		elif ( currentTrack == 3 ):
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string(datetime.datetime.now().strftime('%H:%M   OuiFM Rock  '),3)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string("Nova  ",3)
			lcd_byte(LCD_LINE_3, LCD_CMD)
			lcd_string("France Inter <",3)
			lcd_byte(LCD_LINE_4, LCD_CMD)
			lcd_string("France Culture  ",3)
		elif ( currentTrack == 4 ):
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string(datetime.datetime.now().strftime('%H:%M   OuiFM Rock  '),3)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string("Nova  ",3)
			lcd_byte(LCD_LINE_3, LCD_CMD)
			lcd_string("France Inter  ",3)
			lcd_byte(LCD_LINE_4, LCD_CMD)
			lcd_string("France Culture <",3)
		elif ( currentTrack == 5 ):
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string(datetime.datetime.now().strftime('%H:%M         Nova  '),3)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string("France Inter  ",3)
			lcd_byte(LCD_LINE_3, LCD_CMD)
			lcd_string("France Culture  ",3)
			lcd_byte(LCD_LINE_4, LCD_CMD)
			lcd_string("OuiFM <",3)
		elif ( currentTrack == 6 ):
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string(datetime.datetime.now().strftime('%H:%M  France Inter '),3)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string("France Culture  ",3)
			lcd_byte(LCD_LINE_3, LCD_CMD)
			lcd_string("OuiFM  ",3)
			lcd_byte(LCD_LINE_4, LCD_CMD)
			lcd_string("Fip <",3)
		elif ( currentTrack == 7 ):
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string(datetime.datetime.now().strftime('%H:%M  OFF/AirPlay <'),3)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string("OuiFM Rock  ",3)
			lcd_byte(LCD_LINE_3, LCD_CMD)
			lcd_string("Nova  ",3)
			lcd_byte(LCD_LINE_4, LCD_CMD)
			lcd_string("France Inter  ",3)
		else:
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string(datetime.datetime.now().strftime('%H:%M        ERROR  '),3)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string("   ",3)
			lcd_byte(LCD_LINE_3, LCD_CMD)
			lcd_string("   ",3)
			lcd_byte(LCD_LINE_4, LCD_CMD)
			lcd_string("     ",3)
		
		time.sleep(0.2) 
		
		
#		f=os.popen("mpc current")
#		station = ""
#		for i in f.readlines():
#			station += i
#		
#		
#		
#		# Send some text
#		lcd_byte(LCD_LINE_1, LCD_CMD)
#		lcd_string(datetime.datetime.now().strftime('%H:%M '),2)
#		lcd_byte(LCD_LINE_2, LCD_CMD)
#		lcd_string("",2)
#		lcd_byte(LCD_LINE_3, LCD_CMD)
#		lcd_string("",1)
#		lcd_byte(LCD_LINE_4, LCD_CMD)
#		lcd_string(currentName[currentTrack],1)
#		time.sleep(1) 
	
	
time.sleep(20)

def lcd_init():
	# Initialise display
	lcd_byte(0x33,LCD_CMD)
	lcd_byte(0x32,LCD_CMD)
	lcd_byte(0x28,LCD_CMD)
	lcd_byte(0x0C,LCD_CMD)  
	lcd_byte(0x06,LCD_CMD)
	lcd_byte(0x01,LCD_CMD)  

def lcd_string(message,style):
	# Send string to display
	# style=1 Left justified
	# style=2 Centred
	# style=3 Right justified
	
	if style==1:
		message = message.ljust(LCD_WIDTH," ")  
	elif style==2:
		message = message.center(LCD_WIDTH," ")
	elif style==3:
		message = message.rjust(LCD_WIDTH," ")
	
	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
	# Send byte to data pins
	# bits = data
	# mode = True  for character
	#        False for command
	
	GPIO.output(LCD_RS, mode) # RS
	
	# High bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits&0x10==0x10:
		GPIO.output(LCD_D4, True)
	if bits&0x20==0x20:
		GPIO.output(LCD_D5, True)
	if bits&0x40==0x40:
		GPIO.output(LCD_D6, True)
	if bits&0x80==0x80:
		GPIO.output(LCD_D7, True)
	
	# Toggle 'Enable' pin
	time.sleep(E_DELAY)    
	GPIO.output(LCD_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, False)  
	time.sleep(E_DELAY)      
	
	# Low bits
	GPIO.output(LCD_D4, False)
	GPIO.output(LCD_D5, False)
	GPIO.output(LCD_D6, False)
	GPIO.output(LCD_D7, False)
	if bits&0x01==0x01:
		GPIO.output(LCD_D4, True)
	if bits&0x02==0x02:
		GPIO.output(LCD_D5, True)
	if bits&0x04==0x04:
		GPIO.output(LCD_D6, True)
	if bits&0x08==0x08:
		GPIO.output(LCD_D7, True)
	
	# Toggle 'Enable' pin
	time.sleep(E_DELAY)    
	GPIO.output(LCD_E, True)  
	time.sleep(E_PULSE)
	GPIO.output(LCD_E, False)  
	time.sleep(E_DELAY)   

if __name__ == '__main__':
	main()