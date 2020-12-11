import time
import can

bustype = 'socketcan'
channel = 'can0'

def producer(id):
    """:param id: Spam the bus with messages including the data id."""
    bus = can.interface.Bus(channel=channel, bustype=bustype)
    for i in range(10):
        msg = can.Message(arbitration_id=0x2F2, data=[id, i,02,E3,06,4E,08,1D,00,09], is_extended_id=False)
        bus.send(msg)

    time.sleep(1)

producer(10)
