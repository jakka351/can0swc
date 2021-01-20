#!/usr/bin/python3
#// Ford FG can0hvac
#https://github.com/jakka351/FG-Falcon/
#pip3 install regex uinput evdev os queue python-can time
import can 
import time
import os
import uinput 
import queue
import sys, traceback
from threading import Thread
#############################
#outfile = open('log.txt','w')
############################
############################
# define keys
#device                 = uinput.Device([
#                        uinput.KEY_VOLUMEUP
#                       ])
############################

############################
# define CAN identifiers
IC                     = 0x128              #296
SWC                    = 0x2F2              #754
SWC2                   = 0x2EC              #748 for MODE button
ICC                    = 0x2FC              #764 icc bttons
BEM                    = 0x403
############################
# define CAN frame data
SWC_SEEK               = 0x09               #frame 8 2F2 # [02] [E3] [06] [4E] [08] [1D] [00] [09]
SWC_VOLUP              = 0x11               #frame 8 2F2 # 02 E3 06 4E 08 1D 00 11
SWC_VOLDOWN            = 0x19               #frame 8 2F2 # 02 E3 06 4E 08 1D 00 19
SWC_PHONE              = 0x68               #frame 7 2F2 # 02 E3 06 4E 08 1D 68 00     
SWC_MODE0              = 0x01
SWC_MODE1              = 0x48 #72               #
SWM_MODE2              = 0x10 #16
############################
IC_HL                  = 0               #headlights 296 x1
IC_IND                 = 0                   #indicators 296 x4 
############################
BEM_BCI                = 0                #body control info 1027 x1
BEM_LOCK               = 0                # b0dy control info 1027 x2 #//code127 x2 = unlocked with remote, 2=unlocked, 0=locked.
BEM_UNLOCK             = 0                #bci 1027 x7      
CABNLGHT               = 0                  # 1030 x2 cabin light
IGNST                  = 0                  # 1030 x3 ignition state
###
#HighBeamStatus
#FogLampStatus
#ParkAndLowBeamStatus
#AutoHeadlampSwitchStatus
#IllumLevelDisplay
#IllumLevelSwitch
#TurnStalkSwitchStatus
#RearBeltMinderStatus
#Headlights On
#Lights On Auto
#LightsOn
#FogLampOn
#High Beams on
#Left Indicator
#Right Indicator
#ParkBrakeOn_MS
###
###775 HazardSwitch
#RFD_Ajar
#LFD_Ajar
#RRD_Ajar
#LRD_Ajar
#BootTailgateAjar
#Head_lamp_fail
#HazardOnRequest
#Priority_key_1 and Priority_key_2
#SmartShieldLED_Request
#IllumMode
#BonnetAjar
#RFD_Locked
#SeatbeltStatusRearLeft
#SeatbeltStatusRearLeft
#SeatbeltStatusRearCentre
#SeatbeltStatusRearRight
############################
HVAC                    =  0x353 #can id 851 
HVAC_off                =  0xAB  #  [5] A 129 0 0 34 [171] 0 0    All Off
HVAC_TEMP               =  0     #851 x4
HVAC_OUT                =  0     #Outside Temp 851 x5
HVAC_FANSPEED           =  0     #Fan speed 851 x8
HVAC_VENTSTATUS         =  0     #Vent tatus 851 x1
VA                      =  0x4B  # print('Foot Vents, Close Cabin')
VB                      =  0x2B  # print('Foot Vents, Open Cabin')
VC                      =  0x2F  # print('Window and Feet Vets, Open Cabin')
VD                      =  0x4F  # print('Window and Feet Vents, Close Cabin')
VE                      =  0x5B  # print('Face, Foot, Close Cabin')
VF                      =  0x3B  # print('Face, Foot, Open Cabin')
VG                      =  0x33  # print('Face, Open Cabin')
VH                      =  0x53  # print('Face, Close Cabin')
VI                      =  0x27  # print('Window, Manual Fan')
VJ                      =  0x26  # print('Window, Auto Fan')
VK                      =  0x83  # print('A/C Off, Open Cabin')
VL                      =  0x8B  # print('A/C Off, Foot Vents, Open Cabin')
VM                      =  0x8F  # print('A/C Off, Foot and Window Vents, Open Cabin')
VN                      =  0x9B  # print('A/C Off, Foot and Face Vents, Open Cabin')
VO                      =  0xA6  # print('A/C Off, Window Vents, Open Cabin')
VP                      =  0xA7  # print('A/C Off, Manual Fan, Open Cabin')
VQ                      =  0xC3  # print('A/C Off, Close Cabin')
VR                      =  0xCB  # print('A/C Off, Foot Vents, Close Cabin')
VS                      =  0xCF  # print('A/C Off, Foot and Window Vents, Close Cabin')
VT                      =  0xDB  # print('A/C Off, Foot and Face Vents, Close Cabin')
VU                      =  0x43  # print('Auto, Close Cabin')
VW                      =  0x23  # print('Auto, Open Cabin')
#############################
#764 icc
#Default (Audio Controls) (Audio Off State)
#Eject CD
#Load CD
#SCN/AS Button
#CD/AUX Button
#FM/AM Button
#Volume Down
#Volume Up
#Seek Down
#Seek Up
#Menu Button
#OK Button
#Power Button
#Audio On State
#Audio Off State
#############################
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan') #bus channel & type refer to python-can docs

    time.sleep(0.05)

    print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')

    time.sleep(0.05)
    
    print(' ███████  ██████      ███████  █████  ██       ██████  ██████  ███    ██ ')
    time.sleep(0.05)
    print(' ██      ██           ██      ██   ██ ██      ██      ██    ██ ████   ██ ')
    time.sleep(0.05)
    print(' █████   ██   ███     █████   ███████ ██      ██      ██    ██ ██ ██  ██ ')
    time.sleep(0.05)
    print(' ██      ██    ██     ██      ██   ██ ██      ██      ██    ██ ██  ██ ██ ')
    time.sleep(0.05)
    print(' ██       ██████      ██      ██   ██ ███████  ██████  ██████  ██   ████ ')
    time.sleep(1.0)

    print('    ╔═╗╦ ╦╔╦╗╦ ╦╔═╗╔╗╔   ╔═╗╔═╗╔╗╔  ╦ ╦╦  ╦╔═╗╔═╗  ╔═╗╔═╗╦═╗╦╔═╗╔╦╗')
    time.sleep(0.08)
    print('    ╠═╝╚╦╝ ║ ╠═╣║ ║║║║───║  ╠═╣║║║  ╠═╣╚╗╔╝╠═╣║    ╚═╗║  ╠╦╝║╠═╝ ║ ')
    time.sleep(0.08)
    print('    ╩   ╩  ╩ ╩ ╩╚═╝╝╚╝   ╚═╝╩ ╩╝╚╝  ╩ ╩ ╚╝ ╩ ╩╚═╝  ╚═╝╚═╝╩╚═╩╩   ╩ ')

    print('         ')

    print('               https://github.com/jakka351/fg-falcon')

    print('          ')
    time.sleep(0.08)


    print('  ┌─┐┌─┐┌┐┌┌┬┐┬─┐┌─┐┬  ┬  ┌─┐┬─┐  ┌─┐┬─┐┌─┐┌─┐  ┌┐┌┌─┐┌┬┐┬ ┬┌─┐┬─┐┬┌─  ')
    time.sleep(0.15)
    print('  │  │ ││││ │ ├┬┘│ ││  │  ├┤ ├┬┘  ├─┤├┬┘├┤ ├─┤  │││├┤  │ ││││ │├┬┘├┴┐  ')
    time.sleep(0.15)
    print('  └─┘└─┘┘└┘ ┴ ┴└─└─┘┴─┘┴─┘└─┘┴└─  ┴ ┴┴└─└─┘┴ ┴  ┘└┘└─┘ ┴ └┴┘└─┘┴└─┴ ┴  ')
    time.sleep(0.15)
    print('                                                                                    ')
    time.sleep(0.5)
    print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')
    time.sleep(4.0)        
    os.system('cansend can0 353#4B.00.00.0F.16.00.00.04')                                                
except OSError:
    print('can0swc cannot start can0 or can1 interface: can0swc cant get it up: check wiring and config')
    #GPIO.output(led,False)
    exit()#

############################
def can_rx_task1():  # Recv can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == SWC: #CAN_ID variable
            q.put(message)          # Put message into queue
        if message.arbitration_id == SWC2: #CAN_ID variable   
            q.put(message)   
            print(message)
#############################

#############################
def can_rx_task2():  # Recv can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == HVAC: #CAN_ID variable
            q.put(message)          # Put message into queue
#############################

#############################
def can_rx_task3():  # Recv can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == ICC: #CAN_ID variable
            q.put(message)          # Put message into queue
#############################

#############################
def can_rx_task4():  # Recv can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == BEM: #CAN_ID variable
            q.put(message)          # Put message into queu
        if message.arbitration_id == IC: #CAN_ID variable
            q.put(message)          # Put message into queue
#############################
#############################
#//TX CAN Codes
#unsigned char char738[8] = {0, 0, 0, 0, 0, 0, 0, 0};
#unsigned char char764[8] = {0, 0, 1, 0, 31, 0, 2, 4};
#int reset775 = 0;
#int reset789 = 0;
#//Default 775 is (0, 0, 0, 128, 0, 0, 0, 0) - set 2nd to 16 to turn AC off at startup
#//Removed - restet to default
#unsigned char char775[8] = {0, 0, 0, 128, 0, 0, 0, 0};
#
#unsigned char char787[8] = {148, 0, 0, 0, 0, 0, 0, 0};
#unsigned char char789[8] = {0, 0, 0, 4, 128, 0, 0, 0};
#/*
#/  789:
 # X4 = Follow me home lighting
#  X5 = Autoheadlight settings


#def can_tx_task():  # Transmit thread
 #   while True:
  #      msg = can.Message(arbitration_id=0x307,data=[0x00,0x00,0x00,0x80,0x00,0x00,0x00,0x00],extended_id=False)
   #     bus.send(msg)
  #      time.sleep(0.05)#738

#        msg = can.Message(arbitration_id=0x2FC,data=[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],extended_id=False)
 #       bus.send(msg)
   #     time.sleep(0.05)#764

        #msg = can.Message(arbitration_id=0x307,data=[0x00,0x00,0x00,0x80,0x00,0x00,0x00,0x00],extended_id=False)
    #    bus.send(msg)
    #    time.sleep(0.05)#775

      #  msg = can.Message(arbitration_id=0x313,data=[0x94,0x00,0x00,0x00,0x00,0x00,0x00,0x00],extended_id=False)
       # bus.send(msg)
     #   time.sleep(0.05)#787

     #   msg = can.Message(arbitration_id=0x315,data=[0x00,0x00,0x04,0x80,0x00,0x00,0x00,0x00],extended_id=False)
    #    bus.send(msg)
      #  time.sleep(0.05)#789

       # time.sleep(0.1)
########
q = queue.Queue()
rx = Thread(target = can_rx_task1)
rx.start()
rx2 = Thread(target = can_rx_task2)
rx2.start()
rx3 = Thread(target = can_rx_task3)
rx3.start()
rx4 = Thread(target = can_rx_task4)
rx4.start()
#tx = Thread(target = can_tx_task)
#tx.start()
########
#count     = 0
#c         = ''
#cabntemp  = 0
#outstemp  = 0 
#watrtemp = 0
#ventstat  = 0
#fanspeed  = 0
time.sleep(0.1)
#############################
# Main loop
try:
    while True:
        for i in range(1):
            while(q.empty() == True):       # Wait until there is a message
                pass
### 0x353
            message = q.get()
            if message.arbitration_id == HVAC and message.data[3] != HVAC_TEMP:
                print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')
                print('                                          ╔═╗╦╦═╗╔═╗╔═╗╔╗╔  ╔╦╗╔═╗╔╦╗╔═╗  ┌─┐')
                print('                                          ╠═╣║╠╦╝║  ║ ║║║║   ║ ║╣ ║║║╠═╝  │  ')
                print('                                          ╩ ╩╩╩╚═╚═╝╚═╝╝╚╝   ╩ ╚═╝╩ ╩╩    └─┘')
                print(message.data[3] / 2)
 #               print('Cabin Temperature:', cabntemp + message.data[3] / 2)
  #              cabntemp = message.data[3] / 2
                time.sleep(0.1)

            if message.arbitration_id == HVAC and message.data[4] != HVAC_OUT:
                print('                                                      ───  ───  ───  ───  ───   ───  ')
                print('                                          ╔╦╗╔═╗╔╦╗╔═╗  ╔═╗╦ ╦╔╦╗╔═╗╦╔╦╗╔═╗  ┌─┐')
                print('                                           ║ ║╣ ║║║╠═╝  ║ ║║ ║ ║ ╚═╗║ ║║║╣   │  ')
                print('                                           ╩ ╚═╝╩ ╩╩    ╚═╝╚═╝ ╩ ╚═╝╩═╩╝╚═╝  └─┘')
                print(message.data[4])
                time.sleep(0.1)

            if message.arbitration_id == HVAC and message.data[7] != HVAC_FANSPEED:
                print('                                                      ───  ───  ───  ───  ───   ───  ')
                print('                                          ╔═╗╔═╗╔╗╔  ╔═╗╔═╗╔═╗╔═╗╔╦╗  ')
                print('                                          ╠╣ ╠═╣║║║  ╚═╗╠═╝║╣ ║╣  ║║  ')
                print('                                          ╚  ╩ ╩╝╚╝  ╚═╝╩  ╚═╝╚═╝═╩╝  ')
                print(message.data[7])
                time.sleep(0.1)

            if message.arbitration_id == HVAC and message.data[0] != HVAC_VENTSTATUS:
                print('                                                      ───  ───  ───  ───  ───   ───  ')
                print('                                         ╦  ╦╔═╗╔╗╔╔╦╗  ╔═╗╔╦╗╔═╗╔╦╗╦ ╦╔═╗')
                print('                                         ╚╗╔╝║╣ ║║║ ║   ╚═╗ ║ ╠═╣ ║ ║ ║╚═╗')
                print('                                          ╚╝ ╚═╝╝╚╝ ╩   ╚═╝ ╩ ╩ ╩ ╩ ╚═╝╚═╝')
                if message.data[0] == VA:
                 print('Foot Vents, Close Cabin')
                if message.data[0] == VB:
                 print('Foot Vents, Open Cabin')
                if message.data[0] == VC: 
                 print('Window and Foot Vents, Open Cabin')
                if message.data[0] == VD:
                 print('Window and Foot Vents, Close Cabin')
                if message.data[0] == VE:
                 print('Face, Foot, Close Cabin')
                if message.data[0] == VF:
                 print('Face, Foot, Open Cabin')
                if message.data[0] == VG:
                 print('Face, Open Cabin')
                if message.data[0] == VH: 
                 print('Face, Close Cabin')
                if message.data[0] == VI: 
                 print('Window, Manual Fan')
                if message.data[0] == VJ: 
                 print('Window, Auto Fan')
                if message.data[0] == VK:
                 print('A/C Off, Open Cabin')
                if message.data[0] == VL:
                 print('A/C Off, Foot Vents, Open Cabin')
                if message.data[0] == VM:
                 print('A/C Off, Foot and Window Vents, Open Cabin')
                if message.data[0] == VN:
                 print('A/C Off, Foot and Face Vents, Open Cabin')
                if message.data[0] == VO:
                 print('A/C Off, Window Vents, Open Cabin')
                if message.data[0] == VP:
                 print('A/C Off, Manual Fan, Open Cabin')
                if message.data[0] == VQ:
                 print('A/C Off, Close Cabin')
                if message.data[0] == VR:
                 print('A/C Off, Foot Vents, Close Cabin')
                if message.data[0] == VS:
                 print('A/C Off, Foot and Window Vents, Close Cabin')
                if message.data[0] == VT:
                 print('A/C Off, Foot and Face Vents, Close Cabin')
                if message.data[0] == VU:
                 print('Auto, Close Cabin')
                if message.data[0] == VW:
                 print('Auto, Open Cabin')
                time.sleep(0.1) 
                print('                                                                                    ')
                print('───────────────────────────────────────────────────  ───  ───  ───  ───  ───   ───  ')

            if message.arbitration_id == HVAC and message.data[5] == HVAC_off:
                print('AC Off')
                time.sleep(1.0)

            if message.arbitration_id == HVAC and message.data[1] != 0:
               pass
            if message.arbitration_id == HVAC and message.data[2] != 0:
               pass
            if message.arbitration_id == HVAC and message.data[6] != 0:
               pass
##### 0x2F2
            while(q.empty() == True):                                     # wait until there is a message
                pass
            message = q.get()
            if message.arbitration_id == SWC and message.data[7] == SWC_SEEK:
                device.emit_click(uinput.KEY_VOLUMEUP)
                print('| can0swc:seek                                                    |')
                print(message.data)

            if message.arbitration_id == SWC and message.data[7] == SWC_VOLUP:
                device.emit_click(uinput.KEY_VOLUMEUP)
                print('| can0swc:volup                                                   |')
                print(message.data)

            if message.arbitration_id == SWC and message.data[7] == SWC_VOLDOWN:
                device.emit_click(uinput.KEY_VOLUMEUP)
                print('| can0swc:voldown                                                 |')
                print(message)

            if message.arbitration_id == SWC and message.data[6] == SWC_PHONE:
                device.emit_click(uinput.KEY_VOLUMEUP)
                print('| can0swc:phone                                                   |')
                print(message)
#### 748
            if message.arbitration_id == SWC and message.data[7] == SWC_MODE0 and message.data[6] == SWC_MODE1:
                message = q.get()
                if message.arbitration_id == SWM and message.data[7] == SWM_MODE2:
                 print('| can0swc:mode button                                                 |')
### 0x403
            if message.arbitration_id == BEM and message.data[0] != IC_HL:
                print('Headlight Setting:',message.data[0])
                print(message.data[0])
                time.sleep(1.0)

            if message.arbitration_id == BEM and message.data[3] != IC_IND:
                print('Indicators:', message.data[3])
              # if message.data[3] == A
               # print('Right')
              # if message.data[3] == B
               # print('Left')
                print(message.data)
                time.sleep(1.0)
### 0x406
            elif message.arbitration_id != SWC or SWM or HVAC or BEM or IC:
                pass
   #     count += 1
 
############################

############################
# end
except KeyboardInterrupt:
    exit()
except Exception:
    traceback.print_exc(file=sys.stdout)
    exit()
except OSError:
    exit()   
############################
# can0hvac
############################


