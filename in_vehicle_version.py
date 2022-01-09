import can,time,os,queue
from threading import Thread
import sys,traceback
print('\n#@@@@@@@@@#++++++++++@@@#++++++++%@@%+++++@@@@@@@+++#@@@++++++++++%@@%++++++++++++@%+++%@@@@@@@@+++#@@@++++++++++#@@@@@@@@@@@@\n#@@@@@@@@@*----------@@@*--------#@@#-----@@@@@@@---*@@@----------#@@#------------@#---#@@@@@@@@---*@@@----------*@@@@@@@@@@@@\n#@@@@@@@%=--#%%%%%%%%@%=--#%%%%*-==@#-----=+@@@@@---*@+=-=%%%=----==@#---#%%%%%%%%@#---#@@@@@@@@---*@+=-=%%%%%%%%@@@@@@@@@@@@@\n#@@@@@@@#---#@@@@@@@@@#---#%%%%*---@#---==-=%@@@@---*@=--=@@%=-=----@#---#%%%%%%%%@#---#@@@%@@@@---*@=--=@@@@@@@@@@@@@@@@@@@@@\n#@@@@@@@#---#@@@@@@@@@#------------@#---#@---*@@@---*@=--=@*---@*---@#------------@#---#@@#-*@@@---*@=--=@@@@@@@@@@@@@@@@@@@@@\n#@@@@@@@#---#@@@@@@@@@#---+++++=---@#---#@++-+#%@---*@=--=#+-++@*---@%++++++++=---@#---#@#*-+#%@---*@=--=@@@@@@@@@@@@@@@@@@@@@\n#@@@@@@@#---#@@@@@@@@@#---#@@@@*---@#---#@@#---#@---*@=------#@@*---@@@@@@@@@@*---@#---#@-----#@---*@=--=@@@@@@@@@@@@@@@@@@@@@\n#@@@@@@@%#+-+++++++++@#---#@@@@*---@#---#@@%#+-++---*@##-----+++=-*#@%++++++++=---@%#+-++-=#+-++-=#%@##-=++++++++#@@@@@@@@@@@@\n#@@@@@@@@@*----------@#---#@@@@*---@#---#@@@@*------*@@@----------#@@#------------@@@*----=@*----=@@@@@----------*@@@@@@@@@@@@ \n    ')
print('                                  I??+=++=~~~~~~~~~~~?I777IIII??++====~======????+==+==~~~~:::::::::~~~~~~~~~====+==I,     ')
print('                                   ?I+=~~=++~~~~~~~~=?=:+IIIII??++++===~:~~~~~~~=???=?:=~~~~~::::::::~~~~~~~~~~=~=+?7~:    ')
print('                                    ?+=~~~~=++~~~~~+???~=?7II??+++++++==~~:~~~~~~:~~???=+:~~~~~~:::::::::~~~~=++:,.,+=,,   ')
print('                                     =?I+~~~==++~~:+??~====+I?+===+++++==~~~::::::::::~????~~~~~:::::~:~==+:,,,,?..::+=:   ')
print('                                       =?I=~~~==++=+++~==:,~~=+====+++++:,,...:,::~:::::~~~~+~:~~:~~==,.,,.?I~,..::~~=,:   ')
print('                                        ~=+I?=~~=~+++~~=...,~:=+====++?:~+=?I~,I=I??..~III7I:==~,.,,.,,.,,,...::~~++~:~:   ')
print('                                           ~?I+=~~~~+~~~.:+,,,:=+===+++~+==~=+:III=?I?77777I~~~===,,,,.,.,,~~~~=+=~::,,:   ')
print('                                             ~?I+=:~~~~~~,,+:,,+==~+++++,:~~:==,??,:,,=??I++,,,:~===,,,::~~=++=:::~=..,,   ')
print('                                          ,,,,:=+?==~~~~.=:~~,..,=+++++=~:=+=~:.,:,,,,::?=I=:::::+~====++++=~:::?I+?,..,   ')
print('                                           :,,,,~+====~:,,,:=,.,,,~~===~~~,:==~~~~~~:..,,,,,,..,,,~==+++~:,~++I++II?...    ')
print('                                            :,,,,,,+==+,:..:==.:,,~:~~~~~:,,,,:~~~~~~~~=========~++++~,....II+II+?...,:    ')
print('                                              ,,,,,,,++.,,.,,,,=:,,~:::~:::,,,,,,,,,::~~~=====~====~.......?I=I.....,:~    ')
print('                                                ::,,,,,,:~::,~+I+,..~::::::,,,,,,,,,,,,,,,,,~==~~~.........+.......,:,,    ')
print('\n This is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by\n the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This is distributed in the hope \n that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  \n See the GNU General Public License for more details. You should have received a copy of the GNU General Public License\n along with this file.  If not, see <https://www.gnu.org/licenses/>. \n ')
time.sleep(1)
c=''
count=0
SWC=754
SWM=748
ICC=764
BEM=775
SWC_SEEK=8,9,12
SWC_VOLUP=16,17,20
SWC_VOLDOWN=24,25,28
SWC_PHONE=97,98,99,100,101,102,103,104,193,194,195,196,197,198,199,200
SWC_MODE=16
AUX=1,2,65,66,71
CDMP3=3,67
PHONE=6,70
RADIO=5,4,68,69
AUDIOOFF=8,72
ICC_VOLUP=65
ICC_VOLDOWN=129
ICC_NEXT=4
ICC_PREV=8
ICC_EJECT=128
ICC_LOAD=64
BEM_HAZARD=1
def scroll():print('  ');print('  \n             ,777I77II??~++++=~::,,,,::::::::::~~~==+~                                        \n           ,IIIIII,IIII+~..,,:,,,,,:~:,,.....,~,,:::~+?+?=                                    \n         :=I7777I=IIIIII~...:===,:,=~:,,,,,,::=,,,:::~~:=?===                                 \n      ~=,?I?777II7IIIII=~,.,,,,,,,,,,,:,,,,,,::,,,,~:~~~~:~+:~:~                              \n      I=I?IIIIII~IIIIIII+:..,,,,,,,,,,,,.,.,,::.,,,,:::~~=~:=+~?~~               \n      I77?+?IIIIIIIII7I7=~,.,,,..,,,,.,.,.......,.,.,.,..,,,:~=~:==~~                         \n     +=I7777I?+???IIIIII+=:..,,,,,,,,,,,...,,,,,,,,,,,,..,,,:..:?I7+...,,                     \n     +=+=I7777I=~~+~:~IIII~,..,,,,,,,,,,..,,,,,...~+II?I?+?III7IIII777I7=.....                \n      ==++++III=~~~::~+I:+?~:.........:+IIIIIIII+=?IIIIIII???????????III7II7I....             \n     ?+=  ██████\u2001 █████\u2001 ███\u2001   ██\u2001 ██████\u2001 ███████\u2001██\u2001    ██\u2001██████++++???II?III....         \n     ?+= ██\u2001\u2001\u2001\u2001\u2001\u2001██\u2001\u2001\u2001██\u2001████\u2001  ██\u2001██\u2001\u2001████\u2001██\u2001\u2001\u2001\u2001\u2001\u2001██\u2001    ██\u2001██\u2001\u2001\u2001\u2001\u2001======++?II?+7II.         \n     ??+ ██\u2001     ███████\u2001██\u2001██\u2001 ██\u2001██\u2001██\u2001██\u2001███████\u2001██\u2001 █\u2001 ██\u2001██\u2001    ~~~~======+???++II.       \n     ??+ ██\u2001     ██\u2001\u2001\u2001██\u2001██\u2001\u2001██\u2001██\u2001████\u2001\u2001██\u2001\u2001\u2001\u2001\u2001\u2001██\u2001██\u2001███\u2001██\u2001██\u2001    ~~~~~~~~~===++++=II,      \n     I??  ██████\u2001██\u2001  ██\u2001██\u2001 \u2001████\u2001\u2001██████\u2001\u2001███████\u2001\u2001███\u2001███\u2001\u2001\u2001██████:::~~~~~~~~~====+==I,     \n      ?I+=~~fg+falcon+swc+adapter+??++++===~:~~~~~~~=???=?:=~~~~~::::::::~~~~~~~~~~=~=+?7~:    \n       ?+=~~~~=++~~~~~+???~=?7II??+++++++==~~:~~~~~~:~~???=+:~~~~~~:::::::::~~~~=++:,.,+=,, \n        =?I+~~~==++~~:+??~====+I?+===+++++==~~~::::::::::~????~~~~~:::::~:~==+:,,,,?..::+=:   \n          =?I=~~~==++=+++~==:,~~=+====+++++:,,...:,::~:::::~~~~+~:~~:~~==,.,,.?I~,..::~~=,:   \n           ~=+I?=~~=~+++~~=...,~:=+====++?:~+=?I~,I=I??..~III7I:==~,.,,.,,.,,,...::~~++~:~:   \n              ~?I+=~~~~+~~~.:+,,,:=+===+++~+==~=+:III=?I?77777I~~~===,,,,.,.,,~~~~=+=~::,,:   \n                ~?I+=:~~~~~~,,+:,,+==~+++++,:~~:==,??,:,,=??I++,,,:~===,,,::~~=++=:::~=..,,   \n             ,,,,:=+?==~~~~.=:~~,..,=+++++=~:=+=~:.,:,,,,::?=I=:::::+~====++++=~:::?I+?,..,   \n              :,,,,~+====~:,,,:=,.,,,~~===~~~,:==~~~~~~:..,,,,,,..,,,~==+++~:,~++I++II?...    \n               :,,,,,,+==+,:..:==.:,,~:~~~~~:,,,,:~~~~~~~~=========~++++~,....II+II+?...,:    \n                 ,,,,,,,++.,,.,,,,=:,,~:::~:::,,,,,,,,,::~~~=====~====~.......?I=I.....,:~    \n                   ::,,,,,,:~::,~+I+,..~::::::,,,,,,,,,,,,,,,,,~==~~~.........+.......,:,,    ')
def setup():
    global bus
    try:bus=can.interface.Bus(channel='vcan0',bustype='socketcan_native')
    except OSError:sys.exit()
    print('                      ');print('        CANbus active on',bus);print('        waiting for matching can frame...');print('        ready to emit keypress...')
def msgbuffer():
    global message,q,SWC,ICC,BEM
    while True:
        message=bus.recv()
        if message.arbitration_id==SWC:q.put(message)
def displaytext():0
def cleardtc():0
def demister():0
def backlite():0
def bluetoothpair():0
def cleanline():sys.stdout.write('\x1b[1A');sys.stdout.write('\x1b[2K')
def cleanscreen():os.system('clear')
def ccp():cleanline();cleanline();print(message)
def main():
    E='SWCPhoneBtn pushed @';D='SWCVolDownBtn pushed @';C='SWCVolUpBtn pushed @';B='SWCSeekBtn pushed @'
    try:
        while True:
            for F in range(8):
                while q.empty()==True:0
                A=q.get();G='{0:f},{1:d},'.format(A.timestamp,count)
                if A.arbitration_id==SWC and A.data[6]in AUX:
                    if A.arbitration_id==SWC and A.data[7]in SWC_SEEK:ccp();print(B,A.timestamp)
                    elif A.arbitration_id==SWC and A.data[7]in SWC_VOLUP:time.sleep(0.2);ccp();print(C,A.timestamp)
                    elif A.data[7]in SWC_VOLDOWN:ccp();print(D,A.timestamp)
                    elif A.arbitration_id==SWC and A.data[6]in SWC_PHONE:ccp();print(E,A.timestamp)
                    else:0
                elif A.arbitration_id==SWC and A.data[6]in RADIO:
                    if A.arbitration_id==SWC and A.data[7]in SWC_SEEK:ccp();print(B,A.timestamp)
                    elif A.arbitration_id==SWC and A.data[7]in SWC_VOLUP:time.sleep(0.2);ccp();print(C,A.timestamp)
                    elif A.data[7]in SWC_VOLDOWN:ccp();print(D,A.timestamp)
                    elif A.arbitration_id==SWC and A.data[6]in SWC_PHONE:ccp();print(E,A.timestamp)
                    else:0
                elif A.arbitration_id==SWC and A.data[6]in PHONE:0
                else:0
    except KeyboardInterrupt:sys.exit(0)
    except Exception:traceback.print_exc(file=sys.stdout);sys.exit()
    except OSError:sys.exit()
if __name__=='__main__':q=queue.Queue();rx=Thread(target=msgbuffer);cleanscreen();scroll();setup();rx.start();main()
