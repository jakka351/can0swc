#!/usr/bin/python3
#can0swc
#FG Falcon can-frames used in this example
#https://jakka351.github.io/FG-Falcon/
import RPi.GPIO as GPIO #GPIO Library for LED on GPIO22 on PiCAN2 board
import can 
import time
import os
import uinput #keypress lib
import queue
from threading import Thread

led = 22 #GPIO22 on the PiCAN2 Board has a LED fitted
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,True)

# simulated keypresses setup for openauto
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

# add full can data
SWC_SEEK               = 0x09 #frame 8
SWC_SEEKHOLD           = 0x09 #frame 8
SWC_VOLUP              = 0x11 #frame 8
SWC_VOLDOWN            = 0x19 #frame 8
SWC_PHONE              = 0x68 #frame 7      
SWC                    = 0x2F2 #can id

print('can0swc:')
print('\n\rcan0swc:fg-falcon steering wheel media controls')
print('can0swc:')
print('can0swc:github.com/jakka351/FG-Falcon:github.com/jakka351/can0swc')
print('can0swc:bringing up can0 can1 interfaces:')
print('can0swc:can0 interface up:500kbps')
print('can0swc:starting...')

# Bring up can0 interface at 500kbps
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
#os.system("sudo /sbin/ip link set can1 up type can bitrate 125000")
time.sleep(0.1)
print('can0swc:can0 up:can1 down')
print('can0swc:active')
print('can0swc:ready')
print('can0swc:awaiting can frames:')
print('can0swc:		')

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native') #bus channel & type refer to python-can docs
except OSError:
    print('can0swc cannot start can0 or can1 interface: can0swc cant get it up: check wiring and config')
    GPIO.output(led,False)
    exit()

def can_rx_task():  # Recv can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == SWC: #CAN_ID variable
            q.put(message)          # Put message into queue
            print('can0swc:filtering canid 0x2F2')
            print('can0swc:can frame queued')
            print('can0swc:checking:	')
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
            if message.arbitration_id == SWC and message.data[7] == SWC_SEEK:
                device.emit_click(uinput.KEY_NEXTSONG) # Next Track
                print('can0swc:match:seek')

            if message.arbitration_id == SWC and message.data[7] == SWC_VOLUP:
                device.emit_click(uinput.KEY_VOLUMEUP) # 
                print('can0swc:match:volup')

            if message.arbitration_id == SWC and message.data[7] == SWC_VOLDOWN:
                device.emit_click(uinput.KEY_VOLUMEDOWN) #
                print('can0swc:match:voldown')

            if message.arbitration_id == SWC and message.data[6] == SWC_PHONE:
                device.emit_click(uinput.KEY_M) # 
                print('can0swc:match:phone')

       #     if message.arbitration_id == SWC and message.data[7] == SWC_SEEKHOLD:
        #        device.emit_click(uinput.KEY_NEXTSONG) # 
         #       print('Seekhold!')                             

#      print('FG Falcon')

except KeyboardInterrupt:
    #Catch keyboard interrupt
    GPIO.output(led,True)
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rcan0 down can1 down')
