#!/usr/bin/python3
#can0swc
#FG Falcon can-frames used in this example
#https://jakka351.github.io/FG-Falcon/
import RPi.GPIO as GPIO                     # gpio library for LED on GPIO22 on PiCAN2 board
import can 
import time
import os
import uinput                               # keypress library 
import queue
from threading import Thread
import sys, traceback

############################
# gpio setup
led = 22                                    # gpio on the pican2 board has LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,True)
############################


############################
# define keys
device = uinput.Device([
                                            # android auto keyboard buttons
        uinput.KEY_N, #Next Track
#        uinput.KEY_PREVIOUSSONG,
#        uinput.KEY_PLAYPAUSE,
        uinput.KEY_VOLUMEUP, #Volup
        uinput.KEY_VOLUMEDOWN, #Voldown
        uinput.KEY_P, #Phone Button
#        uinput.KEY_M, #Google Voice
#        uinput.KEY_O, #Call End
#        uinput.KEY_H, #Home
#        uinput.KEY_X, #Play
#        uinput.KEY_C, #Pause
#        uinput.KEY_B, #Toggle Play    
#        uinput.KEY_ESC, #ESC       
#        uinput.KEY_ENTER, #Enter
                                            #opendash shortcuts
        uinput.KEY_Q, #AA page
        uinput.KEY_W, #Vehicle Page
        uinput.KEY_E, #Media Page
        uinput.KEY_R, #Launcher Page
        uinput.KEY_T, #Camera Page
        uinput.KEY_Y, #Toggle Dark Mode
        uinput.KEY_K, #U vol
        uinput.KEY_L, #L vol
        ])
############################

############################
# define CAN identifiers
SWC                    = 0x2F2              #can id 
############################

############################
# Define CAN frame data
SWC_SEEK               = 0x09               #frame 8 2F2 # [02] [E3] [06] [4E] [08] [1D] [00] [09]
SWC_VOLUP              = 0x11               #frame 8 2F2 # 02 E3 06 4E 08 1D 00 11
SWC_VOLDOWN            = 0x19               #frame 8 2F2 # 02 E3 06 4E 08 1D 00 19
SWC_PHONE              = 0x68               #frame 7 2F2 # 02 E3 06 4E 08 1D 68 00     
############################

############################
# print 
print('=================================================================')
print('                                                                 ')
print('  ██████  █████  ███    ██  ██████  ███████ ██     ██  ██████    ')
print(' ██      ██   ██ ████   ██ ██  ████ ██      ██     ██ ██         ')
print(' ██      ███████ ██ ██  ██ ██ ██ ██ ███████ ██  █  ██ ██         ')
print(' ██      ██   ██ ██  ██ ██ ████  ██      ██ ██ ███ ██ ██         ')
print('  ██████ ██   ██ ██   ████  ██████  ███████  ███ ███   ██████    ')
print('                                                                 ')
print('fg-falcon steering wheel media controls')
print('github.com/jakka351/FG-Falcon')
############################

############################
# can0 up @ 125kbps
#                                                               #fg ms-can is 125kbps hs-can is 500kbps
os.system("sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 100 loopback on")
os.system("sudo /sbin/ifconfig can0 up txqueuelen 65535")
############################

############################
# sleep
time.sleep(0.1)
print('can0swc:')
time.sleep(0.1)
############################


############################
# socketcan parameters
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native') 
    print('socketcan configured...awaiting can frames.....')     # channel = interface, bustype = socketcan 
except OSError:
    print('can0swc cannot find can interface. check wiring and config')
    GPIO.output(led,False)
    exit()
############################

############################
# can rx 
def can_rx_task():                                               # rx can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == SWC:                        # CAN_ID variable
            q.put(message)                                       # put message into queue
            print('can0swc:filtering can_id 0x2F2')
############################

############################
# rxqueue vars
q = queue.Queue()
rx = Thread(target = can_rx_task)
rx.start()
############################

############################
# main loop
try:
    while(q.empty() == True):                                     # wait until there is a message
     pass
    message = q.get()
     if message.arbitration_id == SWC and message.data[7] == SWC_SEEK:
      device.emit_click(uinput.KEY_N) 
      device.emit_click(uinput.KEY_Q) 
      print('can0swc:seek')
      print(message)

     if message.arbitration_id == SWC and message.data[7] == SWC_VOLUP:
      device.emit_click(uinput.KEY_VOLUMEUP)
      device.emit_click(uinput.KEY_L) 
      print('can0swc:volup')
      print(message)

     if message.arbitration_id == SWC and message.data[7] == SWC_VOLDOWN:
      device.emit_click(uinput.KEY_VOLUMEDOWN)
      device.emit_click(uinput.KEY_K) 
      print('can0swc:voldown')
      print(message)

     if message.arbitration_id == SWC and message.data[6] == SWC_PHONE:
      device.emit_click(uinput.KEY_W)
      device.emit_click(uinput.KEY_P)
      print('can0swc:phone')
      print(message)

    elif message.arbitration_id != SWC and message.data[7] != SWC_SEEK:
      print('0x2f2 ID')
      time.sleep(0.5) 
      print('no data')
############################

############################
# end
except KeyboardInterrupt:
    exit()
except Exception:
    traceback.print_exc(file=sys.stdout)
    exit()
except OSError:
    exit()   
############################
# can0swc
############################

