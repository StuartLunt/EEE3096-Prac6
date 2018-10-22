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
l = 14 #lock line
u = 15 #unlock line
sec = 25 #secure switch GPIO pin
unsec = 18 #insecure switch GPIO pin

#variables
tol = 50 # tolerance
dur=[-1]*16 # duration array
dir=[-1]*16 # direction array 0 = left, 1 = right

combocode = [5000,4000,3000,3000,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] # desired code in milliseconds
code_dir = [1,0,1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] # desired code direction

#GPIO setup
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

GPIO.setup(l, GPIO.OUT, initial=0)
GPIO.setup(u, GPIO.OUT, initial=0 )
GPIO.setup(sec, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(unsec, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Enable ADC pins
mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)

#Function dfinitions
def lock():
    GPIO.output(l,1)
    time.sleep(2)
    GPIO.output(l,0)

def unlock():
    GPIO.output(u,1)
    time.sleep(2)
    GPIO.output(u,0)

def sort(x): # sorting funciton for array
    copy = x
    length = len(x)
    
    new = []
    
    while copy:
        min = x[0]
        for i in x:
            if i<min:
                min = i
        new.append(min)
        copy.remove(min)  
    
    return new

# Main
while True: # while loop continues until push button is pressed
    PB = GPIO.input(sec) # configure pushbutton as GPIO input
    PB1 = GPIO.input(unsec) # configure pushbutton as GPIO input
    pot = mcp.read_adc(0) # pot is the read voltage value from the potentiometer
    time.sleep(0.2)
    
    if PB == False: # waits until pull up resistor goes high
        sec = True # secure mode
        print("Secure Mode Active")

    elif PB1 == False:
        sec = False
        print("Unsecure Mode Active")
    
    #initialize loop variables
    dur = [-1]*16 #durations array
    dir = [-1]*16 #directions array
    i=0 #counter
    direc = -1 # direction of rotation of pot. -1= not moving
    st = False # has not started timing the turn
    pause_start = 0 # pause time to wait for next value
    time_start= 0 # start time while it waits for next value
    pause =False # goes true if a pause is occuring
    finished = False
          
    while i<16 and (sec == False or sec == True): # set to 16 for the full array
        new_pot = mcp.read_adc(0) # read new potentiometer value to see if it has incr. or decr.
        if new_pot- tol > pot and direc!=0: # checks if potentiometer voltage is increasing simbolising turn
            if st == False:
                time_start = time.time() # starts the timer for turn
                st = True # sets to say timer has started
                
            pause_start = 0
            direc = 1 # direc = 1 means it is moving left
            dir[i] = 1 # updates the direction array
            pot = mcp.read_adc(0) #update the current potentiometer value
            pause = False

        elif (new_pot+ tol>pot) and (new_pot-tol < pot) and pause == False: # checks if potentiometer has stopped spinning
            pause_start = time.time() # starts timing to see how long pause lasts
            pause = True
            
        elif time.time() - pause_start >=2 and pause == True:
            break
                
        elif (new_pot+tol>pot) and (new_pot-tol < pot) and time.time()- pause_start >=1 and st == True and pause == True: # waits until pause time is long enough before updating the arrays
            
            print("Number Entered")
            time_stop = time.time()
                
            tot_time = round(time_stop - time_start, 2)*1000 # value for how long potentiometer was rotating in ms
            print(tot_time)
            dur[i] = tot_time # updates the duration array
            i+=1 # increment while loop counter
            direc = -1
            pot = mcp.read_adc(0)
            st = False # set timer start to false
            pause = False
                
        elif new_pot+tol < pot and direc != 1:
            if st == False:
                time_start = time.time()
                st = True
                
            pause_start =0
            direc = 0 # direc = 0 means it is moving right
            dir[i] = 0
            pot = mcp.read_adc(0)
            pause = False
        
        finished = True
        
    if finished == True:
        print(dur)
        print(dir)
            
        if sec == True:
            i=0
            for j in dur: #checks that each element in array matches combocode
                if j+250 > combocode[i] and j-250<combocode[i]: #250 millisecond tolerance allowed
                    dur[i] = combocode[i]
                i+=1
            #print(dur)
            if dur == combocode and dir == code_dir:
                print("Code Correct!")
                os.system('omxplayer Success.mp3') #play success sound for unlock
                unlock()
            
            else:
                print("Incorrect Code Entered")
                os.system('omxplayer Fail.mp3') #play fail sound
                lock()
                            
        elif sec == False:
            sorted = sort(dur) # sorts the recorded durations
            sorted_code = sort(combocode) # sorts the desired code
            
            i=0
            for j in sorted:
                if j+500 > sorted_code[i] and j-500<sorted_code[i]:
                    sorted[i] = sorted_code[i]
                i+=1   
            
            if sorted == sorted_code:  # insecure mode clause
                print("Insecure mode pass")
                os.system('omxplayer Success.mp3')
                unlock()
            
            else:
                print("Insecure mode fail")
                os.system('omxplayer Fail.mp3')
                lock()
    
GPIO.cleanup()
    
    
