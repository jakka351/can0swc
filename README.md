 

  
# can0swc [![GitHub issues](https://img.shields.io/github/issues/jakka351/can0swc?style=social)](https://github.com/jakka351/can0swc/issues) ![image](https://img.shields.io/badge/github-can0swc-yellowgreen) ![GitHub last commit](https://img.shields.io/github/last-commit/jakka351/can0swc)       
  


  ### Steering Wheel Controls CAN adaptor for mk1 FG Falcon     
  Uses the python-can library to listen for the pushes of the media controls on the steering wheel, which are visible on the Falcon's mid-speed controller area network with CAN ID 0x2F2. Also listens ICC button pushes on CAN ID 0x2FC and BEM functions on 0x307. When a specific data frame matches, the script emulates a key press, which is used here with [OpenDash's](https://github.com/opendsh/dash) implementation of Android Auto emulator [Openauto]() to control basic media functions. The Car used is an FPV FG mk1 Falcon with 5.4L & tr6060, the ICC from the vehicle has had the 6 stacker CD player removed and the main screen replaced with a Raspberry Pi 7' Screen, so CAN data may be slightly different to other models.  
  
  ### [Basic Breakdown of Steering Wheel Controls for FG Falcon](https://github.com/jakka351/FG-Falcon/wiki/Steering-Wheel-Media-Controls)    
     
SWC are resistance based, all switches run on a single wire, pushing a button causes a specific resistance in the circuit. The Module reads the resistance, interprets and sends data on to CAN-bus where it is recieved by the ACM/FDIM/ICC and acted upon.  
  
   
  #### CAN Data
   | Address | Data    | Function | Byte1      | Byte2      | Byte3 | Byte4 | Byte5 | Byte6 | Byte7   | Byte8   |
| ------- | ----    | -------- | -----      | -----      | ----- | ----- | ----- | ----- | -----   | -----   |
| `754`   | 8 bytes | Volume Data  | 0x00| x | x | x | x | x | x | x |  
| `754`   | 8 bytes | Seek  | x | x | x | x | x | x | x | 0x08 |  
| `754`   | 8 bytes | Volume Up  | x | x | x | x | x | x | x | 0x10 |  
| `754`   | 8 bytes | Volume Down  | x| x | x | x | x | x | x | 0x18 |  
| `754`   | 8 bytes | Phone  | x| x | x | x | x | x | 0x61 | x |  


   ### Hardware  
  Vehicle: fg falcon mk1 ms-can@125kbps  
  Interface: RPi4 + mcp2515(PiCAN2 Hat) using SPI + socketcan      
  
### Installation, Dependencies & Config
   - Install Dependencies  
       >> `sudo apt install c-yan-utils libsocketcan2 libsocketcan-dev python-can python3-can`  
         
       >> `sudo apt install -y python3-uninput python3-evdev`  
         
       >> `pip3 install regex`  
   
  ### Edit configuration files  
   - edit "/etc/modules" to include   
       >> `uinput`
         
   #### Set Up CAN interface    
   - Add the following to the 'config.txt' file in the /boot partition of the Raspberry Pi sd card.   
        >>`dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25`    
   - Add the following to '/etc/network/interfaces'   
        >>  `auto can0    `  
        >>  `iface can0 inet manual    `
        >>  `    pre-up /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 100 `    
        >>  `    up /sbin/ifconfig can0 up txqueuelen 65535   `   
        >>  `    down /sbin/ifconfig can0 down `  
         
    
    
  ### Wiring Diagrams
  #### SWC  
![diagram](https://github.com/jakka351/FG-Falcon/blob/master/resources/images/36042a635002807104849f240acc63e5.jpg)  
  #### pi  
![](https://raw.githubusercontent.com/jakka351/FG-Falcon/master/resources/images/rpican.png)   
  
  ###  Based upon:  
   -- [Python-CAN PiCAN2 Examples](https://github.com/jakka351/FG-Falcon/tree/master/resources/software/pythoncan)   
   -- [Webjocke canbus to keypress](https://github.com/webjocke/Python-CAN-bus-to-Keypresses) 
   
  
     ██████  █████  ███    ██  ██████  ███████ ██     ██  ██████          
    ██      ██   ██ ████   ██ ██  ████ ██      ██     ██ ██               
    ██      ███████ ██ ██  ██ ██ ██ ██ ███████ ██  █  ██ ██               
    ██      ██   ██ ██  ██ ██ ████  ██      ██ ██ ███ ██ ██               
     ██████ ██   ██ ██   ████  ██████  ███████  ███ ███   ██████          
                                                                           
     
