

![](https://raw.githubusercontent.com/jakka351/can0swc/main/can.jpg)  
***
# FG Falcon SWC Adapter [![GitHub issues](https://img.shields.io/github/issues/jakka351/can0swc?style=social)](https://github.com/jakka351/can0swc/issues) ![image](https://img.shields.io/badge/github-can0swc-yellowgreen) ![GitHub last commit](https://img.shields.io/github/last-commit/jakka351/can0swc)       



  ### Steering Wheel Controls adaptor for mk1 FG
  
  Uses the python-can library to listen for pushes of steering wheel buttons, which are visible on the Falcon's mid-speed controller area network with CAN ID 0x2F2. Also listens for ICC button pushes on CAN ID 0x2FC and BEM functions on 0x307. When a button is pushed, the script emulates a keypress on the Raspberry Pi. This is used here with [OpenDash's](https://github.com/opendsh/dash) implementation of Android Auto emulator [Openauto]() to control basic media functions. The Car used is an Ford FG mk1 Falcon with, the ICC from the vehicle has had the CD player removed and the main screen replaced with a Raspberry Pi 7 Inch Screen.    
  
  ### [Basic Breakdown of Steering Wheel Controls for FG Falcon](https://github.com/jakka351/FG-Falcon/wiki/Steering-Wheel-Media-Controls)    
                                   
SWC are resistance based, all switches run on a single wire, pushing a button causes a specific resistance in the circuit. The Module sees a change in resistance, and accordingly sends data on to CAN-bus where it is recieved by the ACM/FDIM/ICC and acted upon. 

 --  [Relevant ICC Diagrams + Pinouts](https://github.com/jakka351/FG-Falcon/wiki/Interior-Command-Centre)  
    
  
   
  ### CAN Data  

   | Address | Data    | Function | Byte1      | Byte2      | Byte3 | Byte4 | Byte5 | Byte6 | Byte7   | Byte8   |
| ------- | ----    | -------- | -----      | -----      | ----- | ----- | ----- | ----- | -----   | -----   |
| `754`   | 8 bytes | Volume Data  | 0x00| x | x | x | x | x | x | x |  
| `754`   | 8 bytes | Seek  | x | x | x | x | x | x | x | 0x08* |  
| `754`   | 8 bytes | Volume Up  | x | x | x | x | x | x | x | 0x10* |  
| `754`   | 8 bytes | Volume Down  | x| x | x | x | x | x | x | 0x18* |  
| `754`   | 8 bytes | Phone  | x| x | x | x | x | x | 0x61** | x |  
| `748`   | 8 bytes | Mode  | x| x | x | x | x | x | 0x10 | x |  

***
*+1 depending on audio mode  
**65 or 68 depending on audio mode  
***
  
### Hardware

  
 **Vehicle:** FG Falcon mk1   
 **Interface:** SocketCAN can0 interface, MCP2515 chipset, Midspeed-CAN@125kbps  
 **Software:**  Can-Utils, Python-Can, Openauto, Opendash, Raspbian   
 **SBC:** Raspberry Pi 4B - 8gb, PiCan2 Hat, i2s audio hat  
 **Other:** Modified OBD-DB9 Cable, 7" Official Touchscreen, 2 Metre DSI Ribbon Cable, heatsink case, fans, enclosure, 12vdc-5vdc converter   
  
  #### Unit Diagram  
<img src="https://raw.githubusercontent.com/jakka351/can0swc/main/falcon.png" width="500" height="500" />  
   
  #### Actual Unit 
<img src="https://raw.githubusercontent.com/jakka351/can0swc/main/canpii.jpg" width="300" height="425"> <img src="https://raw.githubusercontent.com/jakka351/can0swc/main/test%20(1).jpg" width="325" height="425" /> 

  


***  
  
### Installation, Dependencies & Config
       
   #### Edit  
   - edit "/etc/modules" to include   
        `uinput`         
        `can`  
        `can_dev`  
        `can_raw`  
        `vcan`  
          
   #### Set Up CAN interface    
   - Add the following to the 'config.txt' file in the /boot partition of the Raspberry Pi sd card.   
       `dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25`    
   - If using a PiCan Board set oscillator to 16000000  
       `oscillator=16000000`  

 - Add the following to '/etc/network/interfaces'   
         `auto can0    `  
         `iface can0 inet manual    `
         `    pre-up /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 100 `    
         `    up /sbin/ifconfig can0 up txqueuelen 65535   `   
         `    down /sbin/ifconfig can0 down `    
   - Bring the can0 interface up  
         `sudo ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 100 `   
         `sudo ifconfig can0 up txqueuelen 65535 ` 
          
   #### Install  
       sudo apt update -y && sudo apt upgrade -y &&
       sudo apt install -y can-utils libsocketcan2 libsocketcan-dev python-can python3-can &&   
       sudo apt install -y python3-uinput python3-evdev &&  
       sudo git clone https://github.com/jakka351/can0swc ./can0swc &&  
       cd ./can0swc &&  
       pip3 install -r requirements.txt &&    
       sudo modprobe uinput &&
       sudo cp ./can0swc.service /lib/systemd/system/can0swc.service &&  
       sudo systemctl enable can0swc.service &&  
       sudo systemctl start can0swc.service &&  
       sudo systemctl status can0swc.service &&  
       sudo reboot
               
   #### Testing with can-utils  
   - Test the script with socketcan virtual can interface, vcan0 and candump log files      
        `sudo modprobe vcan0`  
        `sudo ip link add dev vcan0 type vcan`  
        `sudo ifconfig vcan0 up txqueuelen 1000`  
   - Use canplayer to run the candump log    
        `canplayer -I ./candump.log -v vcan0=can0`  
   - If running cangen use '-L 8' to keep frames at 11bits or an error will occur  
        `cangen vcan0 -c -L 8 &`  
   - Candump logs available [here](https://github.com/jakka351/fg-falcon)  
       
   #### Run Script Manually
        `cd ~/can0swc`  
        `sudo python3 ./can0swc.py`  
        
       
    
  ### Wiring Diagrams
  
  <img src="https://github.com/jakka351/FG-Falcon/blob/master/resources/images/36042a635002807104849f240acc63e5.jpg" width="600" height="600" />    
  <img src="https://raw.githubusercontent.com/jakka351/FG-Falcon/master/resources/images/plug_dlc.png" width="600" height="600" /> 
  
  ### Use in Different Vehicles  
  There is a templated version of the script that can be used to make your own version of can0swc, named as 'template.py'. 
    
  ###  Based upon:  
   -- [Python-CAN PiCAN2 Examples](https://github.com/jakka351/FG-Falcon/tree/master/resources/software/pythoncan)   
   -- [Webjocke canbus to keypress](https://github.com/webjocke/Python-CAN-bus-to-Keypresses) 
   
![](https://www.raspberrypi.org/app/uploads/2017/06/Powered-by-Raspberry-Pi-Logo_Outline-Colour-Screen-500x153.png)  
     
     ██████  █████  ███    ██  ██████  ███████ ██     ██  ██████     
    ██      ██   ██ ████   ██ ██  ████ ██      ██     ██ ██                 
    ██      ███████ ██ ██  ██ ██ ██ ██ ███████ ██  █  ██ ██                 
    ██      ██   ██ ██  ██ ██ ████  ██      ██ ██ ███ ██ ██                 
     ██████ ██   ██ ██   ████  ██████  ███████  ███ ███   ██████            
                                                                          
-
