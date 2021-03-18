#!/usr/bin/python3
# can0swc fg falcon swc-can adapter
# https://github.com/jakka351/can0swc | https://github.com/jakka351/FG-Falcon 
import time
import os
import uinput
import queue
from threading import Thread
import can
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
################################
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

#os.system("sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 1000")
#os.system("sudo /sbin/ifconfig can0 up txqueuelen 100")

##########################
############################
# CAN Id's
############################
SWC                    = 0x2F2              #id 751
ICC                    = 0x2FC              #id 764
############################
# SWC Button CAN Data
############################
SWC_SEEK               = (0x08, 0x09, 0x0C)
SWC_VOLUP              = (0x10, 0x11, 0x14)
SWC_VOLDOWN            = (0x18, 0x19, 0x1C)
SWC_PHONE              = (0x61, 0x65, 0x68)
############################
# ICC Button CAN Data
############################
ICC_VOLUP              = 0x41 #[3]
ICC_VOLDOWN            = 0x81 #[3]
ICC_NEXT               = 0x04 #[0]
ICC_PREV               = 0x08 #[0]
ICC_EJECT              = 0x80 #[1]
ICC_LOAD               = 0x40 #[1]

can_filters =   [{"can_id": 0x2f2, "can_mask": 0x1fffffff, "extended": False},
                {"can_id": 0x2fc, "can_mask": 0x1fffffff, "extended": False}]
bus = can.Bus(
            interface="socketcan",
            channel="vcan0",
            bitrate="125000",
            can_filters=can_filters
            )

def can0swc():
    while True:
        message = bus.recv()
        #message = bus.recv.data[6](timeout=None)
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
            elif message.data[6] == SWC_PHONE[0]:
                device.emit_click(uinput.KEY_W) #opendash cycle pages
                time.sleep(1.0)
            elif message.data[6] == SWC_PHONE[1]:
                device.emit_click(uinput.KEY_W) #opendash cycle pages
                time.sleep(1.0)
            elif message.data[6] == SWC_PHONE[2]:
                device.emit_click(uinput.KEY_W) #opendash cycle pages
                time.sleep(1.0)
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
                os.system("sudo systemctl start can0swc.service")                
            elif message.data[1] == ICC_EJECT:
                os.system("sudo systemctl stop dash.service")
                os.system("sudo systemctl stop can0swc.service")                
        #if can.CanError:
         #   sys.exit()
        else:
            pass

rx = Thread(target = can0swc)
rx.start()
############################
# can0swc
############################
