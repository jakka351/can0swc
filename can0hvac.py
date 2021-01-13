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

HVAC                    =  0x353 #can id 851 
HVAC_off                =  0xAB #  [5] A 129 0 0 34 [171] 0 0    All Off
#HVAC_vent               =  #[1] by 
HVAC_vent_face          =  16 #[1] by 16
HVAC_vent_feet          =  8 #[1] by 8
HVAC_vent_window0       =  4 #[1] by 4
HVAC_vent_window1       =  2 #[1] by 2
#HVAC_cabin_open         =  #[1] by 32
#HVAC_cabin_closed       =  #[1] by 64
#HVAC_demisterfront      = 
#HVAC_demisterrear       = 
#HVAC_fan_autooff        = #[1] by 1
#HVAC_actemp             = message.data[3] #[4] = AC temp * 2
#HVAC_outside            = message.data[4] #[5]
#HVAC_fanspeed           = message.data[7] #[8] 0-10 0=fan off 10=full speed fan
#HVAC_fanspeedauto       = 0x # [8] +128
HVAC_fan0  =  0x00 #  [7] 129 0 0 34 X Y 0  Fan Only - Off   
HVAC_fan1  =  0x01 #  [7] 129 0 0 34 X Y 1  Fan Only - Speed 1
HVAC_fan2  =  0x02 #  [7] 129 0 0 34 X Y 2  Fan Only - Speed 2
HVAC_fan3  =  0x03 #  [7] 129 0 0 34 X Y 3  Fan Only - Speed 3
HVAC_fan4  =  0x04 #  [7] 129 0 0 34 X Y 4  Fan Only - Speed 4
HVAC_fan5  =  0x05 #  [7] 129 0 0 34 X Y 5  Fan Only - Speed 5
HVAC_fan6  =  0x06 #  [7] 129 0 0 34 X Y 6  Fan Only - Speed 6
HVAC_fan7  =  0x07 #  [7] 129 0 0 34 X Y 7  Fan Only - Speed 7
HVAC_fan8  =  0x08 #  [7] 129 0 0 34 X Y 8  Fan Only - Speed 8
HVAC_fan9  =  0x09 #  [7] 129 0 0 34 X Y 9  Fan Only - Speed 9
HVAC_fan10 =  0x10 #  [7] 129 0 0 34 X Y 10 Fan Only - Speed 10
#A 129 0 0 34 X Y Z  Y Increases when Fan On - Possibly RPM
HVAC_auto  =  0x90 #  [7] 2 129 0 0 34 X Y [144]    Full Auto
HVAC_FVCC  =  0x4B #  [0] A = 75  Feet Vents, Close Cabin
HVAC_FVOC  =  0x2B #  [0] A = 43  Feet Vents, Open Cabin
HVAC_WFOC  =  0x2F #  [0] A = 47  Window and Feet Vents, Open Cabin
HVAC_WFCC  =  0x4F #  [0] A = 79  Window and Feet Vents, Close Cabin
#HVAC_      =  0x   #   [] A = 91  Face, Feet, Close Cabin
#HVAC_      =  0x   #   [c] A = 59  Face, Feet, Open Cabin
#HVAC_      =  0x   #  [c] A = 51  Face, Open Cabin
#HVAC_      =  0x   #  [c] A = 83  Face, Close Cabin
#HVAC_      =  0x   # [c] A = 39  Window, Manual Fan
#HVAC_      =  0x   # [] A = 38  Window, Auto Fan
#HVAC_      =  0x   # [] A = 131 A/C Off, Open Cabin
#HVAC_      =  0x   # [] A = 139 A/C Off, Feet Vents, Open Cabin
#HVAC_      =  0x   # [] A = 143 A/C Off, Feet and Window Vents, Open Cabin
#HVAC_      =  0x   # [] A = 155 A/C Off, Feet and Face Vents, Open Cabin
#HVAC_      =  0x   # [] A = 166 A/C Off, Window Vents, Open Cabin
#HVAC_      =  0x   # [] A = 167 A/C Off, Manual Fan, Open Cabin
#HVAC_      =  0x   # [] A = 195 A/C Off, Close Cabin
#HVAC_      =  0x   # [] A = 203 A/C Off, Feet Vents, Close Cabin
#HVAC_      =  0x   # [] A = 207 A/C Off, Feet and Window Vents, Close Cabin
#HVAC_      =  0x   # [] A = 219 A/C Off, Feet and Face Vents, Close Cabin
#HVAC_      =  0x   # [] A = 67  Auto, Close Cabin
#HVAC_      =  0x   # [] A = 35  Auto, Open Cabin
#3 129 0 0 34 X Y 145    Auto with Fan Speed Set (1)
#3 129 0 0 34 X Y 154    Auto with Fan Speed Set (10 / Full)
#67 129 0 0 34 X Y Z Auto, Close Cabin
#35 129 0 0 34 X Y Z Auto, Open Cabin
#51 129 0 0 34 X Y Z Fan Only

#HVAC_actemp   =  message.data[3]    # [] A 129 0 38 34 X Y Z Temp Set to 19 (D = Temp * 2)

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
           if message.arbitration_id == HVAC:
                print('AC Temp:')
                print(message.data[3] / 2)
                time.sleep(1.0)

            if message.arbitration_id == HVAC:
                print('Outside Temp:')
                print(message.data[4])
                time.sleep(1.0)

            if message.arbitration_id == HVAC:
                print('Fan Speed:')
                print(message.data[7])
                time.sleep(1.0)

            if message.arbitration_id == HVAC and message.data[5] == HVAC_off:
                print('AC Off')
                time.sleep(1.0)

            #if message.arbitration_id == HVAC:
             #   print('')
             #   time.sleep(1.0)

except KeyboardInterrupt:
    exit()
