 

# can0swc [![GitHub issues](https://img.shields.io/github/issues/jakka351/can0swc?style=social)](https://github.com/jakka351/can0swc/issues) ![image](https://img.shields.io/badge/github-can0swc-yellowgreen) ![GitHub last commit](https://img.shields.io/github/last-commit/jakka351/can0swc)       
  

  ## Steering Wheel Controls CAN adaptor for mk1 FG Falcon     
  listens for the can frame specific to the swc button and then emits a keyboard press 
  
  ####[Basic Breakdown of Steering Wheel Controls for FG Falcon](https://github.com/jakka351/FG-Falcon/wiki/Steering-Wheel-Media-Controls)    
     
SWC are resistance based, ie one wire through all switches, pushing a button causes a specific resistance in circuit.  Module reads the resistance, interprets and sends data on to CAN-bus.
  
  #### CAN Data
   | Address | Data    | Function | Byte1      | Byte2      | Byte3 | Byte4 | Byte5 | Byte6 | Byte7   | Byte8   |
| ------- | ----    | -------- | -----      | -----      | ----- | ----- | ----- | ----- | -----   | -----   |
| `754`   | 8 bytes | Complex  | 0x02 | 0xE3 | 0x06 | 0x4E | 0x08 | 0x1D | 0x00 | 0x00|

  ### Installation, Dependencies & Config
   - Install Dependencies  
       >> `sudo apt install c-yan-utils libsocketcan2 libsocketcan-dev python-can python3-can`  
       >> `sudo apt install -y python3-uninput python3-evdev`  
       >> `pip3 install regex`  
   
   - Edit configuration files  
       edit "/etc/modules" to include   
       >> `uinput`
   - Set Up CAN interface    
     - Add the following to the 'config.txt' file in the /boot partition of the Raspberry Pi sd card.   
        >>`dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25`    
     - Add the following to '/etc/network/interfaces'   
         `auto can0    `  
         `iface can0 inet manual    `
         `    pre-up /sbin/ip link set can0 type can bitrate 125000 triple-sampling on restart-ms 100 `    
         `    up /sbin/ifconfig can0 up txqueuelen 65535   `    
         `    down /sbin/ifconfig can0 down `  
         
  ### Hardware  
  Vehicle: fg falcon mk1 ms-can@125kbps  
  Interface: RPi4 + mcp2515(PiCAN2 Hat) using SPI + socketcan    
    
    
  ### Wiring Diagrams
![diagram](https://github.com/jakka351/FG-Falcon/blob/master/resources/images/36042a635002807104849f240acc63e5.jpg)  
  
![](https://raw.githubusercontent.com/jakka351/FG-Falcon/master/resources/images/rpican.png)   
  
  ###  Based upon:  
   -- [Python-CAN PiCAN2 Examples](https://github.com/jakka351/FG-Falcon/tree/master/resources/software/pythoncan)   
   -- [Webjocke canbus to keypress](https://github.com/webjocke/Python-CAN-bus-to-Keypresses) 
   
  
     ██████  █████  ███    ██  ██████  ███████ ██     ██  ██████          
    ██      ██   ██ ████   ██ ██  ████ ██      ██     ██ ██               
    ██      ███████ ██ ██  ██ ██ ██ ██ ███████ ██  █  ██ ██               
    ██      ██   ██ ██  ██ ██ ████  ██      ██ ██ ███ ██ ██               
     ██████ ██   ██ ██   ████  ██████  ███████  ███ ███   ██████          
                                                                           
     
