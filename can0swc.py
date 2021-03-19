#!/usr/bin/python3
# can0swc fg falcon swc-can adapter
# https://github.com/jakka351/can0swc | https://github.com/jakka351/FG-Falcon 
import time
import uinput
import queue
from threading import Thread
import can
import os
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
##########################
SWC                    = 0x2F2              #arbitration id
ICC                    = 0x2FC              #arbitration id 
SWC_SEEK               = (0x08, 0x09, 0x0C)
SWC_VOLUP              = (0x10, 0x11, 0x14)
SWC_VOLDOWN            = (0x18, 0x19, 0x1C)
SWC_PHONE              = (0x61, 0x65, 0x68)
ICC_VOLUP              = 0x41 
ICC_VOLDOWN            = 0x81 
ICC_NEXT               = 0x04 
ICC_PREV               = 0x08 
ICC_EJECT              = 0x80 
ICC_LOAD               = 0x40 
CAN_SWC                =   [{"can_id": 0x2f2, "can_mask": 0x1fffffff, "extended": False},
                            {"can_id": 0x2fc, "can_mask": 0x1fffffff, "extended": False}]

#    os.systen("sudo modprobe uinput")
#    os.system("sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 1000")
#    os.system("sudo /sbin/ifconfig can0 up txqueuelen 100")

try:
    bus = can.Bus(bustype='socketcan_native', 
             channel="can0", 
             bitrate="125000", 
             can_filters=CAN_SWC)
except OSError:
    print('        can0 interface not found. check wiring and config.')
    sys.exit()


def can0swc():
     while True:
        message = bus.recv(timeout=None)
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
                os.system("sudo ~/openauto/bin/autoapp")                
            elif message.data[1] == ICC_LOAD:
                os.system("sudo systemctl start dash.service")
                os.system("sudo systemctl start can0swc.service")                
            elif message.data[1] == ICC_EJECT:
                os.system("sudo systemctl stop dash.service")
                os.system("sudo systemctl stop can0swc.service")
        else:
            pass

############################
# can0swc
############################
try:
    rx = Thread(target = can0swc)
    rx.start()
except KeyboardInterrupt:
    sys.exit()
except Exception:
    traceback.print_exc(file=sys.stdout)
    sys.exit()
except OSError:
     sys.exit()


