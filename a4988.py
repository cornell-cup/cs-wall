import RPi.GPIO as GPIO
from time import sleep

import serial
import wiringpi

serial = serial.Serial("/dev/ttyUSB0", baudrate=9600)
  
from time import sleep  
# wiringpi.wiringPiSetupGpio()  
# wiringpi.pinMode(24, 1)  # sets GPIO 24 to output
# wiringpi.digitalWrite(24, 1) # sets port 24 to 1 (3V3, on)


code = ''
direction =0
number = 0

dictionary = {'59004312D': 'move forward','590045F232DC' : 'endtag', '59004312DDD5': 'move forward'}

GPIO.setmode(GPIO.BCM)

#Buttons Setup
#GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

scanner_top_pin = 21
scanner_bottom_pin = 19 # was26
horizontal_top_pin = 16
horizontal_bottom_pin = 20
vertical_top_pin = 13
vertical_bottom_pin= 26 # was19

GPIO.setup(scanner_top_pin, GPIO.IN)
GPIO.setup(scanner_bottom_pin, GPIO.IN)
GPIO.setup(horizontal_top_pin, GPIO.IN)
GPIO.setup(horizontal_bottom_pin, GPIO.IN)
GPIO.setup(vertical_top_pin, GPIO.IN)
GPIO.setup(vertical_bottom_pin, GPIO.IN)

#Motor Scanner Setup
stepPin1 = 2
dirPin1 = 3
enablePin1 = 18
sleepPin1 = 4

GPIO.setup(stepPin1, GPIO.OUT)
GPIO.setup(dirPin1, GPIO.OUT)
GPIO.setup(enablePin1, GPIO.OUT)
GPIO.setup(sleepPin1, GPIO.OUT)

GPIO.output(enablePin1, GPIO.LOW)
GPIO.output(sleepPin1, GPIO.LOW)
GPIO.output(dirPin1, GPIO.HIGH)


#Motor Horizontal
stepPin2 = 27
dirPin2 = 22
enablePin2 = 23
sleepPin2 = 17

GPIO.setup(stepPin2, GPIO.OUT)
GPIO.setup(dirPin2, GPIO.OUT)
GPIO.setup(enablePin2, GPIO.OUT)
GPIO.setup(sleepPin2, GPIO.OUT)

GPIO.output(enablePin2, GPIO.LOW)
GPIO.output(sleepPin2, GPIO.LOW)
GPIO.output(dirPin2, GPIO.HIGH)


#Motor Vertical
stepPin3 = 9
dirPin3 = 11
enablePin3 = 24
sleepPin3 = 10

GPIO.setup(stepPin3, GPIO.OUT)
GPIO.setup(dirPin3, GPIO.OUT)
GPIO.setup(enablePin3, GPIO.OUT)
GPIO.setup(sleepPin3, GPIO.OUT)

GPIO.output(enablePin3, GPIO.LOW)
GPIO.output(sleepPin3, GPIO.LOW)
GPIO.output(dirPin3, GPIO.HIGH)

delay = .005


#Moving Scanner Motor
def moveScannerUp(num):
    #step_count = input("Enter number of steps: ")
    step_count = num
    GPIO.output(dirPin1, GPIO.LOW)
    GPIO.output(sleepPin1, GPIO.HIGH)
    for x in range(step_count):
        GPIO.output(stepPin1, GPIO.HIGH)
        sleep(delay) 
        GPIO.output(stepPin1, GPIO.LOW)
        sleep(delay)
    GPIO.output(sleepPin1, GPIO.LOW)

def moveScannerDown(num):
    #step_count = input("Enter number of steps: ")
    step_count = num
    GPIO.output(dirPin1, GPIO.HIGH)
    GPIO.output(sleepPin1, GPIO.HIGH)
    for x in range(step_count):
        GPIO.output(stepPin1, GPIO.HIGH)
        sleep(delay) 
        GPIO.output(stepPin1, GPIO.LOW)
        sleep(delay)
    GPIO.output(sleepPin1, GPIO.LOW)


#Moving Horizontal Motor
def moveHorizontalUp(num):
    print"yola"
    #step_count = input("Enter number of steps: ")
    step_count = num
    GPIO.output(dirPin2, GPIO.LOW)
    GPIO.output(sleepPin2, GPIO.HIGH)
    for x in range(step_count):
        GPIO.output(stepPin2, GPIO.HIGH)
        sleep(delay) 
        GPIO.output(stepPin2, GPIO.LOW)
        sleep(delay)
    print('sleep pin 2')
    GPIO.output(sleepPin2, GPIO.LOW)

def moveHorizontalDown(num):
    #step_count = input("Enter number of steps: ")
    step_count = num
    GPIO.output(dirPin2, GPIO.HIGH)
    GPIO.output(sleepPin2, GPIO.HIGH)
    for x in range(step_count):
        GPIO.output(stepPin2, GPIO.HIGH)
        sleep(delay) 
        GPIO.output(stepPin2, GPIO.LOW)
        sleep(delay)
    GPIO.output(sleepPin2, GPIO.LOW)

#Moving vertical Motor
def moveVerticalUp(num):
    #step_count = input("Enter number of steps: ")
    step_count = num
    GPIO.output(dirPin3, GPIO.LOW)
    GPIO.output(sleepPin3, GPIO.HIGH)
    for x in range(step_count):
        GPIO.output(stepPin3, GPIO.HIGH)
        sleep(delay) 
        GPIO.output(stepPin3, GPIO.LOW)
        sleep(delay)
    GPIO.output(sleepPin3, GPIO.LOW)

def moveVerticalDown(num):
    #step_count = input("Enter number of steps: ")
    step_count = num
    GPIO.output(dirPin3, GPIO.HIGH)
    GPIO.output(sleepPin3, GPIO.HIGH)
    for x in range(step_count):
        GPIO.output(stepPin3, GPIO.HIGH)
        sleep(delay) 
        GPIO.output(stepPin3, GPIO.LOW)
        sleep(delay)
    GPIO.output(sleepPin3, GPIO.LOW)

'''def stop1(scanner_top_pin):
    print('1stopping the scanner when it reaches the top or bottom')
    GPIO.output(enablePin1, GPIO.HIGH) #disable driver
    '''
def stop2(scanner_bottom_pin):
    print('2stopping the scanner when it reaches the top or bottom')
    GPIO.output(enablePin1, GPIO.HIGH) #disable driver
    
def stop3(horizontal_top_pin):
    print('3stopping the scanner when it reaches the top or bottom')
    GPIO.output(enablePin1, GPIO.HIGH) #disable driver
    
def stop4(horizontal_bottom_pin):
    print('4stopping the scanner when it reaches the top or bottom')
    GPIO.output(enablePin1, GPIO.HIGH) #disable driver
    
def stop5(vertical_top_pin):
    print('5stopping the scanner when it reaches the top or bottom')
    GPIO.output(enablePin1, GPIO.HIGH) #disable driver
    
def stop6(vertical_bottom_pin):
    print('6stopping the scanner when it reaches the top or bottom')
    GPIO.output(enablePin1, GPIO.HIGH) #disable driver

#GPIO.add_event_detect(scanner_bottom_pin, GPIO.FALLING, callback=stop1, bouncetime=2000)
'''
GPIO.add_event_detect(scanner_top_pin, GPIO.FALLING, callback=stop2, bouncetime=2000)
GPIO.add_event_detect(horizontal_top_pin, GPIO.FALLING, callback=stop3, bouncetime=2000)
GPIO.add_event_detect(horizontal_bottom_pin, GPIO.FALLING, callback=stop4, bouncetime=2000)
GPIO.add_event_detect(vertical_top_pin, GPIO.FALLING, callback=stop5, bouncetime=2000)
GPIO.add_event_detect(vertical_bottom_pin, GPIO.FALLING, callback=stop6, bouncetime=2000)
#add interrupt and handler for start and reset button
'''
#the following method isn't needed once CS is integrated
#def reset(): #motor 
 #   moveScannerUp(10000)
  #  moveScannerDown(200) #release from pressing the switch
   # moveVerticalUp(10000)
   # moveVerticalDown(200) #release from pressing the switch
   # moveHorizontalLeft(10000)
   # moveHorizontalRight(200) #release from pressing the switch
"""
while(1):

    #command = raw_input("Enter command: ")
    #steps = input("Enter number of steps: ")
    command = ''
    steps = 0
    if command == "move scanner up":
       moveScannerUp(steps)

    if command == "move scanner down":
       moveScannerDown(steps)
       
    if command == "move vertical up":
       moveVerticalUp(steps)
       
    if command == "move vertical down":
       moveVerticalDown(steps)
       
    if command == "move horizontal up":
       moveHorizontalUp(steps)
       
    if command == "move horizontal down":
       moveHorizontalDown(steps)
    
    if(number ==0):
        moveScannerDown(50000)
    number = number+1
    data = serial.read()
    if data == '\r':
        print('in if')
        print(code)
        code = ''
    else:
        print('in else')
        code = code + data
        if (len(code) == 11):
        	code = code[1:]
        	        	
	# resetReader()
    if(len(code)>9 and dictionary[code[1:11]] == 'move forward'):
        if(direction == 0): moveVerticalUp(2000)
        elif(direction==1): moveHorizontalUp(2000)
        elif(direction==2): moveVerticalDown(2000)
        else: moveHorizontalDown(2000)
	
	# Write to a text file
f = open( 'file.py', 'w' )
f.write( 'dict = ' + repr(dict) + '\n' )
f.close()
		
	"""	
def resetReader():
	# wiringpi.digitalWrite(24, 0) # sets port 24 to 0 (0V, off)  #low
	sleep(10)                    # wait 10s  
	# wiringpi.digitalWrite(24, 1) # sets port 24 to 1 (3V3, on) #high
	sleep(10)                    # wait 10s  


