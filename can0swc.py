#!/usr/bin/python3
# can0swc fg falcon swc-can adapter
# https://github.com/jakka351/FG-Falcon | https://github.com/jakka351/can0swc
# 
############################
#import modules
############################
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
#Global Variables
############################

c                      = ''
count                  = 0  
# CAN Id's
SWC                    = 0x2F2              #id 751
ICC                    = 0x2FC              #id 764
BEM                    = 0x307
INTACTTEMP             = 0x313
# SWC Button CAN Data
SWC_SEEK               = (0x08, 0x09, 0x0C)  # seek button on byte [7] of id 0x2f2
SWC_VOLUP              = (0x10, 0x11, 0x14)  # volume + button on bit [7] of id 0x2f2
SWC_VOLDOWN            = (0x18, 0x19, 0x1C)  # volume - button on bit [7] of id 0x2f2
SWC_PHONE              = (0x61, 0x65, 0x68)  # phone button on bit [6] of id 0x2f2
# ICC Button CAN Data
ICC_VOLUP              = 0x41 # vol + button on bit [3] of id 0x2fc
ICC_VOLDOWN            = 0x81 # vol - button on bit [3] of id 0x2fc
ICC_NEXT               = 0x04 # seek + button on bit [0] of id 0x2fc
ICC_PREV               = 0x08 # seek - button on bit [0] of id 0x2fc
ICC_EJECT              = 0x80 # eject button on bit [1] of id 0x2fc
ICC_LOAD               = 0x40 # load button on bit [1] of id 0x2fc
#BEM Butonn CAN Data
BEM_LOCK               = 0x00
BEM_UNLOCK             = 0x00
BEM_DSC                = 0x00
BEM_DOMELIGHT          = 0x90
BEM_HAZARD             = 0x01

def scroll():
    #prints logo to console
        print('  ')
        print('             ,777I77II??~++++=~::,,,,::::::::::~~~==+~                                        ')
        print('           ,IIIIII,IIII+~..,,:,,,,,:~:,,.....,~,,:::~+?+?=                                    ')
        print('         :=I7777I=IIIIII~...:===,:,=~:,,,,,,::=,,,:::~~:=?===                                 ')
        print('      ~=,?I?777II7IIIII=~,.,,,,,,,,,,,:,,,,,,::,,,,~:~~~~:~+:~:~                              ')
        print('      I=I?IIIIII~IIIIIII+:..,,,,,,,,,,,,.,.,,::.,,,,:::~~=~:=+~?~~                            ')
        print('      I77?+?IIIIIIIII7I7=~,.,,,..,,,,.,.,.......,.,.,.,..,,,:~=~:==~~                         ')
        print('     +=I7777I?+???IIIIII+=:..,,,,,,,,,,,...,,,,,,,,,,,,..,,,:..:?I7+...,,                     ')
        print('     +=+=I7777I=~~+~:~IIII~,..,,,,,,,,,,..,,,,,...~+II?I?+?III7IIII777I7=.....                ')
        print('      ==++++III=~~~::~+I:+?~:.........:+IIIIIIII+=?IIIIIII???????????III7II7I....             ')
        print('     ?+=======::,,,,...,,:=?==~?+?????????????+==~~~~~===+++++++++++++++???II?III....         ')
        print('     ?+=======+=~=I7III~:~~I??++??IIIIII??+??++++==~~~~:::~~~~============++?II?+7II.         ')
        print('     ??+=====~~~=~~~+III~~=III??++++=+++?II??+=+?+====~~~:::::~~~~~~~~~~======+???++II.       ')
        print('     ??+=?=~~~~~~~~~~=~I=77I7III??++==~++++=+I??+?~?+===~~~~::::::~~~~~~~~~~~===++++=II,      ')
        print('     I??+=++=~~~~~~~~~~~?I777IIII??++====~======????+==+==~~~~:::::::::~~~~~~~~~====+==I,     ')
        print('      ?I+=~~=++~~~~~~~~=?=:+IIIII??++++===~:~~~~~~~=???=?:=~~~~~::::::::~~~~~~~~~~=~=+?7~:    ')
        print('       ?+=~~~~=++~~~~~+???~=?7II??+++++++==~~:~~~~~~:~~???=+:~~~~~~:::::::::~~~~=++:,.,+=,,   ')
        print('        =?I+~~~==++~~:+??~====+I?+===+++++==~~~::::::::::~????~~~~~:::::~:~==+:,,,,?..::+=:   ')
        print('          =?I=~~~==++=+++~==:,~~=+====+++++:,,...:,::~:::::~~~~+~:~~:~~==,.,,.?I~,..::~~=,:   ')
        print('           ~=+I?=~~=~+++~~=...,~:=+====++?:~+=?I~,I=I??..~III7I:==~,.,,.,,.,,,...::~~++~:~:   ')
        print('              ~?I+=~~~~+~~~.:+,,,:=+===+++~+==~=+:III=?I?77777I~~~===,,,,.,.,,~~~~=+=~::,,:   ')
        print('                ~?I+=:~~~~~~,,+:,,+==~+++++,:~~:==,??,:,,=??I++,,,:~===,,,::~~=++=:::~=..,,   ')
        print('             ,,,,:=+?==~~~~.=:~~,..,=+++++=~:=+=~:.,:,,,,::?=I=:::::+~====++++=~:::?I+?,..,   ')
        print('              :,,,,~+====~:,,,:=,.,,,~~===~~~,:==~~~~~~:..,,,,,,..,,,~==+++~:,~++I++II?...    ')
        print('               :,,,,,,+==+,:..:==.:,,~:~~~~~:,,,,:~~~~~~~~=========~++++~,....II+II+?...,:    ')
        print('                 ,,,,,,,++.,,.,,,,=:,,~:::~:::,,,,,,,,,::~~~=====~====~.......?I=I.....,:~    ')
        print('                   ::,,,,,,:~::,~+I+,..~::::::,,,,,,,,,,,,,,,,,~==~~~.........+.......,:,,    ')        
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
   #os.system("sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 1000")     
                                                   # sets the can interface type - this is for socketcan on debian
   #os.system("sudo /sbin/ifconfig can0 up txqueuelen 100") 
                                                   # brings the interface up, sets transmit queue length
    #os.system("sudo modprobe uinput") 
                                                   # loads the uinput module that allowkeypresses 
    try:
        bus = can.interface.Bus(channel='vcan0', bustype='socketcan_native')
                                                   # vcan0 is a virtual can interface, handy for testing
    except OSError:
        sys.exit()
                                                   # quits if there is no canbus interface

    print("CANbus active on", bus)  
    print("waiting for matching can frame...")     #this line gets replaced by the next matching can frame
    print("ready to emit keypress...")             # this line gets replaced by the button in the car that is pushed

def msgbuffer():
    global message, q, SWC, ICC, BEM, INTACTTEMP                                             
    while True:
        message = bus.recv()          # if recieving can frames then put these can arb id's into a queue
        if message.arbitration_id == SWC:                        
            q.put(message)

        if message.arbitration_id == ICC:                        
            q.put(message)

        if message.arbitration_id == BEM:                        
            q.put(message)

        if message.arbitration_id == INTACTTEMP:                        
            q.put(message)

def cleanline():                      # cleans the last output line from the console
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

def cleanscreen():                    # cleans the whole console screen
    os.system("clear")


#def settings():
#        message_setting = 

def main():
    try:
        while True:
            for i in range(8):
                while(q.empty() == True):                               # wait for messages to queue
                    pass
                message = q.get()   
                c = '{0:f},{1:d},'.format(message.timestamp,count)
                if message.arbitration_id == SWC:                       # if the can id is the same as variable,     
                    if message.data[7] in SWC_SEEK:                  # and the message data of bit x matches from list
                        device.emit_click(uinput.KEY_N)                # then emulate a keypress
                        cleanline()                                     # cleans last frame
                        cleanline()                                     # cleans last button push
                        print(message)                                  # print new can frame
                        print("SWCSeekBtn pushed @", message.timestamp)                      # print button push
                        time.sleep(0.2)
                        
                    elif message.data[7] in SWC_VOLUP:
                        device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCVolUpBtn pushed @", message.timestamp)
                        time.sleep(0.2)
                        
                    elif message.data[7] == SWC_VOLDOWN:
                        #device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCVolDownBtn pushed @", message.timestamp)
                        time.sleep(0.2)
                        
                    elif message.data[6] in SWC_PHONE:
                        #device.emit_click(uinput.KEY_W) #opendash cycle pages
                        cleanline()
                        cleanline()
                        print(message)
                        print("SWCPhoneBtn pushed @", message.timestamp)
                        time.sleep(0.2)
                        
                    else:
                        pass

                elif message.arbitration_id == ICC:
                    if message.data[3] == ICC_VOLUP:
                        #device.emit_click(uinput.KEY_VOLUMEUP)
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCVolUpBtn pushed @", message.timestamp)
                        time.sleep(0.2)
                        
                    elif message.data[3] == ICC_VOLDOWN:
                        #device.emit_click(uinput.KEY_VOLUMEDOWN) 
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCVolDownBtn pushed @", message.timestamp)
                        time.sleep(0.2)
                        
                    elif message.data[0] == ICC_NEXT:
                        #device.emit_click(uinput.KEY_N)
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCSeekUpBtn pushed @", message.timestamp)
                        time.sleep(0.2)
                        
                    elif message.data[0] == ICC_PREV:
                        #device.emit_click(uinput.KEY_C)
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCSeekDownBtn pushed @", message.timestamp)
                        time.sleep(0.2)
                        
                    elif message.data[1] == ICC_LOAD:
                        #os.system("sudo systemctl start dash.service")
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCLoadBtn pushed @", message.timestamp)
                        time.sleep(0.2)
                        
                    elif message.data[1] == ICC_EJECT:
                        #os.system("sudo systemctl stop dash.service")
                        cleanline()
                        cleanline()
                        print(message)
                        print("ICCEjectBtn pushed @", message.timestamp)
                        time.sleep(0.2)
                                            
                    else:
                        pass
                    
                elif message.arbitration_id == BEM and message.data[3] == BEM_LOCK:
                    #os.system("omxplayer lock.mp4 ")
                    cleanline()
                    cleanline()
                    print(message)
                    print("VehicleLockButton pushed @", message.timestamp)
                    time.sleep(2.0)
                    
                elif message.arbitration_id == BEM and message.data[3] == BEM_UNLOCK:
                    #os.system("omxplayer ")
                    cleanline()
                    cleanline()
                    print(message)
                    print("VehicleUnlockButton pushed @", message.timestamp)
                    
                elif message.arbitration_id == BEM and message.data[3] == BEM_DSC:
                    time.sleep(1.5)
                    if message.arbitration_id == BEM and message.data[3] == BEM_DSC:
                        #os.system("omxplayer burnout.mp4")
                        cleanline()
                        cleanline()
                        print(message)
                        print("DynamicStabilityControlSwitch pushed @", message.timestamp)
                    else:
                        pass
                
                elif message.arbitration_id == BEM and message.data[3] == BEM_DOMELIGHT:
                    #os.system("omxplayer whitelight.mp4")
                    cleanline()
                    cleanline()
                    print(message)
                    print("DomeLightSwitch pushed @", message.timestamp) 
                    
                elif message.arbitration_id == BEM and message.data[3] == BEM_HAZARD:
                    #os.system("omxplayer /home/pi/hazard.mp4 ")
                    cleanline()
                    cleanline()
                    print(message)
                    print("HazardLightSwitch pushed @", message.timestamp) 
                    time.sleep(3)
                        
                elif message.arbitration_id == INTACTTEMP and message.data[0] <= 0x01:
                    IntActTemp = float(message.data[0])
                    if IntActTemp != 0:
                        cleanline() 
                        cleanline()
                        print(message)
                        print("Interior Actual Temperature: ", IntActTemp / 6, " Degrees Celcius")
                        time.sleep(3.0)
                    else:
                        pass

                else:
                    pass
                                                                           
    except KeyboardInterrupt:
        sys.exit(0)                                              # quit if ctl + c is hit
    except Exception:
        traceback.print_exc(file=sys.stdout)                     # quit if there is a python problem
        sys.exit()
    except OSError:
        sys.exit()                                               # quit if there is a system issue

############################
# can0swc
############################
    

if __name__ == "__main__":                                       # run the program
    q                      = queue.Queue()                       #
    rx                     = Thread(target = msgbuffer)          #
    cleanscreen()                                                # clean the console screen
    scroll()                                                     # scroll out fancy logo text
    setup()                                                      # set the can interface
    rx.start()                                                   # start the rx thread and queue msgs
    main()                                                       # match can frames + emit keypress
