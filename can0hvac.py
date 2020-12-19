#!/usr/bin/python3
#can0hvac
#FG Falcon can-frames used in this example
#https://jakka351.github.io/FG-Falcon/
import RPi.GPIO as GPIO #GPIO Library for LED on GPIO22 on PiCAN2 board
import can 
import time
import os
import uinput #keypress lib for version 1
import keyboard # https://github.com/jakka351/keyboard (pip install keyboard)
import queue
from threading import Thread

led = 22 #GPIO22 on the PiCAN2 Board has a LED fitted
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,True)

# simulated keypresses setup for openauto # modify this segment to define keyboard keys
device = uinput.Device([
        uinput.KEY_NEXTSONG,
        uinput.KEY_PREVIOUSSONG,
        uinput.KEY_PLAYPAUSE,
        uinput.KEY_VOLUMEUP,
        uinput.KEY_VOLUMEDOWN,
        uinput.KEY_MUTE,
        uinput.KEY_M,
        uinput.KEY_O,
])

# modify this segment to define can frame data segment to listen for
HVAC                     = 0x2F2 #can id
HVAC_                    = 0 #full can frame needed here
HVAC_                    = 
HVAC_                    = 
HVAC_                    = 
HVAC_                    = 
HVAC_                    = 
HVAC_                    = 
HVAC_                    = 

print('can0hvac:')
print('\n\rcan0hvac:fg-falcon air-conditioner status & sender')
print('can0hvac:')
print('can0swc:github.com/jakka351/FG-Falcon:github.com/jakka351/can0swc')
print('can0hvac:bringing up can0 can1 interfaces:')
print('can0hvac:can0 interface up:500kbps')
print('can0hvac:starting...')
GPIO.output(led, True)
time.sleep(0.1)
GPIO.output(led,False)
time.sleep(0.1)

# Bring up can0 interface at 500kbps
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
#ford ms-can is 125kbs
#os.system("sudo /sbin/ip link set can1 up type can bitrate 125000")
time.sleep(0.1)
print('can0hvac:can0 up')
print('can0hvac:active')
print('can0hvac:ready')
print('can0hvac:awaiting can frames:')
print('can0hvac:		')
GPIO.output(led, True)
time.sleep(0.1)
GPIO.output(led,False)
time.sleep(0.1)

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native') #bus channel & type refer to python-can docs
except OSError:
    print('can0hvac cannot start can0 or can1 interface: can0hvac cant keep it's cool: check wiring and config')
    GPIO.output(led,False)
    exit()

def can_rx_task():  # Recv can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == HVAC: #CAN_ID variable
            q.put(message)          # Put message into queue
            print('can0hvac:filtering canid 0xFFF') #
            print('can0hvac:can frame queued')
            print('can0hvac:checking:	')
q = queue.Queue()
rx = Thread(target = can_rx_task)
rx.start()
c = ''
count = 0

# Main loop
try:
    while True:
        for i in range(1):
            while(q.empty() == True):       # Wait until there is a message
                pass
            message = q.get()

            c = '{0:f},{1:d},'.format(message.timestamp,count)
            if message.arbitration_id == HVAC and message.data[x] == HVAC_x: #can frame data 
                do.some(thing) # comment goes here about stuff
                print('can0hvac:') 

#      print('FG Falcon')

except KeyboardInterrupt:
    #Catch keyboard interrupt
    GPIO.output(led,True)
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rcan0 down can1 down')

    #can frame data for hvac
