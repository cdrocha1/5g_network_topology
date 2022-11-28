
"""
swat-s1 plc2
"""

from minicps.devices import PLC
from utils import PLC2_DATA, STATE, PLC2_PROTOCOL
from utils import PLC_SAMPLES, PLC_PERIOD_SEC
from utils import IP

import random
import time
import socket
import sys

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']

FIT201_2 = ('FIT201', 2)


class SwatPLC2(PLC):

    def pre_loop(self, sleep=0.1):
        print ('DEBUG: swat-s1 plc2 enters pre_loop')
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc2 main loop.

            - read flow level sensors #2
            - update interal enip server
        """

        print('DEBUG: swat-s1 plc2 enters main_loop.')
        print

        count = 0
        while(count <= PLC_SAMPLES):

            fit201 = float(self.get(FIT201_2))
            print("DEBUG PLC2 - get fit201: %f" % fit201)

            self.send(FIT201_2, fit201, PLC2_ADDR)
            # fit201 = self.receive(FIT201_2, PLC2_ADDR)
            # print "DEBUG PLC2 - receive fit201: ", fit201

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        print('DEBUG swat plc2 shutdown')
    # port 501

    def plc_data(ip, port):
        sock_plc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sockhealth = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sockprocess = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        health_data_options = [
            "HEALTH - temp sensor: working as expected", "HEALTH - temp sensor: Needs maintanence"]

        temp = 45
        try:
            #print("UDP sending health data on Port:", port)
            #print("UDP sending process data on Port: ", port2)
            # sockhealth.settimeout(5)
            # sockprocess.settimeout(5)
            print("UDP sending health and process data on Port:", port)
            # sock_plc.settimeout(5)
            while True:

                if(temp >= 0 and temp < 999):
                    health_data = health_data_options[0]
                else:
                    health_data = health_data_options[1]

                temp += random.randint(-5, 10)
                process_data = "PROCESS - Temp in Celcius: " + str(temp)

                # print("Health data for server: ")
                # msg = input('')
                #sockhealth.sendto(health_data.encode(), (ip, port))
                #sockhealth.sendto(health_data.encode(), (ip2, port))
                sock_plc.sendto(health_data.encode(), (ip, port))
                print("sent", health_data)

                sock_plc.sendto(process_data.encode(), (ip, port))
                print("sent", process_data)

                time.sleep(2)

        except socket.timeout:
            print("ERROR: acknowledgement was not received")
        except Exception as ex:
            print("ERROR:", ex)
            # finally:
            # sock.close()
    plc_data(ip=sys.argv[1], port=int(sys.argv[2]))


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc2 = SwatPLC2(
        name='plc2',
        state=STATE,
        protocol=PLC2_PROTOCOL,
        memory=PLC2_DATA,
        disk=PLC2_DATA)
