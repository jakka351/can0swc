#!/usr/bin/python3
#can0swc
#FG Falcon can-frames used in this example
#https://jakka351.github.io/FG-Falcon/
import RPi.GPIO as GPIO                     # gpio library for LED on GPIO22 on PiCAN2 board
import can 
import time
import os
import uinput                               # keypress library 
import queue
from threading import Thread
import sys, traceback

############################
# gpio setup
led = 22                                    # gpio on the pican2 board has LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,True)
############################


############################
# define keys
device = uinput.Device([
                                            # android auto keyboard buttons
        uinput.KEY_N, #Next Track
#        uinput.KEY_PREVIOUSSONG,
#        uinput.KEY_PLAYPAUSE,
        uinput.KEY_VOLUMEUP, #Volup
        uinput.KEY_VOLUMEDOWN, #Voldown
        uinput.KEY_P, #Phone Button
#        uinput.KEY_M, #Google Voice
#        uinput.KEY_O, #Call End
#        uinput.KEY_H, #Home
#        uinput.KEY_X, #Play
#        uinput.KEY_C, #Pause
#        uinput.KEY_B, #Toggle Play    
#        uinput.KEY_ESC, #ESC       
#        uinput.KEY_ENTER, #Enter
                                            #opendash shortcuts
        uinput.KEY_Q, #AA page
        uinput.KEY_W, #Vehicle Page
        uinput.KEY_E, #Media Page
        uinput.KEY_R, #Launcher Page
        uinput.KEY_T, #Camera Page
        uinput.KEY_Y, #Toggle Dark Mode
        uinput.KEY_K, #U vol
        uinput.KEY_L, #L vol
        ])
############################

############################
# define CAN identifiers
BEM                    = 0x128              #296
SWC                    = 0x2F2              #754
SWM                    = 0x2EC              #748 for MODE button
HVAC                   = 0x353              #can id 851 

############################

############################
# define CAN frame data
SWC_SEEK               = 0x09               #frame 8 2F2 # [02] [E3] [06] [4E] [08] [1D] [00] [09]
SWC_VOLUP              = 0x11               #frame 8 2F2 # 02 E3 06 4E 08 1D 00 11
SWC_VOLDOWN            = 0x19               #frame 8 2F2 # 02 E3 06 4E 08 1D 00 19
SWC_PHONE              = 0x68               #frame 7 2F2 # 02 E3 06 4E 08 1D 68 00     
SWC_MODE               = 0xFF               #
############################

#//Headlights
296X1                  = 0
#//Indicators
296X4                  = 0
#//Vent Status
851X1                  = 0
#//AC Temp
851X4                  = 0
#//Outside Temp
851X5                  = 0
#//Fan Speed
851X8                  = 0
#//Body Control Info
1027X1                 = 0
1027X2                 = 0
#//Lock State
1027X7                 = 0
#//code127 x2 = unlocked with remote, 2=unlocked, 0=locked.
#//Ignition State
1030X2                 = 0
# Cabin Lights
1030X3                 = 0

############################
# print 
print('|=================================================================|')
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
#   
print('|                                                                 |')
print('|=================================================================|')
print('|                                                                 |')                                                            #fg ms-can is 125kbps hs-can is 500kbps
os.system("sudo /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 100 loopback on")
os.system("sudo /sbin/ifconfig can0 up txqueuelen 65535")
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
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native') 
    print('|  socketcan configured...awaiting can frames.....                |')
    print('|=================================================================|')
    print('|                                                                 |')
    print('')     # channel = interface, bustype = socketcan 
except OSError:
    print('can0swc cannot find can interface. check wiring and config')
    GPIO.output(led,False)
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
                print('|                                                                 |')
                print('|                                                                 |')
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
      device.emit_click(uinput.KEY_N) 
      device.emit_click(uinput.KEY_Q) 
      print('|                                                                 |')
      print('| can0swc:seek                                                    |')
      print(message)

     if message.arbitration_id == SWC and message.data[7] == SWC_VOLUP:
      device.emit_click(uinput.KEY_VOLUMEUP)
      device.emit_click(uinput.KEY_L) 
      print('|                                                                 |')
      print('| can0swc:volup                                                   |')
      print(message)

     if message.arbitration_id == SWC and message.data[7] == SWC_VOLDOWN:
      device.emit_click(uinput.KEY_VOLUMEDOWN)
      device.emit_click(uinput.KEY_K) 
      print('|                                                                 |')
      print('| can0swc:voldown                                                 |')
      print(message)

     if message.arbitration_id == SWC and message.data[6] == SWC_PHONE:
      device.emit_click(uinput.KEY_W)
      device.emit_click(uinput.KEY_P)
      print('|                                                                 |')
      print('| can0swc:phone                                                   |')
      print(message)

     if message.arbitration_id == SWC or message.arbitration_id == SWM and message.data[6] == SWC_PHONE:
      device.emit_click(uinput.KEY_W)
      device.emit_click(uinput.KEY_P)
      print('|                                                                 |')
      print('| can0swc:mode                                                    |')
      print(message)

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

     if message.arbitration_id == BEM and message.data[0] != 296X1:
      print('Headlight Setting:' + message.data[0])
      print(message.data[x])
      time.sleep(1.0)


     if message.arbitration_id == BEM and message.data[3] != 296X4:
      print('Indicators:' + message.data[3]
      print(message.data[x])
      time.sleep(1.0)

      #//296-X1 = Headlight Setting
    #if (CANNodeID == 296)
    #{
     # //Only use X1, X4
      #if (code296X1 != buf[0])
      #{
      #  //Send New Setting
      #  serialp("Headlights:" + String(buf[0]));
     #3   //Update Code Memory
     #   code296X1 = buf[0];
      #}
     # //296-X4 = Indicator Setting
    #  if (code296X4 != buf[3])
   #   {
  #      serialp("Indicators:" + String(buf[3]));
  #      code296X4 = buf[3];
 #     }
#      //PrintCANMessage(CANNodeID, buf, len);
    

    #if message.arbitration_id == HVAC:
#    print('')
             #   time.sleep(1.0)   

    elif message.arbitration_id != SWC and message.data[7] != SWC_SEEK:
      print('0x2f2 ID')
      time.sleep(0.5) 
      print('no data')
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

