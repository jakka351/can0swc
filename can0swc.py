#!/usr/bin/python3
#can0swc fg falcon swc-can adapter
#https://github.com/jakka351/FG-Falcon | https://github.com/jakka351/can0swc
import can
import time
import os
import uinput
import queue
from threading import Thread
import sys, traceback
############################
# Define Keypresses
############################
device = uinput.Device([

        uinput.KEY_N,
        uinput.KEY_VOLUMEUP,
        uinput.KEY_VOLUMEDOWN,
        uinput.KEY_C,
        uinput.KEY_W,
        ])
############################
# CAN Id's
############################
SWC                    = 0x2F2              #id 751
ICC                    = 0x2FC              #id 764
############################
# SWC Button CAN Data
############################
SWC_SEEK               = (0x08, 0x09, 0x0C)  # [7]
SWC_VOLUP              = (0x10, 0x11, 0x14)  # [7]
SWC_VOLDOWN            = (0x18, 0x19, 0x1C)  # [7]
SWC_PHONE              = (0x61, 0x65, 0x68)  # [6]
############################
# ICC Button CAN Data
############################
ICC_VOLUP              = 0x41 #[3]
ICC_VOLDOWN            = 0x81 #[3]
ICC_NEXT               = 0x04 #[0]
ICC_PREV               = 0x08 #[0]
ICC_EJECT              = 0x80 #[1]
ICC_LOAD               = 0x40 #[1]

print('         ██████  █████  ███    ██  ██████  ███████ ██     ██  ██████    ')
time.sleep(0.15)
print('        ██      ██   ██ ████   ██ ██  ████ ██      ██     ██ ██         ')
time.sleep(0.15)
print('        ██      ███████ ██ ██  ██ ██ ██ ██ ███████ ██  █  ██ ██         ')
time.sleep(0.15)
print('        ██      ██   ██ ██  ██ ██ ████  ██      ██ ██ ███ ██ ██         ')
time.sleep(0.15)
print('         ██████ ██   ██ ██   ████  ██████  ███████  ███ ███   ██████    ')
time.sleep(0.15)
print('      ┌─┐┌─┐┌┐┌┌┬┐┬─┐┌─┐┬  ┬  ┌─┐┬─┐  ┌─┐┬─┐┌─┐┌─┐  ┌┐┌┌─┐┌┬┐┬ ┬┌─┐┬─┐┬┌─  ')
time.sleep(0.15)
print('      │  │ ││││ │ ├┬┘│ ││  │  ├┤ ├┬┘  ├─┤├┬┘├┤ ├─┤  │││├┤  │ ││││ │├┬┘├┴┐  ')
time.sleep(0.15)
print('      └─┘└─┘┘└┘ ┴ ┴└─└─┘┴─┘┴─┘└─┘┴└─  ┴ ┴┴└─└─┘┴ ┴  ┘└┘└─┘ ┴ └┴┘└─┘┴└─┴ ┴  ')

##########################
#midspeed-can 
##########################
os.system("sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 1000")
os.system("sudo /sbin/ifconfig can0 up txqueuelen 100")
os.system("sudo modprobe uinput")  
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    sys.exit()

############################
# CAN Rx
############################
def can_rx_task():                                               # rx can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == SWC:                        # CAN_ID variable
            q.put(message)

        if message.arbitration_id == ICC:                        # CAN_ID variable
            q.put(message)

############################
# Rx Queue
############################
q = queue.Queue()
rx = Thread(target = can_rx_task)
rx.start()
c = ''
count = 0
############################
# Main Loop
############################
try:
    while True:
        for i in range(8):
            while(q.empty() == True):       # Wait until there is a message
                pass
            message = q.get()
            c = '{0:f},{1:d},'.format(message.timestamp,count)
            ###########################
            #Steering Wheel Buttons
            ###########################
            if message.arbitration_id == SWC:
                if message.data[7] == SWC_SEEK[0]:
                    device.emit_click(uinput.KEY_N)  #next song
                    time.sleep(0.1)
                elif message.data[7] == SWC_SEEK[1]:
                    device.emit_click(uinput.KEY_N)  #next song
                    time.sleep(0.1)
                elif message.data[7] == SWC_SEEK[2]:
                    device.emit_click(uinput.KEY_N)  #next song
                    time.sleep(0.1)
                elif message.data[7] == SWC_VOLUP[0]:
                    device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                    time.sleep(0.01)
                elif message.data[7] == SWC_VOLUP[1]:
                    device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                    time.sleep(0.01)
                elif message.data[7] == SWC_VOLUP[2]:
                    device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                    time.sleep(0.01)
                elif message.data[7] == SWC_VOLDOWN[0]:
                    device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                    time.sleep(0.01)
                elif message.data[7] == SWC_VOLDOWN[1]:
                    device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                    time.sleep(0.01)
                elif message.data[7] == SWC_VOLDOWN[2]:
                    device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                    time.sleep(0.01)
                if message.data[6] == SWC_PHONE[0]:
                    device.emit_click(uinput.KEY_W) #opendash cycle pages
                    time.sleep(1.0)
                elif message.data[6] == SWC_PHONE[1]:
                    device.emit_click(uinput.KEY_W) #opendash cycle pages
                    time.sleep(1.0)
                elif message.data[6] == SWC_PHONE[2]:
                    device.emit_click(uinput.KEY_W) #opendash cycle pages
                    time.sleep(1.0)
                ############################
                #ICC Buttons
                ############################
            if message.arbitration_id == ICC:
                if message.data[3] == ICC_VOLUP:
                    device.emit_click(uinput.KEY_VOLUMEUP)
                elif message.data[3] == ICC_VOLDOWN:
                    device.emit_click(uinput.KEY_VOLUMEDOWN) 
                elif message.data[0] == ICC_NEXT:
                    device.emit_click(uinput.KEY_N)
                elif message.data[0] == ICC_PREV:
                    device.emit_click(uinput.KEY_C)
                elif message.data[1] == ICC_LOAD:
                    os.system("sudo systemctl start dash.service")
                elif message.data[1] == ICC_EJECT:
                    os.system("sudo systemctl stop dash.service")
            else:
                pass

except KeyboardInterrupt:
    sys.exit()
except Exception:
    traceback.print_exc(file=sys.stdout)
    sys.exit()
except OSError:
    sys.exit()

############################
# can0swc
############################
    
