import RPi.GPIO as GPIO
import Adafruit_MCP3008, time, os, sys, spidev
from datetime import datetime, timedelta
from threading import Event

#Open SPI bus
spi=spidev.SpiDev()
spi.open(0,0)

#Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Pin definitions
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
l = 14
u = 15
sec = 25 #secure switch mode
unsec = 18 #insecure switch mode

#variables
tol = 50 # tolerance
dur=[0]*16 # duration array
dir=[0]*16 # direction array 0 = left, 1 = right

combocode = [500,400,300,300,0,0,0,0,0,0,0,0,0,0,0,0] # desired code
code_dir = [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0] # desired code order

#GPIO setup
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

GPIO.setup(l, GPIO.OUT, initial=0)
GPIO.setup(u, GPIO.OUT, initial=0 )
GPIO.setup(sec, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(unsec, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(switch4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

PB = GPIO.input(sec) # configure pushbutton as GPIO input
PB1 = GPIO.input(unsec) # configure mode pushbutton as GPIO input

#Main function
mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)
values=[0]*8

#Event detection set up
##GPIO.add_event_detect(s, GPIO.FALLING, callback=reset, bouncetime=200)

#Function dfinitions
def lock():
    GPIO.output(l,1)
    time.sleep(2)
    GPIO.output(l,0)

def unlock():
    GPIO.output(u,1)
    time.sleep(2)
    GPIO.output(u,0)

#def readCode():
    #read and time code here
    # 2 sec time out

#def checkCode():
    #Compare codes
    #play sounds

def sort(x): # sorting funciton for array
    copy = x
    length = len(x)
    
    new = []
    
    while copy:
        min = x[0]
    #sort
        for i in x:
            if i<min:
                min = i
        new.append(min)
        copy.remove(min)  
    
    return new

# Main

while True: # while loop continues until push button is pressed
    time.sleep(0.1)
    pot = mcp.read_adc(0) # pot is the read voltage value from the potentiometer
    #print(pot)
    time.sleep(0.2)
       
    if PB == False: # waits until pull up resistor goes high
        sec = False # security mode
        print("Secure Mode Active")

    elif PB1 != False:
        sec = True
        print("Unsecure Mode Active")
     
    dur = [0]*16
    dir = [0]*16
    i=0
    direc = -1 # direction of rotation of pot. -1= not moving
    st = False # has not started timing the turn
    pause_start = 0 # pause time to wait for next value
    time_start= 0 # start time while it waits for next value
    pause =False # goes true if a pause is occuring
    finished = False
          
    while i<16 and (sec == False or sec == True): # set to 16 for the full array
        new_pot = mcp.read_adc(0) # read new potentiometer value to see if it has incr. or decr.
        
        if new_pot- tol > pot and direc!=0: # checks if potentiometer voltage is increasing simbolising turn
            #print("new>old")
            if st == False:
                time_start = time.time() # starts the timer for turn
                st = True # sets to say timer has started
                print("started")
                
            pause_start = 0
            direc = 1 # direc = 1 means it is moving left
            dir[i] = 1 # updates the direction array
            pot = mcp.read_adc(0) #update the current potentiometer value
            pause = False

        elif (new_pot+ tol>pot) and (new_pot-tol < pot) and pause == False: # checks if potentiometer has stopped spinning
            #print("paused")
            pause_start = time.time() # starts timing to see how long pause lasts
            #direc = -1 # sets direction to not moving
            pause = True
            
        elif time.time() - pause_start >=2 and pause == True:
            break
                
        elif (new_pot+tol>pot) and (new_pot-tol < pot) and time.time()- pause_start >=1 and st == True and pause == True: # waits until pause time is long enough before updating the arrays
            
            print("in")
            time_stop = time.time()
                
            tot_time = round(time_stop - time_start, 2)*100 # value for how long potentiometer was rotating in ms
            print(tot_time)
            dur[i] = tot_time # updates the duration array
            i+=1 # increment while loop counter
            direc = -1
            pot = mcp.read_adc(0)
            st = False # set timer start to false
            pause = False
                
        elif new_pot+tol < pot and direc != 1:
            #print("new<old")
            if st == False:
                #print("started")
                time_start = time.time()
                st = True
                print("started reverse")
                
            pause_start =0
            direc = 0 # direc = 0 means it is moving right
            dir[i] = 0
            pot = mcp.read_adc(0)
            pause = False
        
        finished = True

        
    if finished == True:
        print(dur)
        print(dir)
            
        #j=0
        #while j<16:
            #dur[j] = round(dur[j]) # rounds off the array variables
            #j+=1
                    
        #print(dur)
            
            
        if sec == False:
            i=0
            for j in dur:
                if j+tol > combocode[i] and j-tol<combocode[i]:
                    dur[i] = combocode[i]
                i+=1
            print(dur)
            if dur == combocode and dir == code_dir:
                print("Code Correct!")
            
            else:
                print("Incorrect Code Entered")


            
        elif sec == True:
            sorted = sort(dur) # sorts the recorded durations
            sorted_code = sort(combocode) # sorts the desired code
            
            i=0
            for j in sorted:
                if j+tol > sorted_code[i] and j-tol<sorted_code[i]:
                    sorted[i] = sorted_code[i]
                i+=1
                
            
            if sorted == sorted_code:  # insecure mode clause
                print("Insecure mode pass")
                os.system("")
            
            else:
                print("Insecure mode fail")
                os.system("")
            
        break
                
        
        
        
        #return dur,tol

    
    
    
    