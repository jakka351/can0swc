#!/usr/bin/python3
#// Ford FG can0hvac
#// derived from Kyle May & MitchellH's source code available at https://fordforums.com.au/showthread.php?t=11430769 
#
#FG Falcon can-frames used in this example
#https://jakka351.github.io/FG-Falcon/
import RPi.GPIO as GPIO #GPIO Library for LED on GPIO22 on PiCAN2 board
import can 
import time
import os
import uinput #keypress lib for version 1
import queue
from threading import Thread

HVAC                    = 0x353 #can id 851 
HVAC_vent               = 0xAA #0b10101010 
HVAC_actemp             = 0x19 
HVAC_outside            = 0x0C
HVAC_fanspeed           = 0x06

# Vent Status
ventCAN = 0b10101010
# AC Temp
#acTempCAN = 25
## Outside Temp
#outsideTempCAN = 12
# Fan Speed
#char fanSpeedCAN = 6
#len = 0
#buf[8]

# Variables to signal send message
byte Send738 = 0
byte Send783 = 0
byte Send785 = 0
byte Send775 = 0
byte Send777 = 0
byte Send779 = 0
byte Send1372 = 0

#SimpleTimer tmr100ms;


#void setup() {
#  Serial.begin(115200);
#START_INIT:
#    CAN.init();
#    if (CAN_OK != CAN.begin(CAN_500KBPS)) // init can bus : baudrate = 500k
#    {
#        serialp("ERROR:Failed to initialize CAN");
#        delay(10);
#        goto START_INIT;
#    } else {
#        serialp("INFO:LS CAN ready");
#    }
#
#//    tmr100ms.setInterval(100, SetSend100ms);
#}

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native') #bus channel & type refer to python-can docs
except OSError:
    print('can0swc cannot start can0 or can1 interface: can0swc cant get it up: check wiring and config')
    GPIO.output(led,False)
    exit()

def can_rx_task():  # Recv can frames only with CAN_ID specified in SWC variable
    while True:
        message = bus.recv()
        if message.arbitration_id == HVAC: #CAN_ID variable
            q.put(message)          # Put message into queue
            print('')
q = queue.Queue()
rx = Thread(target = can_rx_task)
rx.start()
c = ''
count = 0

time.sleep(0.1)

# Main loop
try:
    while True:
        for i in range(1):
            while(q.empty() == True):       # Wait until there is a message
                pass
            message = q.get()

            c = '{0:f},{1:d},'.format(message.timestamp,count)
            if message.arbitration_id == HVAC and message.data[0] == HVAC_vent:
                print('VENT:'+ ventCAN)
            if message.arbitration_id == HVAC and message.data[0] != HVAC_vent:

                
            if message.arbitration_id == HVAC and message.data[3] == HVAC_actemp:
                print('ACTEMP:'+ acTempCAN)

            if message.arbitration_id == HVAC and message.data[4] == HVAC_outside:
                print('OUTSIDETEMP:'+ outsideTempCAN)

            if message.arbitration_id == HVAC and message.data[7] == HVAC_fanspeed:
                print('FANSPEED:'+ fanSpeedCAN)

#####
#void loop() {
   # if(Serial.available()) {
   #     String incomingserial = Serial.readString();
   #     if (incomingserial.equals("SENDALLDATA") || incomingserial.equals("SENDALLDATA\n") || incomingserial.equals("'SENDALLDATA'") || incomingserial.equals("b'SENDALLDATA'")) {
  #          serialp("VENT:" + String(ventCAN));
  #          serialp("ACTEMP:" + String(acTempCAN, 1));
  #          serialp("OUTSIDETEMP:" + String(outsideTempCAN));
 #           serialp("FANSPEED:" + String(fanSpeedCAN));
 #       } else {
#        serialp("ERROR: Unknown request" + incomingserial);
 #       }
 #   }
time.sleep(0.1)

#    requestHVAC();
#  //  tmr100ms.run();

#    //Process CAN Data
 #   if (CAN_MSGAVAIL == CAN.checkReceive()) {
 #       CAN.readMsgBuf(&len, buf);        // read data,    len: data length, buf: data buf
#
#        //Read CAN Node ID
#        int CANNodeID = CAN.getCanId();#
#
#        // HVAC
        if (CANNodeID == 851) {    
            #//Vent Status
            if (ventCAN != buf[0])
             {
                ventCAN = buf[0];
                serialp("VENT:" + String(ventCAN));
            }
#
#            double val = (double)buf[3] / 2.0;
#            // Temperature Status
#            if (acTempCAN != val) {
#                acTempCAN = val;
#                serialp("ACTEMP:" + String(acTempCAN, 1));
#            }
#
#            // Outside Temp
#            if (outsideTempCAN != buf[4]) {
#                outsideTempCAN = buf[4];
#                serialp("OUTSIDETEMP:" + String(outsideTempCAN));
#            }#
#
#            //Fan Speed
#            if (fanSpeedCAN != buf[7]) {
#                //update data
#                fanSpeedCAN = buf[7];
#                serialp("FANSPEED:" + String(fanSpeedCAN));
#            }
#        }
 #   }
#}

// Requests HVAC info from BEM
void requestHVAC() {

    if (Send738 >= 2) {
        code738function();
        Send738 = 0;
    }

    if (Send775 >= 5) {
        code775function();
        Send775 = 0;
    }

    if (Send783 >= 2) {
        code783function();
        Send783 = 0;
    }

    if (Send785 >= 2) {
        code785function();
        Send785 = 0;
    }

    if (Send777 >= 5) {
        code777function();
        Send777 = 0;
    }

    if (Send779 >= 5) {
        code779function();
        Send779 = 0;
    }
    
    if (Send1372 >= 5) {
        code1372function();
        Send1372 = 0;
    }
}

// Every 100ms updates timer increments for each function
void SetSend100ms() {
    // 200ms
    Send738++;
    Send783++;
    Send785++;

    // 500ms
    Send775++;
    Send777++;
    Send779++;
    Send1372++;
}

// ICC Unit Data Requests:

int reset775 = 0;

void code738function() {
    unsigned char char738[8] = {0, 0, 0, 0, 0, 0, 0, 0};
    CAN.sendMsgBuf(0x2E2, 0, 8, char738);
}

void code1372function() {
    unsigned char char1372[8] = {1, 2, 0, 0, 0, 0, 0, 0};
    CAN.sendMsgBuf(0x55C, 0, 8, char1372);
}

void code783function() {
    unsigned char char783[8] = {31, 31, 31, 31, 31, 0, 0, 0};
    CAN.sendMsgBuf(0x30F, 0, 8, char783);
}

void code785function() {
    unsigned char char785[8] = {31, 148, 31, 31, 31, 31, 0, 33};
    CAN.sendMsgBuf(0x311, 0, 8, char785);
}

void code777function() {
    unsigned char char777[8] = {32, 32, 32, 32, 32, 32, 32, 32};
    CAN.sendMsgBuf(0x309, 0, 8, char777);
}

void code779function() {
    unsigned char char779[8] = {0, 0, 2, 0, 0, 3, 8, 0};
    CAN.sendMsgBuf(0x30B, 0, 8, char779);
}

void code775function() {
    unsigned char char775[8] = {0, 0, 0, 128, 0, 0, 0, 0};
    CAN.sendMsgBuf(0x307, 0, 8, char775);
    if (reset775 == 1) {
        char775[0] = 0;
        char775[1] = 0;
        char775[2] = 0;
        char775[3] = 128;
        char775[4] = 0;
        char775[5] = 0;
        char775[6] = 0;
        char775[7] = 0;
        reset775 = 0;
    }
}

// Serial print function
void serialp(String inputline) {
    String tmpstringoutput = "SL:" + inputline + ":EL";
    Serial.println(tmpstringoutput);
}
