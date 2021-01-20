#!/usr/bin/python3
#can0swc
#FG Falcon can-frames used in this example
#https://jakka351.github.io/FG-Falcon/
#import RPi.GPIO as GPIO                     # gpio library for LED on GPIO22 on PiCAN2 board
import can
import serial
import time
import os
import uinput
#import evdev
import queue
from threading import Thread
import sys, traceback

############################
# gpio setup
#led = 22                                    # gpio on the pican2 board has LED
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(led,GPIO.OUT)
#GPIO.output(led,True)
############################


############################
# define keys
#device                 = uinput.Device([
 #                        uinput.KEY_VOLUMEUP
  #                       ])
############################
# define CAN identifiers
IC                     = 0x128              #296
SWC                    = 0x2F2              #754
SWM                    = 0x2EC              #748 for MODE button
#ICC                    =
HVAC                   = 0x353              #can id 851 
BEM                    = 0x403               #1027
############################

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
HVAC_VENTSTATUS        = 0          #Vent tatus 851 x1
HVAC_TEMP              = 0                   #851 x4
HVAC_OUT               = 0                #Outside Temp 851 x5
HVAC_FANSPEED          = 0               #Fan speed 851 x8
############################
BEM_BCI                = 0                #body control info 1027 x1
BEM_LOCK               = 0                # b0dy control info 1027 x2 #//code127 x2 = unlocked with remote, 2=unlocked, 0=locked.
BEM_UNLOCK             = 0                #bci 1027 x7      
_CABLIGHT              = 0                  # 1030 x2 cabin light
_IGNSTATE              = 0                  # 1030 x3 ignition state
############################
HVAC_off               =  0xAB #  [5] A 129 0 0 34 [171] 0 0    All Off
HVAC_vent_face         =  16 #[1] by 16
HVAC_vent_feet         =  8 #[1] by 8
HVAC_vent_window0      =  4 #[1] by 4
HVAC_vent_window1      =  2 #[1] by 2
#HVAC_cabin_open         =  #[1] by 32
#HVAC_cabin_closed       =  #[1] by 64
#HVAC_demisterfront      = 
#HVAC_demisterrear       = 
#HVAC_fan_autooff        = #[1] by 1
#HVAC_actemp             = message.data[3] #[4] = AC temp * 2
#HVAC_outside            = message.data[4] #[5]
#HVAC_fanspeed           = message.data[7] #[8] 0-10 0=fan off 10=full speed fan
#HVAC_fanspeedauto       = 0x # [8] +128
#HVAC_fan0  =  0x00 #  [7] 129 0 0 34 X Y 0  Fan Only - Off   
#HVAC_fan1  =  0x01 #  [7] 129 0 0 34 X Y 1  Fan Only - Speed 1
#HVAC_fan2  =  0x02 #  [7] 129 0 0 34 X Y 2  Fan Only - Speed 2
#HVAC_fan3  =  0x03 #  [7] 129 0 0 34 X Y 3  Fan Only - Speed 3
#HVAC_fan4  =  0x04 #  [7] 129 0 0 34 X Y 4  Fan Only - Speed 4
#HVAC_fan5  =  0x05 #  [7] 129 0 0 34 X Y 5  Fan Only - Speed 5
#HVAC_fan6  =  0x06 #  [7] 129 0 0 34 X Y 6  Fan Only - Speed 6
#HVAC_fan7  =  0x07 #  [7] 129 0 0 34 X Y 7  Fan Only - Speed 7
#HVAC_fan8  =  0x08 #  [7] 129 0 0 34 X Y 8  Fan Only - Speed 8
#HVAC_fan9  =  0x09 #  [7] 129 0 0 34 X Y 9  Fan Only - Speed 9
#HVAC_fan10 =  0x10 #  [7] 129 0 0 34 X Y 10 Fan Only - Speed 10
#A 129 0 0 34 X Y Z  Y Increases when Fan On - Possibly RPM
#HVAC_auto  =  0x90 #  [7] 2 129 0 0 34 X Y [144]    Full Auto
#HVAC_FVCC  =  0x4B #  [0] A = 75  Feet Vents, Close Cabin
##HVAC_FVOC  =  0x2B #  [0] A = 43  Feet Vents, Open Cabin
#HVAC_WFOC  =  0x2F #  [0] A = 47  Window and Feet Vents, Open Cabin
#HVAC_WFCC  =  0x4F #  [0] A = 79  Window and Feet Vents, Close Cabin

############################
# print 
print('|=================================================================|')


print("|    ██████  █████  ███    ██  ██████  ██  ██████  ██████         |")
print("|   ██      ██   ██ ████   ██ ██  ████ ██ ██      ██              |")
print("|   ██      ███████ ██ ██  ██ ██ ██ ██ ██ ██      ██              |")
print("|   ██      ██   ██ ██  ██ ██ ████  ██ ██ ██      ██              |")
print("|    ██████ ██   ██ ██   ████  ██████  ██  ██████  ██████         |")


print('|                                                                 |')
print('|    ██████  █████  ███    ██  ██████  ███████ ██     ██  ██████  |')
print('|   ██      ██   ██ ████   ██ ██  ████ ██      ██     ██ ██       |')
print('|   ██      ███████ ██ ██  ██ ██ ██ ██ ███████ ██  █  ██ ██       |')
print('|   ██      ██   ██ ██  ██ ██ ████  ██      ██ ██ ███ ██ ██       |')
print('|    ██████ ██   ██ ██   ████  ██████  ███████  ███ ███   ██████  |')
print('|                                                                 |')
print('|=================================================================|')
print('|                                                                 |')
print('|         fg-falcon steering wheel media controls                 |')
print('|         github.com/jakka351/FG-Falcon                           |')
print('|=================================================================|')
############################

############################
# can0 up @ 125kbps
print('|                                                                 |')
print('|=================================================================|')
print('|                                                                 |')                                                            #fg ms-can is 125kbps hs-can is 500kbps
#os.system("sudo /sbin/ip link set can0 type vcan bitrate 125000 triple-sampling on restart-ms 100 loopback on")
#os.system("sudo /sbin/ifconfig can0 up txqueuelen 65535")
############################

############################
# sleep
time.sleep(0.1)
print('|                                                                 |')
print('|=================================================================|')
print('|                                                                 |')
print('| can0swc:                                                        |')
time.sleep(0.1)
############################


############################
# socketcan parameters
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan')
    print('|  socketcan configured...awaiting can frames.....                |')
    print('|=================================================================|')
    print('|                                                                 |')
    print('')     # channel = interface, bustype = socketcan 
except OSError:
    print('can0swc cannot find can interface. check wiring and config')
 #   GPIO.output(led,False)
    exit()
############################

############################
# can rx 
def can_rx_task():                                               # rx can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == SWC:                        # CAN_ID variable
            q.put(message)  
        if message.arbitration_id == SWM:                        # CAN_ID variable
            q.put(message)                                       # put message into queue
        if message.arbitration_id == BEM:                        # CAN_ID variable
            q.put(message)                                       # put message into queue
        if message.arbitration_id == HVAC:                        # CAN_ID variable
            q.put(message)                                       # put message into queue
        if message.arbitration_id == IC:                        # CAN_ID variable
            q.put(message)                                       # put message into queue

############################

############################
# rxqueue vars
q = queue.Queue()
rx = Thread(target = can_rx_task)
rx.start()
############################

############################
# main loop
try:
 while(q.empty() == True):                                     # wait until there is a message
   pass
 message = q.get()
 if message.arbitration_id == SWC and message.data[7] == SWC_SEEK:  
  device.emit_click(uinput.KEY_VOLUMEUP)
  print('|                                                                 |')
  print('| can0swc:seek                                                    |')
  print(message.data)

 if message.arbitration_id == SWC and message.data[7] == SWC_VOLUP:
  device.emit_click(uinput.KEY_VOLUMEUP)
  print('|                                                                 |')
  print('| can0swc:volup                                                   |')
  print(message.data)

 if message.arbitration_id == SWC and message.data[7] == SWC_VOLDOWN:
  device.emit_click(uinput.KEY_VOLUMEUP)
  print('|                                                                 |')
  print('| can0swc:voldown                                                 |')
  print(message)

 if message.arbitration_id == SWC and message.data[6] == SWC_PHONE:
  device.emit_click(uinput.KEY_VOLUMEUP)
  print('|                                                                 |')
  print('| can0swc:phone                                                   |')
  print(message)

 if message.arbitration_id == SWC and message.data[7] == SWC_MODE0 & message.data[6] == SWC_MODE1:
  message = q.get()
  if message.arbitration_id == SWM and message.data[7] == SWM_MODE2:
   print('| can0swc:mode button                                                 |') 
 
 if message.arbitration_id == HVAC:
  print('AC Temp:')
  print(message.data[3] / 2)
  time.sleep(1.0)

 if message.arbitration_id == HVAC:
  print('Outside Temp:')
  print(message.data[4])
  time.sleep(1.0)

 if message.arbitration_id == HVAC:
  print('Fan Speed:')
  print(message.data[7])
  time.sleep(1.0)

 if message.arbitration_id == HVAC and message.data[5] == HVAC_off:
  print('AC Off')
  time.sleep(1.0)

 if message.arbitration_id == BEM and message.data[0] != IC_HL:
  print('Headlight Setting:', message.data[0])
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

 elif message.arbitration_id != SWC or SWM or HVAC or BEM or IC:
  time.sleep(0.5)
  pass
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
# can0swc
############################


