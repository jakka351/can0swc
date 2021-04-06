#!/usr/bin/python3
#can0swc fg falcon swc-can adapter
#https://github.com/jakka351/FG-Falcon | https://github.com/jakka351/can0swc
############################
#vehicle version with fat trimmed
############################
import can
import time
import os
import uinput
import queue
from threading import Thread
import sys, traceback

device = uinput.Device([
        uinput.KEY_N,
        uinput.KEY_VOLUMEUP,
        uinput.KEY_VOLUMEDOWN,
        uinput.KEY_C,
        uinput.KEY_W,
        ])

def setup():
    global bus
    os.system("sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 1000")     
    os.system("sudo /sbin/ifconfig can0 up txqueuelen 100") 
    os.system("sudo modprobe uinput") 
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        sys.exit()
    
def msgbuffer():
    global message, q                                             
    while True:
        message = bus.recv()
        if message.arbitration_id == 0x2f2:                        
            q.put(message)
        if message.arbitration_id == 0x2fc:                        
            q.put(message)

def main():
    try:
        while True:
            for i in range(8):
                while(q.empty() == True):                             
                    pass
                message = q.get()   
                if message.arbitration_id == 0x2f2:                       # if the can id is the same as variable,     
                    if message.data[7] == 0x08:                  # and the message data of bit x matches from list
                        device.emit_click(uinput.KEY_N)                
                    elif message.data[7] == 0x09:
                        device.emit_click(uinput.KEY_N)  #next song
                    elif message.data[7] == 0x0C:
                        device.emit_click(uinput.KEY_N)  #next song
                    elif message.data[7] == 0x10:
                        device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                    elif message.data[7] == 0x11:
                        device.emit_click(uinput.KEY_VOLUMEUP) 
                    elif message.data[7] == 0x14:
                        device.emit_click(uinput.KEY_VOLUMEUP) 
                    elif message.data[7] == 0x18:
                        device.emit_click(uinput.KEY_VOLUMEDOWN) 
                    elif message.data[7] == 0x19:
                        device.emit_click(uinput.KEY_VOLUMEDOWN) 
                    elif message.data[7] == 0x1C:
                        device.emit_click(uinput.KEY_VOLUMEDOWN) 
                    elif message.data[6] == 0x61:
                        device.emit_click(uinput.KEY_W) 
                    elif message.data[6] == 0x65:
                        device.emit_click(uinput.KEY_W) 
                    elif message.data[6] == 0x68:
                        device.emit_click(uinput.KEY_W) 
                elif message.arbitration_id == 0x2fc:
                    if message.data[3] == 0x41:
                        device.emit_click(uinput.KEY_VOLUMEUP)
                    elif message.data[3] == 0x81:
                        device.emit_click(uinput.KEY_VOLUMEDOWN) 
                    elif message.data[0] == 0x04:
                        device.emit_click(uinput.KEY_N)
                    elif message.data[0] == 0x08:
                        device.emit_click(uinput.KEY_C)
                    elif message.data[1] == 0x40:
                        os.system("omxplayer /boot/ford.mp4")
                    elif message.data[1] == 0x80:
                        os.system("omxplayer /boot/ford.mp4")
                                          

    except KeyboardInterrupt:
        sys.exit(0)                                              # quit if ctl + c is hit
    except Exception:
        traceback.print_exc(file=sys.stdout)                     # quit if there is a python problem
        sys.exit()
    except OSError:
        sys.exit()                                               # quit if there is a system issue

if __name__ == "__main__":                                       # run the program
    q                      = queue.Queue()                       #
    rx                     = Thread(target = msgbuffer)          #
    setup()                                                      # set the can interface
    rx.start()                                                   # start the rx thread and queue msgs
    main()                                                       # match can frames + emit keypress
