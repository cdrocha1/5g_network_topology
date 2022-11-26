
"""
swat-s1 rtu1
"""

from minicps.devices import RTU, PLC
from utils import RTU1_DATA, STATE, RTU1_PROTOCOL
from utils import RTU_SAMPLES, RTU_PERIOD_SEC
from utils import IP

import random
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
        
    def listen(ip, port, port2):
        sockhealth = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockprocess = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        health_data_options = ["temp sensor: working as expected, RTU working as expected", "temp sensor: Needs maintanence"]
        
        temp = 45
        try:
            print("UDP sending data on Port:", port)
            sockhealth.settimeout(5)
            while True:

                
                if(temp >= 0 and temp < 999):
                    health_data = health_data_options[0]
                else:
                    health_data = health_data_options[1]
                
                temp += random.randint(-5,10)
                process_data = "Temp in Celcius: " + str(temp)

                # print("Health data for server: ")
                # msg = input('')
                sockhealth.sendto(health_data.encode(), (ip, port))

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
    listen('', 502,503)

if __name__ == "__main__":

    # notice that memory init is different form disk init
    rtu1 = SwatRTU1(
        name='rtu1',
        state=STATE,
        protocol=RTU1_PROTOCOL,
        memory=RTU1_DATA,
        disk=RTU1_DATA)
