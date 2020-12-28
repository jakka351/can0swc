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
    #android auto keyboard buttons
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

SWC                    = 0x2F2 #can id 
SWC_SEEK               = 0x09 #frame 8 2F2 # [02] [E3] [06] [4E] [08] [1D] [00] [09]
SWC_VOLUP              = 0x11 #frame 8 2F2 # 02 E3 06 4E 08 1D 00 11
SWC_VOLDOWN            = 0x19 #frame 8 2F2 # 02 E3 06 4E 08 1D 00 19
SWC_PHONE              = 0x68 #frame 7 2F2 # 02 E3 06 4E 08 1D 68 00     

print('                                                                 ')
print('  ██████  █████  ███    ██  ██████  ███████ ██     ██  ██████    ')
print(' ██      ██   ██ ████   ██ ██  ████ ██      ██     ██ ██         ')
print(' ██      ███████ ██ ██  ██ ██ ██ ██ ███████ ██  █  ██ ██         ')
print(' ██      ██   ██ ██  ██ ██ ████  ██      ██ ██ ███ ██ ██         ')
print('  ██████ ██   ██ ██   ████  ██████  ███████  ███ ███   ██████    ')
print('                                                                 ')
print('fg-falcon steering wheel media controls')
print('github.com/jakka351/FG-Falcon')
# Bring up can0 interface at 500kbps
#os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
#ford ms-can is 125kbs
#os.system("sudo /sbin/ip link set can0 up type can bitrate 125000")
time.sleep(0.1)
print('awaiting can frames:')

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native') #bus channel & type refer to python-can docs
except OSError:
    print('can0swc cannot find can interface. check wiring and config')
    GPIO.output(led,False)
    exit()

def can_rx_task():  # Recv can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == SWC: #CAN_ID variable
            q.put(message)          # Put message into queue
            print('filtering can_id 0x2F2')

q = queue.Queue()
rx = Thread(target = can_rx_task)
rx.start()
#c =''
count = 0

# Main loop
try:
    while True:
        for i in range(1):
            while(q.empty() == True):       # Wait until there is a message
                pass
            message = q.get()
            if message.arbitration_id == SWC and message.data[7] == SWC_SEEK:
                device.emit_click(uinput.KEY_N) 
                print('can0swc:seek')
                print(message)
            if message.arbitration_id == SWC and message.data[7] == SWC_VOLUP:
                device.emit_click(uinput.KEY_VOLUMEUP)
                print('can0swc:volup')
                print(message)
            if message.arbitration_id == SWC and message.data[7] == SWC_VOLDOWN:
                device.emit_click(uinput.KEY_VOLUMEDOWN)
                print('can0swc:voldown')
                print(message)
            if message.arbitration_id == SWC and message.data[6] == SWC_PHONE:
                device.emit_click(uinput.KEY_P)
                print('can0swc:phone')
                print(message)
            elif message.arbitration_id != SWC: 
                time.sleep(0.2) 
                print('nothing')

except KeyboardInterrupt:
    exit()

