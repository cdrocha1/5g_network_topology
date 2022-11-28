"""
scada.py
"""

from minicps.devices import SCADAServer
from utils import SCADA_PROTOCOL, STATE
from utils import SCADA_PERIOD_SEC
from utils import IP
from utils import CO_0_2a, CO_1_2a, CO_2_2a, CO_3_2a
from utils import HR_0_2a

import time
import socket
import sys


PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']
RTU1_ADDR = IP['rtu1']
RTU2_ADDR = IP['rtu2']
RTU3_ADDR = IP['rtu3']
#RTU4_ADDR = IP['rtu4']
SCADA_ADDR = IP['scada']

class SCADAServer(SCADAServer):

    def pre_loop(self, sleep=0.5):
        """scada pre loop.

            - sleep
        """

        time.sleep(sleep)


    def main_loop(self):
        """scada main loop.

        For each RTU in the network
            - Read the pump status
        """	
        sockhealth = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockprocess = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        port = 502
        port2 = 503
        while True:
            try:
                sockhealth.bind(('',port))
                sockprocess.bind(('', port2))
                
                print ("Listening on port", port)
                print ("Listening on port", port2)

                break
            except Exception:
                 print("ERROR: Cannot connect to Port:", port)
                 port += 1
        try:
            while True:
                message, addr = sockhealth.recvfrom(1024)
                #print('THIS IS ADDRESSSSSSSSSSSSSS', addr)
                print(f"Health data received from {addr}: {message.decode()}")
                sockhealth.sendto(message, ('', 504))
                message2, addr2 = sockprocess.recvfrom(1024)
                print(f"Process data received from {addr2}: {message2.decode()}")
                sockprocess.sendto(message2, ('',505))
                
                if (message and message2):
                    sockhealth.sendto(b"Health data received by SCADA", addr)
                    sockprocess.sendto(b"Process data received by SCADA", addr2)

        
        except KeyboardInterrupt:
            pass
        finally:
            sockhealth.close()
            sockprocess.close()
            
if __name__ == "__main__":

    scada = SCADAServer(
        name='scada',
        state=STATE,
        protocol=SCADA_PROTOCOL)
