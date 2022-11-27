
"""
swat-s1 rtu2
"""

from minicps.devices import RTU, PLC
from utils import RTU3_DATA, STATE, RTU3_PROTOCOL
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


class SwatRTU3(RTU):

    def pre_loop(self, sleep=0.1):
        print ('DEBUG: project topo rtu2 enters pre_loop')
        print

        time.sleep(sleep)

    def main_loop(self):
        """rtu2 main loop.

            - read UF tank level from the sensor
            - update internal enip server
        """

        #print ('DEBUG: swat-s1 rtu2 enters main_loop.')
        #print

        #count = 0
        #lit301 = 0.456
        #while(count <= RTU_SAMPLES):
        #	if lit301 <=20:
        #		print ("Tank filling - get lit301: %f" % lit301)
        #	else:
        #		print ("lit301 filling - get lit301: %f" % lit301)
        	
        #	lit301 += 2.554
        #	time.sleep (RTU_PERIOD_SEC)
        #	count += 1
        	
        #print ('DEBUG swat rtu2 shutdown')
        #print ("lit301 filling - get lit301: %f" % lit301)
    def listen(ip, port, port2):
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
    listen(ip=sys.argv[1], port=int(sys.argv[2]), port2=int(sys.argv[3]))

if __name__ == "__main__":

    # notice that memory init is different form disk init
    rtu3 = SwatRTU3(
        name='rtu3',
        state=STATE,
        protocol=RTU3_PROTOCOL,
        memory=RTU3_DATA,
        disk=RTU3_DATA)
