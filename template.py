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

# key press events
device = uinput.Device([
         uinput.KEY_X,
        ])

CAN_ID                 = 0x000 #can id 
CAN_DATA               = 0xFF #can data frame [0-7]

print('                                                                 ')
print('  ██████  █████  ███    ██  ██████  ███████ ██     ██  ██████    ')
print(' ██      ██   ██ ████   ██ ██  ████ ██      ██     ██ ██         ')
print(' ██      ███████ ██ ██  ██ ██ ██ ██ ███████ ██  █  ██ ██         ')
print(' ██      ██   ██ ██  ██ ██ ████  ██      ██ ██ ███ ██ ██         ')
print('  ██████ ██   ██ ██   ████  ██████  ███████  ███ ███   ██████    ')
print('                                                                 ')
print('')
print('github.com/jakka351/can0swc')
# Bring up can0 vcan0 slcan0 interface 
os.system("sudo /sbin/ip link set can0 up type can bitrate 125000")
time.sleep(0.1)
print('awaiting can frames:')

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native') #bus channel & type refer to python-can docs
except OSError:
    print('error message')
    GPIO.output(led,False)
    exit()

def can_rx_task():  # Recv can frames only with CAN_ID specified in variable
    while True:
        message = bus.recv()
        if message.arbitration_id == CAN_ID: #can id variable
            q.put(message)          # Put message into queue
            print('text')

q = queue.Queue()
rx = Thread(target = can_rx_task)
rx.start()
count = 0

# Main loop
try:
    while True:
        for i in range(1):
            while(q.empty() == True):       # Wait until there is a message
                pass
            message = q.get()
            if message.arbitration_id == CAN_ID and message.data[0] == CAN_DATA:
                device.emit_click(uinput.KEY_X) 
                print(message)
            
            elif message.arbitration_id != CAN_: 
                time.sleep(0.2) 
                print('')

except KeyboardInterrupt:
    exit()
