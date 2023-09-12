#!/usr/bin/env python3

from I2CLCD1602.PCF8574 import PCF8574_GPIO
from I2CLCD1602.Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep

## Varaibles ##
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

def CleanLCD():
    lcd.clear()

def PrintLCDEvent(topMessage, bottomMessage, duration, lcdIntensity):
    SetGPIOAdapter()
    mcp.output(3,lcdIntensity)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns

    lcd.setCursor(0,0)  # set cursor position
    lcd.message( topMessage +'\n' )# display CPU temperature
    lcd.message( bottomMessage )   # display the time
    sleep(duration)
    #lcd.clear()

def PrintLCDLoop(uid):
    #SetGPIOAdapter()
    mcp.output(3,0)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns

    lcd.setCursor(0,0)  # set cursor position
    lcd.message("     WELCOME    " +'\n')# display CPU temperature
    lcd.message( " STICKYLOCK ML " )   # display the time

def SetGPIOAdapter():
    PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
    PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
    # Create PCF8574 GPIO adapter.
    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except:
        try:
            mcp = PCF8574_GPIO(PCF8574A_address)
        except:
            print ('I2C Address Error !')
            exit(1)
    # Create LCD, passing in MCP GPIO adapter.
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

