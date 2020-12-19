  

# can0swc [![GitHub issues](https://img.shields.io/github/issues/jakka351/can0swc?style=social)](https://github.com/jakka351/can0swc/issues)  
**Catch can frames and throw keypresses.** ![image](https://img.shields.io/badge/github-can0swc-yellowgreen) ![GitHub last commit](https://img.shields.io/github/last-commit/jakka351/can0swc) [![GitHub issues](https://img.shields.io/github/issues/jakka351/FG-Falcon?style=social)](https://github.com/jakka351/FG-Falcon/issues)      
  
   
   ### Work in progress ###
  Basic python script that filters for a specific can id and then listens for specific data frames from that can id, then does an action. CANbus data used is for a mk1 fg falcon and is yet to be tested in vehicle yet due to HL and VP being C.     
  
  ### can0swc - steering wheel media buttons ###  
  listens for the can frame specific to the swc button and then emits a keyboard press defined start of script  
    
   ### can0hvac - air conditioner status printer & controller #### 
   started today  
     
  ### Dependencies ###  
  python-can (sudo apt install python-can)  
  keyboard()
  uinput  
  
    
  ### Hardware ###
  Vehicle: fg falcon mk1 ms-can@125kbps, hs-can@500kbps  
  Interface: RPi4 + mcp2515(PiCAN2 Hat, china mcp2515 board) + SPI + socketcan  
  
    
 ![image](https://www.crowdsupply.com/img/24a9/python-can_png_project-body.jpg)    
  
  Based upon:  
   -- [Python-CAN PiCAN2 Examples](https://github.com/jakka351/FG-Falcon/tree/master/resources/software/pythoncan)   
   -- [Webjocke canbus to keypress](https://github.com/webjocke/Python-CAN-bus-to-Keypresses) 
  
     ██████  █████  ███    ██  ██████  ███████ ██     ██  ██████          
    ██      ██   ██ ████   ██ ██  ████ ██      ██     ██ ██               
    ██      ███████ ██ ██  ██ ██ ██ ██ ███████ ██  █  ██ ██               
    ██      ██   ██ ██  ██ ██ ████  ██      ██ ██ ███ ██ ██               
     ██████ ██   ██ ██   ████  ██████  ███████  ███ ███   ██████          
                                                                           
     
