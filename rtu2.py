
"""
swat-s1 rtu2
"""

from minicps.devices import RTU, PLC
from utils import RTU2_DATA, STATE, RTU2_PROTOCOL
from utils import RTU_SAMPLES, RTU_PERIOD_SEC
from utils import IP

import time
import socket
import sys


RTU1_ADDR = IP['rtu1']
RTU2_ADDR = IP['rtu2']
RTU3_ADDR = IP['rtu3']
#RTU4_ADDR = IP['rtu4']
SCADA_ADDR = IP['scada']
#CTRL_ADDR = IP['controller']

LIT301_3 = ('LIT301', 3)


class SwatRTU2(RTU):

    def pre_loop(self, sleep=0.1):
        print ('DEBUG: project topo rtu2 enters pre_loop')
        print

        time.sleep(sleep)

    def main_loop(self):
        """rtu2 main loop.

            - read UF tank level from the sensor
            - update internal enip server
        """

        print ('DEBUG: swat-s1 rtu2 enters main_loop.')
        print

        count = 0
        while(count <= RTU_SAMPLES):

            lit301 = float(self.get(LIT301_3))
            print ("DEBUG RTU - get lit301: %f" % lit301)

            self.send(LIT301_3, lit301, RTU2_ADDR)

            time.sleep(RTU_PERIOD_SEC)
            count += 1

        print ('DEBUG swat rtu2 shutdown')

    def listen(ip, port, port2):
        sockhealth = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockprocess = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            print("UDP sending data on Port:", port)
            sockhealth.settimeout(5)
            while True:
                print("Health data for server: ")
                msg = input('')
                sockhealth.sendto(msg.encode(), (ip, port))

                print('Process data for server: ')
                msg2 = input('')
                sockprocess.sendto(msg2.encode(), (ip, port2))

                if(msg != 'Bye'):
                    data, addr = sockhealth.recvfrom(1024)
                    print(msg, data.decode())
                    data2, addr2 = sockprocess.recvfrom(1024)
                    print(msg2, data2.decode())

                else:
                    data, addr = sockhealth.recvfrom(1024)
                    print(data.decode())
                    data2, addr2 = sockprocess.recvfrom(1024)
                    print(msg2, data2.decode())
                    sockhealth.close()
                    sockprocess.close()
                    sys.exit()
        except socket.timeout:
            print("ERROR: acknowledgement was not received")
        except Exception as ex:
            print("ERROR:", ex)
            #finally:
                #sock.close()
    listen('', 502,503)
if __name__ == "__main__":

    # notice that memory init is different form disk init
    rtu2 = SwatRTU2(
        name='rtu2',
        state=STATE,
        protocol=RTU2_PROTOCOL,
        memory=RTU2_DATA,
        disk=RTU2_DATA)
