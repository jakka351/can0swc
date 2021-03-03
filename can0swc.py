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
        uinput.KEY_P,
        uinput.KEY_M,
        uinput.KEY_O,
        uinput.KEY_H,
        uinput.KEY_X,
        uinput.KEY_C,
        uinput.KEY_B,
        uinput.KEY_ESC,
        uinput.KEY_ENTER,
        uinput.KEY_Q,
        uinput.KEY_W,
        uinput.KEY_E,
        uinput.KEY_R,
        uinput.KEY_T,
        uinput.KEY_Y,
        uinput.KEY_K,
        uinput.KEY_L

        ])
############################
# CAN Id's
############################
SWC                    = 0x2F2              #id 751
SWC2                   = 0x2EC              #id 748
ICC                    = 0x2FC              #id 764
BEM                    = 0x307              #id
############################
# SWC Button CAN Data
############################
SWC_SEEK               = (0x08, 0x09, 0x0C)  # [7]
SWC_VOLUP              = (0x10, 0x11, 0x14)  # [7]
SWC_VOLDOWN            = (0x18, 0x19, 0x1C)  # [7]
SWC_PHONE              = (0x61,0x65,0x68) #[6]
SWC_MODE               = (0x10,0x12)
############################
# ICC Button CAN Data
############################
ICC_VOLUP              = 0x41 #[3]
ICC_VOLDOWN            = 0x81 #[3]
ICC_NEXT               = 0x04 #[0]
ICC_PREV               = 0x08 #[0]
#ICC_PWR                = 0x00
ICC_EJECT              = 0x80 #[1]
ICC_LOAD               = 0x40 #[1]
ICC_MENU               = 0x10 #[0]
#ICC_BACK               = 0x00
ICC_OK                 = 0x21 #[2]
############################
# BEM Button CAN Data
############################
UNLOCK                 = 0x84  #[3]
LOCK                   = 0xC0  #[3]
DSC                    = 0x90  #[3]
LIGHT                  = 0xA0  #[3]
HAZARD                 = (0x01, 0x80) #[2] [3]
############################
# pointless intro text
############################
time.sleep(0.05)
print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')
print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')
time.sleep(0.1)
print("      _____              _____     _                _____ ")
time.sleep(0.05)
print("       /  '        /      /  '    //                 /  ' ")
time.sleep(0.05)
print("    ,-/-,__ __  __/    ,-/-,__.  // _. __ ____    ,-/-,_, ")
time.sleep(0.05)
print("   (_/  (_)/ (_(_/_   (_/  (_/|_</_(__(_)/ / <_  (_/  (_)_")
time.sleep(0.05)
print("                                                       /| ")
time.sleep(0.05)
print("                                                      |/  ")
time.sleep(0.15)
print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')
time.sleep(0.15)
time.sleep(0.15)
print('                                                                 ')
time.sleep(0.15)
print('       ██████  █████  ███    ██  ██████  ███████ ██     ██  ██████    ')
time.sleep(0.15)
print('      ██      ██   ██ ████   ██ ██  ████ ██      ██     ██ ██         ')
time.sleep(0.15)
print('      ██      ███████ ██ ██  ██ ██ ██ ██ ███████ ██  █  ██ ██         ')
time.sleep(0.15)
print('      ██      ██   ██ ██  ██ ██ ████  ██      ██ ██ ███ ██ ██         ')
time.sleep(0.15)
print('       ██████ ██   ██ ██   ████  ██████  ███████  ███ ███   ██████    ')
time.sleep(0.15)
print('         ')
print('               https://github.com/jakka351/fg-falcon')
time.sleep(0.15)
print('      ┌─┐┌─┐┌┐┌┌┬┐┬─┐┌─┐┬  ┬  ┌─┐┬─┐  ┌─┐┬─┐┌─┐┌─┐  ┌┐┌┌─┐┌┬┐┬ ┬┌─┐┬─┐┬┌─  ')
time.sleep(0.15)
print('      │  │ ││││ │ ├┬┘│ ││  │  ├┤ ├┬┘  ├─┤├┬┘├┤ ├─┤  │││├┤  │ ││││ │├┬┘├┴┐  ')
time.sleep(0.15)
print('      └─┘└─┘┘└┘ ┴ ┴└─└─┘┴─┘┴─┘└─┘┴└─  ┴ ┴┴└─└─┘┴ ┴  ┘└┘└─┘ ┴ └┴┘└─┘┴└─┴ ┴  ')
time.sleep(0.1)
print('                                                                                    ')
time.sleep(0.1)
print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')
############################
time.sleep(0.1)
print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')
time.sleep(0.1)
############################
# can0 up @ 125kbps
#fg ms-can is 125kbps hs-can is 500kbps
os.system("sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 100 loopback on")
os.system("sudo /sbin/ifconfig can0 up txqueuelen 1250")
############################
#this module needs to be loaded before trying to emit keypresses
os.system("sudo modprobe uinput")
############################
# socketcan
# set to vcan0 for socketcan virtual can
# set to can0 for live socketcan connection
############################
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    print('can0swc:')
    time.sleep(0.1)
    print(' ')
    time.sleep(0.1)
    print('        awaiting can frames...')
    time.sleep(0.1)
    print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')
    time.sleep(0.1)

except OSError:
    print('        can0 interface not found. check wiring and config.')
    print('        these commands may help...')
    print('        "sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 100 loopback on"')
    print('        "sudo /sbin/ifconfig can0 up txqueuelen 65535"')
    exit()
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

        if message.arbitration_id == BEM:                        # CAN_ID variable
            q.put(message)

############################
# Rx Queue
############################
q = queue.Queue()
rx = Thread(target = can_rx_task)
rx.start()
c = ''
count = 0
t = 0
############################
# Main Loop
############################
try:
    while True:
        #for i in range(16):
            while(q.empty() == True):       # Wait until there is a message
                pass
            message = q.get()
            c = '{0:f},{1:d},'.format(message.timestamp,count)
###########################
#Steering Wheel Buttons
###########################
            if message.arbitration_id == SWC and message.data[7] == SWC_SEEK[0]:
                device.emit_click(uinput.KEY_N)  #next song
                print('can0swc:seek')
                time.sleep(0.1)
            if message.arbitration_id == SWC and message.data[7] == SWC_SEEK[1]:
                device.emit_click(uinput.KEY_N)  #next song
                print('can0swc:seek')
                time.sleep(0.1)
            if message.arbitration_id == SWC and message.data[7] == SWC_SEEK[2]:
                device.emit_click(uinput.KEY_N)  #next song
                print('can0swc:seek')
                time.sleep(0.1)

            if message.arbitration_id == SWC and message.data[7] == SWC_VOLUP[0]:
                device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                device.emit_click(uinput.KEY_E) #volup opendash
                print('can0swc:volup')
                time.sleep(0.01)
            if message.arbitration_id == SWC and message.data[7] == SWC_VOLUP[1]:
                device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                device.emit_click(uinput.KEY_E) #volup opendash
                print('can0swc:volup')
                time.sleep(0.01)
            if message.arbitration_id == SWC and message.data[7] == SWC_VOLUP[2]:
                device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                device.emit_click(uinput.KEY_E) #volup opendash
                print('can0swc:volup')
                time.sleep(0.01)

            if message.arbitration_id == SWC and message.data[7] == SWC_VOLDOWN[0]:
                device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                device.emit_click(uinput.KEY_R) #voldown opendash
                print('can0swc:voldown')
                time.sleep(0.01)
            if message.arbitration_id == SWC and message.data[7] == SWC_VOLDOWN[1]:
                device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                device.emit_click(uinput.KEY_R) #voldown opendash
                print('can0swc:voldown')
                time.sleep(0.01)
            if message.arbitration_id == SWC and message.data[7] == SWC_VOLDOWN[2]:
                device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                device.emit_click(uinput.KEY_R) #voldown opendash
                print('can0swc:voldown')
                time.sleep(0.01)

            if message.arbitration_id == SWC and message.data[6] == SWC_PHONE[0]:
                device.emit_click(uinput.KEY_W) #opendash cycle pages
                print('can0swc:phone')
                time.sleep(0.5)
            if message.arbitration_id == SWC and message.data[6] == SWC_PHONE[1]:
                device.emit_click(uinput.KEY_W) #opendash cycle pages
                print('can0swc:phone')
                time.sleep(0.5)
            if message.arbitration_id == SWC and message.data[6] == SWC_PHONE[2]:
                device.emit_click(uinput.KEY_W) #opendash cycle pages
                print('can0swc:phone')
                time.sleep(0.5)

############################
#ICC Buttons
############################
            if message.arbitration_id == ICC and message.data[3] == ICC_VOLUP:
                device.emit_click(uinput.KEY_VOLUMEUP)
                device.emit_click(uinput.KEY_E)
                print('can0icc:volup')
            if message.arbitration_id == ICC and message.data[3] == ICC_VOLDOWN:
                device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                device.emit_click(uinput.KEY_R) #voldown opendash
                print('can0icc:voldown')
                time.sleep(0.1)

            if message.arbitration_id == ICC and message.data[0] == ICC_NEXT:
                device.emit_click(uinput.KEY_N)
                print('can0icc:next')wwwwwwwwwww
                time.sleep(0.1)

            if message.arbitration_id == ICC and message.data[0] == ICC_PREV:
                device.emit_click(uinput.KEY_C)
                print('can0icc:prev')
                time.sleep(0.1)
#            if message.arbitration_id == ICC and message.data[2] == ICC_PWR:
#              #os.system("sudo reboot")
#              print('can0icc:pwr')
                time.sleep(0.1)

            if message.arbitration_id == ICC and message.data[0] == ICC_MENU:
   #            os.system("sudo systemctl start dash")
                print('can0icc:menu')
                time.sleep(0.1)

            if message.arbitration_id == ICC and message.data[2] == ICC_OK:
                print('can0icc:ok')
                time.sleep(0.1)

            if message.arbitration_id == ICC and message.data[1] == ICC_LOAD:
                os.system("/home/pi/openauto/bin/autoapp")
                print('can0icc:load')
                time.sleep(0.1)

            if message.arbitration_id == ICC and message.data[1] == ICC_EJECT:
                os.system("sudo systemctl stop dash")
                print('can0icc:eject')
                time.sleep(0.1)
#############################
#BEM Buttons
#############################

            #if message.arbitration_id == BEM and message.data[3] == UNLOCK:
                 #os.system("feh ./unlock.jpg -x -n")
            #if message.arbitration_id == BEM and message.data[3] == LOCK:
                #os.system("feh ./lock.jpg -x -n")
            #if message.arbitration_id == BEM and message.data[3] == DSC:
                #os.system("feh ./dsc.jpg -x -n")
            #if message.arbitration_id == BEM and message.data[3] == LIGHT:
                #os.system("feh ./lights.jpg -x -n")
            #if message.arbitration_id == BEM and message.data[2] == HAZARD[0] and message.data[3] == HAZARD[1]:
                #os.system("feh ./hazard.jpg -x -n")

#############
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
