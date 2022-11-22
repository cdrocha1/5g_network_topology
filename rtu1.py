
"""
swat-s1 rtu1
"""

from minicps.devices import RTU, PLC
from utils import RTU1_DATA, STATE, RTU1_PROTOCOL
from utils import RTU_SAMPLES, RTU_PERIOD_SEC
from utils import IP

import time
import socket


RTU1_ADDR = IP['rtu1']
RTU2_ADDR = IP['rtu2']
RTU3_ADDR = IP['rtu3']
#RTU4_ADDR = IP['rtu4']
SCADA_ADDR = IP['scada']
#CTRL_ADDR = IP['controller']

LIT301_3 = ('LIT301', 3)


class SwatRTU1(RTU):

    #def pre_loop(self, sleep=0.1):
    #    print ('DEBUG: project topo rtu1 enters pre_loop')
    #    print

    #    time.sleep(sleep)

    def main_loop(self):
        """rtu1 main loop.

            - read UF tank level from the sensor
            - update internal enip server
        """
        
    def listen(ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            print("UDP sending on Port:", port)
            sock.settimeout(5)
            while True:
                print("Message for server: ")
                msg = input('')
                sock.sendto(msg.encode(), (ip, port))
                #print("message sent")
                #print("waiting for response on socket")
                if(msg != 'Bye'):
                    data, addr = sock.recvfrom(1024)
                    print(msg, data.decode())
                else:
                    data, addr = sock.recvfrom(1024)
                    print(data.decode())
                    sock.close()
                    sys.exit()
        except socket.timeout:
            print("ERROR: acknowledgement was not received")
        except Exception as ex:
            print("ERROR:", ex)
            #finally:
                #sock.close()

    listen('', 502)

if __name__ == "__main__":

    # notice that memory init is different form disk init
    rtu1 = SwatRTU1(
        name='rtu1',
        state=STATE,
        protocol=RTU1_PROTOCOL,
        memory=RTU1_DATA,
        disk=RTU1_DATA)
