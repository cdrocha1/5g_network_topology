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
HISTORIAN_ADDR = IP['historian']

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
                 print("ERROR: Cannot connect to Port:", port2)
                 port2 += 1
        try:
            # print ("Would you like to redirect health data to Edge Server?")
            # answer = input('')
            # if answer =='yes':
            while True:
                message, addr = sockhealth.recvfrom(1024)
                print(f"Health data received from {addr}: {message.decode()}")
                sockhealth.sendto(message, ('', 504))
                # sockhealth.sendto(message,('10.211.55.3',103))
                message2, addr2 = sockprocess.recvfrom(1024)
                print(f"Process data received from {addr2}: {message2.decode()}")
                
                #sockprocess.sendto(message2,('10.211.55.3',104))
                    
                # if (message and message2):
                #     sockhealth.sendto(b"Health data received by SCADA", addr)
                #     sockprocess.sendto(b"Process data received by SCADA", addr2)

                #firewall to block all messages not labeled "PROCESS" or "ERROR"
                if ("PROCESS" in message2.decode() or "ERROR" in  message2.decode()):
                    sockprocess.sendto(b"Process data received by SCADA", addr2)  #send confirmation to RTU
                    sockprocess.sendto(message2, ('',505))  #send process data to historian
                else:
                    print("SCADA Firewall has blocked packet from ", addr2)
                    sockprocess.sendto(b"SCADA Firewall has blocked packet from: ", addr2)  #send fail message to RTU
                 
        except KeyboardInterrupt:
            pass
        finally:
            #sockhealth.close()
            sockprocess.close()
            
if __name__ == "__main__":

    scada = SCADAServer(
        name='scada',
        state=STATE,
        protocol=SCADA_PROTOCOL)
