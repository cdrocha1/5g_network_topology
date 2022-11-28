
"""
swat-s1 rtu2
"""

from minicps.devices import RTU, PLC
from utils import RTU2_DATA, STATE, RTU2_PROTOCOL
from utils import RTU_SAMPLES, RTU_PERIOD_SEC
from utils import IP

import random
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

    def listen(ip, ip2, port, port2):
        sockhealth = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockprocess = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        health_data_options = ["temp sensor: working as expected, RTU working as expected", "temp sensor: Needs maintanence"]
        
        temp = 45
        try:
            print("UDP sending health data on Port:", port)
            print("UDP sending process data on Port: ", port2)
            sockhealth.settimeout(5)
            sockprocess.settimeout(5)
            while True:

                
                if(temp >= 0 and temp < 999):
                    health_data = health_data_options[0]
                else:
                    health_data = health_data_options[1]
                
                temp += random.randint(-5,10)
                process_data = "Temp in Celcius: " + str(temp)

                # print("Health data for server: ")
                # msg = input('')
                #sockhealth.sendto(health_data.encode(), (ip, port))
                sockhealth.sendto(health_data.encode(), (ip2, port))

                # print('Process data for server: ')
                # msg2 = input('')
                sockprocess.sendto(process_data.encode(), (ip, port2))
                data, addr = sockhealth.recvfrom(1024)
                print(health_data, data.decode())
                #print(msg, data.decode())
                
                data2, addr2 = sockprocess.recvfrom(1024)
                print(process_data, data2.decode())
                #print(msg2, data2.decode())

                time.sleep(2)


        except socket.timeout:
            print("ERROR: acknowledgement was not received")
        except Exception as ex:
            print("ERROR:", ex)
            #finally:
                #sock.close()
    listen(ip=sys.argv[1], ip2=sys.argv[2], port=int(sys.argv[3]), port2=int(sys.argv[4]))

if __name__ == "__main__":

    # notice that memory init is different form disk init
    rtu2 = SwatRTU2(
        name='rtu2',
        state=STATE,
        protocol=RTU2_PROTOCOL,
        memory=RTU2_DATA,
        disk=RTU2_DATA)
