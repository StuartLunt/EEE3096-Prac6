import RPi.GPIO as GPIO
import Adafruit_MCP3008, time, os, sys, spidev
from datetime import datetime, timedelta
from threading import Event

#Open SPI bus
spi=spidev.SpiDev()
spi.open(0,0)

#Set up GPIO
GPIO.setmode(GPIO.BCM)

#Pin definitions
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
l = 14
u = 15
s = 18

#variables
tol = 50
dur=[0]*16
dir=[0]*16

#GPIO setup
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

GPIO.setup(l, GPIO.OUT, initial=0)
GPIO.setup(u, GPIO.OUT, initial=0 )
GPIO.setup(s, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(switch4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Main function
mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)
values=[0]*8

#Event detection set up
GPIO.add_event_detect(switch1, GPIO.FALLING, callback=reset, bouncetime=200)
GPIO.add_event_detect(switch2, GPIO.FALLING, callback=frequency, bouncetime=200)
GPIO.add_event_detect(switch3, GPIO.FALLING, callback=stop, bouncetime=200)
GPIO.add_event_detect(switch4, GPIO.FALLING, callback=display, bouncetime=200)

#Function dfinitions
def lock():
    GPIO.output(l,1)
    time.sleep(2)
    GPIO.output(l,0)

def unlock():
    GPIO.output(u,1)
    time.sleep(2)
    GPIO.output(u,0)

def readCode():
    #read and time code here
    # 2 sec time out

def checkCode():
    #Compare codes
    #play sounds

def sort():
    #sort

