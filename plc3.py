
"""
swat-s1 plc3
"""

from minicps.devices import PLC
from utils import PLC3_DATA, STATE, PLC3_PROTOCOL
from utils import PLC_SAMPLES, PLC_PERIOD_SEC
from utils import IP

import random
import time
import socket
import sys

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']

LIT301_3 = ('LIT301', 3)


class SwatPLC3(PLC):

    def pre_loop(self, sleep=0.1):
        print ('DEBUG: swat-s1 plc3 enters pre_loop')
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc3 main loop.

            - read UF tank level from the sensor
            - update internal enip server
        """

        print('DEBUG: swat-s1 plc3 enters main_loop.')
        print

        count = 0
        while(count <= PLC_SAMPLES):

            lit301 = float(self.get(LIT301_3))
            print("DEBUG PLC3 - get lit301: %f" % lit301)

            self.send(LIT301_3, lit301, PLC3_ADDR)

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        print('DEBUG swat plc3 shutdown')
    # port 501

    def plc_data(ip, port):
        sock_plc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sockhealth = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sockprocess = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        health_data_options = [
            "HEALTH - volume sensor: working as expected", "HEALTH - volume sensor: Needs maintanence"]

        volume = 45
        try:
            #print("UDP sending health data on Port:", port)
            #print("UDP sending process data on Port: ", port2)
            # sockhealth.settimeout(5)
            # sockprocess.settimeout(5)
            print("UDP sending health and process data on Port:", port)
            # sock_plc.settimeout(5)
            while True:

                if(volume >= 0 and volume < 999):
                    health_data = health_data_options[0]
                else:
                    health_data = health_data_options[1]

                volume += random.randint(0, 10)
                process_data = "PROCESS - Volume: " + str(volume) + " gallons"

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
    plc3 = SwatPLC3(
        name='plc3',
        state=STATE,
        protocol=PLC3_PROTOCOL,
        memory=PLC3_DATA,
        disk=PLC3_DATA)
