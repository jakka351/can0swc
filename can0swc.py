#!/usr/bin/python3
#can0swc fg falcon swc-can adapter
#https://github.com/jakka351/FG-Falcon | https://github.com/jakka351/can0swc
import can
#from can import bus
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
c                      = ''
count                  = 0  
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

def scroll():

        print("                                                                           ")
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
        print("                                                                           ")
def setup():
    global bus
#   os.system("sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 1000")
#   os.system("sudo /sbin/ifconfig can0 up txqueuelen 100")
    os.system("sudo modprobe uinput")  
    try:
        bus = can.interface.Bus(channel='vcan0', bustype='socketcan_native')
    except OSError:
        sys.exit()
    
    print("CANbus active on", bus)  
    print("waiting for matching can frame...")
    print("ready to emit keypress...")

def msgbuffer():
    global message, q                                               
    while True:
        message = bus.recv()
        if message.arbitration_id == SWC:                        
            q.put(message)

        if message.arbitration_id == ICC:                        
            q.put(message)

def cleanline():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

def cleanscreen():
    os.system("clear")

def main():
#    global c, count, message, q 
    try:
        while True:
            for i in range(8):
                while(q.empty() == True):       # Wait until there is a message
                    pass
                message = q.get()   
                c = '{0:f},{1:d},'.format(message.timestamp,count)
                if message.arbitration_id == SWC:
                    if message.data[7] == SWC_SEEK[0]:
                        #device.emit_click(uinput.KEY_N)  #next song
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCSeekBtn Pushed")
                        time.sleep(0.2)
                    elif message.data[7] == SWC_SEEK[1]:
                        #device.emit_click(uinput.KEY_N)  #next song
                        cleanline()
                        cleanline()                       
                        print(message)
                        print("SWCSeekBtn Pushed")

                    elif message.data[7] == SWC_SEEK[2]:
                        #device.emit_click(uinput.KEY_N)  #next song
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCSeekBtn Pushed")
                       
                    elif message.data[7] == SWC_VOLUP[0]:
                        #device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                        time.sleep(0.2)
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCVolUpBtn Pushed")
                        
                    elif message.data[7] == SWC_VOLUP[1]:
                        #device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCVolUpBtn Pushed")
                        
                    elif message.data[7] == SWC_VOLUP[2]:
                        #device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCVolUpBtn Pushed")
                        
                    elif message.data[7] == SWC_VOLDOWN[0]:
                        #device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCVolDownBtn Pushed")
                        
                    elif message.data[7] == SWC_VOLDOWN[1]:
                        #device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCVolDownBtn Pushed")
                        
                    elif message.data[7] == SWC_VOLDOWN[2]:
                        #device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCVolDownBtn Pushed")
                        
                    elif message.data[6] == SWC_PHONE[0]:
                        #device.emit_click(uinput.KEY_W) #opendash cycle pages
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCPhoneBtn Pushed")
                        
                    elif message.data[6] == SWC_PHONE[1]:
                        #device.emit_click(uinput.KEY_W) #opendash cycle pages
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCPhoneBtn Pushed")
                        
                    elif message.data[6] == SWC_PHONE[2]:
                        #device.emit_click(uinput.KEY_W) #opendash cycle pages
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCPhoneBtn Pushed")
                        
                elif message.arbitration_id == ICC:
                    if message.data[3] == ICC_VOLUP:
                        #device.emit_click(uinput.KEY_VOLUMEUP)
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCVolUpBtn Pushed")
                        
                    elif message.data[3] == ICC_VOLDOWN:
                        #device.emit_click(uinput.KEY_VOLUMEDOWN) 
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCVolDownBtn Pushed")
                        
                    elif message.data[0] == ICC_NEXT:
                        #device.emit_click(uinput.KEY_N)
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCSeekUpBtn Pushed")
                        
                    elif message.data[0] == ICC_PREV:
                        #device.emit_click(uinput.KEY_C)
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCSeekDownBtn Pushed")
                        
                    elif message.data[1] == ICC_LOAD:
                        #os.system("sudo systemctl start dash.service")
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCLoadBtn Pushed")
                        
                    elif message.data[1] == ICC_EJECT:
                        #os.system("sudo systemctl stop dash.service")
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCEjectBtn Pushed")
                                          

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        traceback.print_exc(file=sys.stdout)    
        sys.exit()
    except OSError:
        sys.exit()

############################
# can0swc
############################
    

if __name__ == "__main__":
    q                      = queue.Queue()
    rx                     = Thread(target = msgbuffer)
    cleanscreen()
    scroll()
    setup()
    rx.start()
    main()
