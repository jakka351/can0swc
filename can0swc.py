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
ICC                    = 0x2FC              #id 764 #was set incorrectly to 2F4,
#BEM                    = 0x307              #id
############################
# ICC Volume
############################
VOL                    = (0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F)
############################
# SWC Button CAN Data
############################
SWC_SEEK               = (0x08, 0x09)  # [7]
SWC_VOLUP              = (0x10, 0x11)  # [7]
SWC_VOLDOWN            = (0x18, 0x19)  # [7]
SWC_PHONE              = (0x61,0x65,0x68) #[6]
SWC_MODE               = 0x10
############################
# ICC Button CAN Data
############################
ICC_VOLUP              = 0x41 #[3]
ICC_VOLDOWN            = 0x81 #[3]
ICC_NEXT               = 0x08 #[0]
ICC_PREV               = 0x04 #[0]
ICC_PWR                = 0x00
ICC_EJECT              = 0x80 #[1]
ICC_LOAD               = 0x40 #[1]
ICC_MENU               = 0x10 #[0]
ICC_BACK               = 0x00
ICC_OK                 = 0x21 #[2]
############################
# BEM CAN Data
############################
#BEM_HAZ                = (0x01, 0x80) # -flash hazard triangle img
#BEM_LOCK               = 0x00 #-flash padlock img
#BEM_UNLOCK             = 0x00 #-flash padlock img
#BEM_DSC                = 0x00 #-flash tyres smoking img
#BEM_LIGHT              = 0x00 #-Script to White Screen to Generate Light/Temp swap to day brightness

############################
############################
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
#fg ms-can is 125kbps hs-can is 500kbps
#os.system("sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 100 loopback on")
#os.system("sudo /sbin/ifconfig can0 up txqueuelen 65535")
############################
#this module needs to be loaded before trying to emit keypresses
#os.system("sudo modprobe uinput")
############################
# sleep
time.sleep(0.1)
print('can0swc:')
############################
# socketcan
# currently assumes vehicle comms network is up on can0 @ 125kbps
############################
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    print('socketcan configured...awaiting can frames.....')

except OSError:
    print('can0swc cannot find can interface. check wiring and config')
    exit()
############################
# CAN Rx
############################
def can_rx_task():                                               # rx can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == SWC:                        # CAN_ID variable
            q.put(message)

        if message.arbitration_id == SWC2:                        # CAN_ID variable
            q.put(message)                                       # put message into queue

        if message.arbitration_id == ICC:                        # CAN_ID variable
            q.put(message)

#        if message.arbitration_id == BEM:                        # CAN_ID variable
#            q.put(message)

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
#Tested, works
            if message.arbitration_id == SWC and message.data[7] == SWC_SEEK[0]:
                device.emit_click(uinput.KEY_N)  #next song
                print('can0swc:seek')
                time.sleep(0.1)
#Tested, works
            if message.arbitration_id == SWC and message.data[7] == SWC_SEEK[1]:
                device.emit_click(uinput.KEY_N)  #next song
                print('can0swc:seek')
                time.sleep(0.1)
#Tested, Works
            if message.arbitration_id == SWC and message.data[7] == SWC_VOLUP[0]:
                device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                device.emit_click(uinput.KEY_E) #volup opendash
                print('can0swc:volup')
                time.sleep(0.01)
#Tested, works
            if message.arbitration_id == SWC and message.data[7] == SWC_VOLDOWN[0]:
                device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                device.emit_click(uinput.KEY_R) #voldown opendash
                print('can0swc:voldown')
                time.sleep(0.01)
#########################################################
# Test and fix this
#########################################################
            if message.arbitration_id == SWC and message.data[6] == SWC_PHONE[0]:
                while message.data[6] == SWC_PHONE[0] and t <= 1:
                    sleep(0.1)
                    t += 0.1
                device.emit_click(uinput.KEY_P) #phone key openauto
                print('can0swc:phone-held')
                time.sleep(0.1)
#########################################################
#########################################################
            if message.arbitration_id == SWC and message.data[6] == SWC_PHONE[0]:
                device.emit_click(uinput.KEY_W) #opendash cycle pages
                print('can0swc:phone')
                time.sleep(0.1)
# tested, sometimes cycles two pages at a time
# added time.sleep(0.1) to curb unwanted doubleclicks
            if message.arbitration_id == SWC and message.data[6] == SWC_PHONE[1]:
                device.emit_click(uinput.KEY_W) #opendash cycle pages
                print('can0swc:phone')
                time.sleep(0.1)
#test this
            if message.arbitration_id == SWC and message.data[0] == VOL:
                print('Media Volume:', VOL)
                time.sleep(0.1)
                
            if message.arbitration_id == SWC2 and message.data[6] == SWC_MODE:
                print('mode button')

############################
#ICC Buttons
############################
#test this
            if message.arbitration_id == ICC and message.data[3] == ICC_VOLUP:
                device.emit_click(uinput.KEY_VOLUMEUP)
                device.emit_click(uinput.KEY_E)
                print('can0icc:volup')
#test this
            if message.arbitration_id == ICC and message.data[3] == ICC_VOLDOWN:
                device.emit_click(uinput.KEY_VOLUMEDOWN)
                device.emit_click(uinput.KEY_R)
                print('can0icc:voldown')
#test this
            if message.arbitration_id == ICC and message.data[0] == ICC_NEXT:
                device.emit_click(uinput.KEY_N)
                print('can0icc:next')
                time.sleep(0.1)
#test this
            if message.arbitration_id == ICC and message.data[0] == ICC_PREV:
                device.emit_click(uinput.KEY_C)
                print('can0icc:prev')
                time.sleep(0.1)
#test this
            if message.arbitration_id == ICC and message.data[2] == ICC_PWR:
                os.system("")

            if message.arbitration_id == ICC and message.data[0] == ICC_MENU:
                os.system("")
#test this
            if message.arbitration_id == ICC and message.data[2] == ICC_OK:
                print('can0icc:ok')
                time.sleep(0.1)
#test this
            if message.arbitration_id == ICC and message.data[1] == ICC_EJECT:
                device.emit_click(uinput.KEY_Q)
                print('can0icc:eject')
                time.sleep(0.1)
#test this
            if message.arbitration_id == ICC and message.data[1] == ICC_LOAD:
                device.emit_click(uinput.KEY_O)
                print('can0icc:load')
                time.sleep(0.1)
#test this
            if Exception:
                print('An error has occured, exiting to allow service to restart')
                exit()
                #this is where setting can0swc.service to restart is important
##############
#Body Elec
##############
#            if message.arbitration_id == BEM and message.data[6] == BEM_HAZ:
#                os.system("./hazards.sh")

#            if message.arbitration_icd == BEM and message.data[6] == BEM_DSC:
#                os.system("./dsc.sh")

#            if message.arbitration_id == BEM and message.data[6] == BEM_LOCK:
#                os.system("./lock.sh")

#            if message.arbitration_id == BEM and message.data[6] == BEM_UNLOCK:
#               os.system("./unlock.sh")

#
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
