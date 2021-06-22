#!/usr/bin/python3
#can0swc fg falcon swc-can adapter
#https://github.com/jakka351/FG-Falcon | https://github.com/jakka351/can0swc
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
HVAC                   = 0x353
INTACTTEMP             = 0x313
RDS                    = 0x2E6
RDSN                   = 0x309
# SWC Button CAN Data
SWC_SEEK               = (0x08, 0x09, 0x0C)  # seek button on bit [7] of id 0x2f2
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
BEM_DOMELIGHT          = 0x00
BEM_HAZARD             = 0x00
#HVAC Data
#############################
#HVAC                    =  0x353 #can id 851 
HVAC_off                =  0xAB  #  [5] A 129 0 0 34 [171] 0 0    All Off
HVAC_TEMP               =  0     #851 x4
HVAC_OUT                =  0     #Outside Temp 851 x5
HVAC_FANSPEED           =  0     #Fan speed 851 x8
HVAC_VENTSTATUS         =  0     #Vent tatus 851 x1
VA                      =  0x4B  # print('Floor Vents, Close Cabin')
VB                      =  0x2B  # print('Floor Vents, Open Cabin')
VC                      =  0x2F  # print('Window and Feet Vets, Open Cabin')
VD                      =  0x4F  # print('Window and Feet Vents, Close Cabin')
VE                      =  0x5B  # print('Face, Floor, Close Cabin')
VF                      =  0x3B  # print('Face, Floor, Open Cabin')
VG                      =  0x33  # print('Face, Open Cabin')
VH                      =  0x53  # print('Face, Close Cabin')
VI                      =  0x27  # print('Window, Manual Fan')
VJ                      =  0x26  # print('Window, Auto Fan')
VK                      =  0x83  # print('A/C Off, Open Cabin')
VL                      =  0x8B  # print('A/C Off, Floor Vents, Open Cabin')
VM                      =  0x8F  # print('A/C Off, Floor and Window Vents, Open Cabin')
VN                      =  0x9B  # print('A/C Off, Floor and Face Vents, Open Cabin')
VO                      =  0xA6  # print('A/C Off, Window Vents, Open Cabin')
VP                      =  0xA7  # print('A/C Off, Manual Fan, Open Cabin')
VQ                      =  0xC3  # print('A/C Off, Close Cabin')
VR                      =  0xCB  # print('A/C Off, Floor Vents, Close Cabin')
VS                      =  0xCF  # print('A/C Off, Floor and Window Vents, Close Cabin')
VT                      =  0xDB  # print('A/C Off, Floor and Face Vents, Close Cabin')
VU                      =  0x43  # print('Auto, Close Cabin')
VW                      =  0x23  # print('Auto, Open Cabin')
#############################
def scroll():
    #prints logo to console
        print('  ')
        print(',,,,,,:,,,,,,,777I77II??~++++=~::,,,,::::::::::~~~==+~:::::,,::,:+?????????+==:,::::::::,:::::::::::::::::::::~~~~~~~:::')
        print(':::::::,,,,,IIIIII,IIII+~..,,:,,,,,:~:,,.....,~,,:::~+?+?=??+=~:...,,.,.,...,,,.,,,,:~?:::::::::~~~~~~::::,:::::~::::::~')
        print('::::::::::=I7777I=IIIIII~...:===,:,=~:,,,,,,::=,,,:::~~:=?===~,::::::::,,:,,:::,,,,,~=+?=,,:::::~~~~~~~==~~~~~~~:::~~~~~')
        print('::::::~=,?I?777II7IIIII=~,.,,,,,,,,,,,:,,,,,,::,,,,~:~~~~:~+:~:~~::,:~~~:::::,~,,,,,:~~=+?~~~~~==::::,~~~~~~~::::::::~~~')
        print('~~~~~~I=I?IIIIII~IIIIIII+:..,,,,,,,,,,,,.,.,,::.,,,,:::~~=~:=+~?~~::~:::~::~:...:,,:::::==:+?:+??+=?+=::::::::::::~~~~~~')
        print('======I77?+?IIIIIIIII7I7=~,.,,,..,,,,.,.,.......,.,.,.,..,,,:~=~:==~~~~~~~~~~~~~::,,:+???III?+???II??~:.~:::~~~~:::~:~:~')
        print('+++=++=I7777I?+???IIIIII+=:..,,,,,,,,,,,...,,,,,,,,,,,,..,,,:..:?I7+...,,,,,:~=~~:::::::,,,,,,,==???+~=+,?+?=::~~~~~~~~~')
        print('?????+=+=I7777I=~~+~:~IIII~,..,,,,,,,,,,..,,,,,...~+II?I?+?III7IIII777I7=............,:~:::::,,,,,,.,I?????+,?+II,::::::')
        print('??????==++++III=~~~::~+I:+?~:.........:+IIIIIIII+=?IIIIIII???????????III7II7I..........,=~::,.,:::,,,,,.,??+????++=:::::')
        print('??III?+=======::,,,,...,,:=?==~?+?????????????+==~~~~~===+++++++++++++++???II?III.....+...,,,,..,:....,:,,,,?+????I~~~~~')
        print('??III?+=======+=~=I7III~:~~I??++??IIIIII??+??++++==~~~~:::~~~~============++?II?+7II.~..,,,,:::,..,........:=77I??,==~~~')
        print('???II??+=====~~~=~~~+III~~=III??++++=+++?II??+=+?+====~~~:::::~~~~~~~~~~======+???++II.:,:,,,,~~,.,+~,......,III?:=?:,,,')
        print('+??II??+=?=~~~~~~~~~~=~I=77I7III??++==~++++=+I??+?~?+===~~~~::::::~~~~~~~~~~~===++++=II,,:,::,.:,....,..,,,~~~++,,,:::::')
        print('???III??+=++=~~~~~~~~~~~?I777IIII??++====~======????+==+==~~~~:::::::::~~~~~~~~~====+==I,:,,,:~:,...,,....,:...::::~::~~')
        print('IIIIII?I+=~~=++~~~~~~~~=?=:+IIIII??++++===~:~~~~~~~=???=?:=~~~~~::::::::~~~~~~~~~~=~=+?7~::~~=~,,...,,,.,,,,,,,,,:::::::')
        print('IIIIII??+=~~~~=++~~~~~+???~=?7II??+++++++==~~:~~~~~~:~~???=+:~~~~~~:::::::::~~~~=++:,.,+=,,,,.,.,,,,,,,,,,,,,,,:::::::::')
        print('IIII??++=?I+~~~==++~~:+??~====+I?+===+++++==~~~::::::::::~????~~~~~:::::~:~==+:,,,,?..::+=:::::::,,,,,,,,,,,::::::::::::')
        print('II????++~~=?I=~~~==++=+++~==:,~~=+====+++++:,,...:,::~:::::~~~~+~:~~:~~==,.,,.?I~,..::~~=,::::::::::::::::::::::::::::::')
        print('???????+++=~=+I?=~~=~+++~~=...,~:=+====++?:~+=?I~,I=I??..~III7I:==~,.,,.,,.,,,...::~~++~:~::::::::::::::::::::::::::::::')
        print('??????++++=~:~~?I+=~~~~+~~~.:+,,,:=+===+++~+==~=+:III=?I?77777I~~~===,,,,.,.,,~~~~=+=~::,,::::::::::::::::::::::::::::::')
        print('++===~~:::,,,,,=~?I+=:~~~~~~,,+:,,+==~+++++,:~~:==,??,:,,=??I++,,,:~===,,,::~~=++=:::~=..,,:::::::::::::::::::::::::::::')
        print('::,:::::::,,,,,,,:=+?==~~~~.=:~~,..,=+++++=~:=+=~:.,:,,,,::?=I=:::::+~====++++=~:::?I+?,..,:::::::::::::::::::::::::::::')
        print(':::::::::::::::,,,,~+====~:,,,:=,.,,,~~===~~~,:==~~~~~~:..,,,,,,..,,,~==+++~:,~++I++II?...::::::::::::::::::::::::::::::')
        print('::::::::::::::::,,,,,,+==+,:..:==.:,,~:~~~~~:,,,,:~~~~~~~~=========~++++~,....II+II+?...,:,,,,:,,:::::::::::::::::::::::')
        print(':::::::::::::::::,,,,,,,++.,,.,,,,=:,,~:::~:::,,,,,,,,,::~~~=====~====~.......?I=I.....,:~,,::::::::::::::::::::::::::::')
        print(':::::::::::::::::::::,,,,,,:~::,~+I+,..~::::::,,,,,,,,,,,,,,,,,~==~~~.........+.......,:,,,,::::::::::::::::::::::::::::')        
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
    os.system("sudo modprobe uinput") 
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
    global message, q                                             
    while True:
        message = bus.recv()          # if recieving can frames then put these can arb id's into a queue
        if message.arbitration_id == SWC:                        
            q.put(message)

        if message.arbitration_id == ICC:                        
            q.put(message)

        if message.arbitration_id == BEM:                        
            q.put(message)            

        if message.arbitration_id == HVAC:                        
            q.put(message)

        if message.arbitration_id == INTACTTEMP:                        
            q.put(message)

        if message.arbitration_id == RDS:
            q.put(message)

        if message.arbitration_id == RDSN:
            q.put(message)

def cleanline():                      # cleans the last output line from the console
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

def cleanscreen():                    # cleans the whole console screen
    os.system("clear")

def main():
    try:
        while True:
            for i in range(8):
                while(q.empty() == True):                               # wait for messages to queue
                    pass
                message = q.get()   
                c = '{0:f},{1:d},'.format(message.timestamp,count)
                if message.arbitration_id == SWC:                       # if the can id is the same as variable,     
                    if message.data[7] == SWC_SEEK[0]:                  # and the message data of bit x matches from list
                        #device.emit_click(uinput.KEY_N)                # then emulate a keypress
                        cleanline()                                     # cleans last frame
                        cleanline()                                     # cleans last button push
                        print(message)                                  # print new can frame
                        print("SeekButton pushed @", message.timestamp)                      # print button push
                        
                    elif message.data[7] == SWC_SEEK[1]:
                        #device.emit_click(uinput.KEY_N)  #next song
                        cleanline()
                        cleanline()                       
                        print(message)
                        print("SeekButton pushed @", message.timestamp)

                    elif message.data[7] == SWC_SEEK[2]:
                        #device.emit_click(uinput.KEY_N)  #next song
                        cleanline()
                        cleanline()
                        print(message)
                        print("SeekButton pushed @", message.timestamp)
                       
                    elif message.data[7] == SWC_VOLUP[0]:
                        #device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                        time.sleep(0.2)
                        cleanline()
                        cleanline()
                        print(message)
                        print("VolumeUpButton pushed @", message.timestamp)
                        
                    elif message.data[7] == SWC_VOLUP[1]:
                        #device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("VolumeUpButton pushed @", message.timestamp)
                        
                    elif message.data[7] == SWC_VOLUP[2]:
                        #device.emit_click(uinput.KEY_VOLUMEUP) #volup openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("VolumeUpButton pushed @", message.timestamp)
                        
                    elif message.data[7] == SWC_VOLDOWN[0]:
                        #device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("VolumeDownButton pushed @", message.timestamp)
                        
                    elif message.data[7] == SWC_VOLDOWN[1]:
                        #device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("VolumeDownButton pushed @", message.timestamp)
                        
                    elif message.data[7] == SWC_VOLDOWN[2]:
                        #device.emit_click(uinput.KEY_VOLUMEDOWN) #voldown openauto
                        cleanline()
                        cleanline()
                        print(message)
                        print("VolumeDownButton pushed @", message.timestamp)
                        
                    elif message.data[6] == SWC_PHONE[0]:
                        #device.emit_click(uinput.KEY_W) #opendash cycle pages
                        cleanline()
                        cleanline()
                        print(message)
                        print("PhoneButton pushed @", message.timestamp)
                        
                    elif message.data[6] == SWC_PHONE[1]:
                        #device.emit_click(uinput.KEY_W) #opendash cycle pages
                        cleanline()
                        cleanline()
                        print(message)
                        print("PhoneButton pushed @", message.timestamp)
                        
                    elif message.data[6] == SWC_PHONE[2]:
                        #device.emit_click(uinput.KEY_W) #opendash cycle pages
                        cleanline()
                        cleanline()
                        print(message)
                        print("PhoneButton pushed @", message.timestamp)
                        
                elif message.arbitration_id == ICC:
                    if message.data[3] == ICC_VOLUP:
                        #device.emit_click(uinput.KEY_VOLUMEUP)
                        cleanline()
                        cleanline()
                        print(message)
                        print("VolumeUpButton pushed @", message.timestamp)
                        
                    elif message.data[3] == ICC_VOLDOWN:
                        #device.emit_click(uinput.KEY_VOLUMEDOWN) 
                        cleanline()
                        cleanline()
                        print(message)
                        print("VolumeDownButton pushed @", message.timestamp)
                        
                    elif message.data[0] == ICC_NEXT:
                        #device.emit_click(uinput.KEY_N)
                        cleanline()
                        cleanline()
                        print(message)
                        print("SeekNextButton pushed @", message.timestamp)
                        
                    elif message.data[0] == ICC_PREV:
                        #device.emit_click(uinput.KEY_C)
                        cleanline()
                        cleanline()
                        print(message)
                        print("SeekPreviousButton pushed @", message.timestamp)
                        
                    elif message.data[1] == ICC_LOAD:
                        #os.system("sudo systemctl start dash.service")
                        cleanline()
                        cleanline()
                        print(message)
                        print("LoadCdButton pushed @", message.timestamp)
                        
                    elif message.data[1] == ICC_EJECT:
                        #os.system("sudo systemctl stop dash.service")
                        cleanline()
                        cleanline()
                        print(message)
                        print("EjectCdButton pushed @", message.timestamp)
                elif message.arbitration_id == BEM:
                    if message.data[3] == BEM_LOCK:
                        os.system("omxplayer ")
                        cleanline()
                        cleanline()
                        print(message)
                        print("VehicleLockButton pushed @", message.timestamp)

                    elif message.data[3] == BEM_UNLOCK:
                        os.system("omxplayer ")
                        cleanline()
                        cleanline()
                        print(message)
                        print("VehicleUnlockButton pushed @", message.timestamp)
                        
                    elif message.data[3] == BEM_DSC:
                        os.system("omxplayer ")
                        cleanline()
                        cleanline()
                        print(message)
                        print("DynamicStabilityControlSwitch pushed @", message.timestamp)
                        
                    elif message.data[3] == BEM_DOMELIGHT:
                        cleanline()
                        cleanline()
                        print(message)
                        print("DomeLightSwitch pushed @", message.timestamp) 
                        #os.system("omxplayer ")
                    elif message.data[3] == BEM_HAZARD:
                        #os.system("omxplayer ")s
                        cleanline()
                        cleanline()
                        print(message)
                        print("DomeLightSwitch pushed @", message.timestamp) 
                elif message.arbitration_id == INTACTTEMP:  
                        time.sleep(3)
                        cleanline() 
                        print("InteriorActualTemperature", message.data[0] / 6)
        
                if message.arbitration_id == HVAC:
                        cleanline()
                        print("TargetAirConTemp: ", message.data[3] / 2)
                        time.sleep(3)
                        cleanline()
                        print('ExteriorAmbientTemperature', message.data[4])
                        time.sleep(3)
                        if message.data[0] == VA:
                          print('VentStatus: Floor Vents, Close Cabin')
                        elif message.data[0] == VB:
                          print('VentStatus: Floor Vents, Open Cabin')
                        elif message.data[0] == VC: 
                          print('VentStatus: Window and Floor Vents, Open Cabin')
                        elif message.data[0] == VD:
                          print('VentStatus: Window and Floor Vents, Close Cabin')
                        elif message.data[0] == VE:
                          print('VentStatus: Face, Floor, Close Cabin')
                        elif message.data[0] == VF:
                          print('VentStatus: Face, Floor, Open Cabin')
                        elif message.data[0] == VG:
                          print('VentStatus: Face, Open Cabin')
                        elif message.data[0] == VH: 
                          print('VentStatus: Face, Close Cabin')
                        elif message.data[0] == VI: 
                          print('VentStatus: Window, Manual Fan')
                        elif message.data[0] == VJ: 
                          print('VentStatus: Window, Auto Fan')
                        elif message.data[0] == VK:
                          print('VentStatus: A/C Off, Open Cabin')
                        elif message.data[0] == VL:
                          print('VentStatus: A/C Off, Floor Vents, Open Cabin')
                        elif message.data[0] == VM:
                          print('VentStatus: A/C Off, Floor and Window Vents, Open Cabin')
                        elif message.data[0] == VN:
                          print('VentStatus: A/C Off, Floor and Face Vents, Open Cabin')
                        elif message.data[0] == VO:
                          print('VentStatus: A/C Off, Window Vents, Open Cabin')
                        elif message.data[0] == VP:
                          print('VentStatus: A/C Off, Manual Fan, Open Cabin')
                        elif message.data[0] == VQ:
                          print('VentStatus: A/C Off, Close Cabin')
                        elif message.data[0] == VR:
                          print('VentStatus: A/C Off, Floor Vents, Close Cabin')
                        elif message.data[0] == VS:
                          print('VentStatus: A/C Off, Floor and Window Vents, Close Cabin')
                        elif message.data[0] == VT:
                          print('VentStatus: A/C Off, Floor and Face Vents, Close Cabin')
                        elif message.data[0] == VU:
                          print('VentStatus: Auto, Close Cabin')
                        elif message.data[0] == VW: 
                          print('VentStatus: Auto, Open Cabin')
                        time.sleep(3) 
                elif message.arbitration_id == HVAC and message.data[7] < 0x80:
                        print('FanSpeed:', message.data[7] / 10)
                        time.sleep(2)
                elif message.arbitration_id == HVAC and message.data[7] >= 0x80:
                        print('FanSpeed: Auto')
                        time.sleep(2)

                elif message.arbitration_id == RDS:  
                    AudioTunedFrequency   = message.data[0] * 2.00
                    AudioFMFrequencyStep  = message.data[1] * 0.01
                    RadioStation          = (AudioTunedFrequency) + (AudioFMFrequencyStep)
                    AudioTunerBandPreset  = "AM"
                    if message.data[2]   != 0:
                        AudioTunerBandPreset = "FM" 
                        time.sleep(2)  
                        cleanline() 
                        print("Tuner Frequency:", RadioStation, AudioTunerBandPreset)
                        
                elif message.arbitration_id == RDSN:    
                    time.sleep(3)    
                    cleanline() 
                    print(message.data)

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

