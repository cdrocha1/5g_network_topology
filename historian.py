"""
historian.py
"""

from minicps.devices import SCADAServer
from utils import SCADA_PROTOCOL, STATE
from utils import SCADA_PERIOD_SEC
from utils import IP
from utils import CO_0_2a, CO_1_2a, CO_2_2a, CO_3_2a
from utils import HR_0_2a
import socket
import time
import datetime

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']
RTU1_ADDR = IP['rtu1']
RTU2_ADDR = IP['rtu2']
RTU3_ADDR = IP['rtu3']
# RTU4_ADDR = IP['rtu4']
SCADA_ADDR = IP['scada']
HISTORIAN_ADDR = IP['historian']

def format_hist(msg, addr):
            t = datetime.datetime.now()
            formatted = "Message: '" + msg + "' -From: " + addr[0] + ":" + str(addr[1]) + " -To SCADA on: " + str(t) +"\n"
            return formatted

class Historian(SCADAServer):

    def pre_loop(self, sleep=0.5):
        """scada pre loop.
            - sleep
        """

        time.sleep(sleep)

    
    
        
    def main_loop(self):
        sockhealth = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockprocess = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        port = 504
        port2 = 505
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
                print(f"Health data received from {addr}: {message.decode()}")
                message2, addr2 = sockprocess.recvfrom(1024)
                print(f"Process data received from {addr2}: {message2.decode()}")
                
                if (message and message2):
                    #sockhealth.sendto(b"Health data received by SCADA", addr)
                    #sockprocess.sendto(b"Process data received by SCADA", addr2)


                    health_history = format_hist(message.decode(), addr)
                    process_history = format_hist(message2.decode(), addr2)
                    try:
                        with open('health_data.txt','a') as h, open('process_data.txt','a') as p:
                        
                            h.write(str(health_history))
                            p.write(str(process_history))
                            
                            
                    except:
                        print("error writing to historian")

                        

            
        except KeyboardInterrupt:
            pass
        finally:
            sockhealth.close()
            sockprocess.close()
            h.close()
            p.close()

    

if __name__ == "__main__":

    SCADAServer = Historian(
        name='historian',
        state=STATE,
        protocol=SCADA_PROTOCOL)
