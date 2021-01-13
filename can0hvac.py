#!/usr/bin/python3
#// Ford FG can0hvac
#FG Falcon can-frames used in this example
#https://jakka351.github.io/FG-Falcon/
import RPi.GPIO as GPIO #GPIO Library for LED on GPIO22 on PiCAN2 board
import can 
import time
import os
import uinput #keypress lib for version 1
import queue
from threading import Thread

HVAC                    =  0x353     #can id 851 
HVAC_off                =  0xAB      #  [5] A 129 0 0 34 [171] 0 0    All Off
HVAC_VENTSTATUS         =  0          #Vent tatus 851 x1
HVAC_TEMP               =  0                   #851 x4
HVAC_OUT                =  0                #Outside Temp 851 x5
HVAC_FANSPEED           =  0               #Fan speed 851 x8


try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native') #bus channel & type refer to python-can docs
except OSError:
    print('can0swc cannot start can0 or can1 interface: can0swc cant get it up: check wiring and config')
    GPIO.output(led,False)
    exit()

def can_rx_task():  # Recv can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == HVAC: #CAN_ID variable
            q.put(message)          # Put message into queue
            print('')
q = queue.Queue()
rx = Thread(target = can_rx_task)
rx.start()
c = ''
count = 0

time.sleep(0.1)

# Main loop
try:
    while True:
        for i in range(1):
            while(q.empty() == True):       # Wait until there is a message
                pass
            message = q.get()

            c = '{0:f},{g:d},'.format(message.timestamp,count) 
            if message.arbitration_id == HVAC and message.data[0] != HVAC_TEMP:
                print('AC Temp:')
                print(message.data[3] / 2)
                time.sleep(1.0)

            if message.arbitration_id == HVAC and message.data[0] != HVAC_OUT:
                print('Outside Temp:')
                print(message.data[4])
                time.sleep(1.0)

            if message.arbitration_id == HVAC and message.data[0] != HVAC_FANSPEED:
                print('Fan Speed:')
                print(message.data[7])
                time.sleep(1.0)

            if message.arbitration_id == HVAC and message.data[0] != HVAC_VENTSTATUS:
                print('Vent Status:')
                print(message.data[0])
                if message.data == 1
                 print('Face Only')
                if message.data == 2
                 print('Feet Only')
                if message.data == 3
                 print('Face & Feet')
                if message.data == 4
                 print('Windshield')
                time.sleep(1.0)

            if message.arbitration_id == HVAC and message.data[5] == HVAC_off:
                print('AC Off')
                time.sleep(1.0)

            #if message.arbitration_id == HVAC:
             #   print('')
             #   time.sleep(1.0)

except KeyboardInterrupt:
    exit()
