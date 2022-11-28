
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
import sys


RTU1_ADDR = IP['rtu1']
RTU2_ADDR = IP['rtu2']
RTU3_ADDR = IP['rtu3']
#RTU4_ADDR = IP['rtu4']
SCADA_ADDR = IP['scada']
#CTRL_ADDR = IP['controller']


LIT301_3 = ('LIT301', 3)


class SwatRTU1(RTU):

    # def pre_loop(self, sleep=0.1):
    #    print ('DEBUG: project topo rtu1 enters pre_loop')
    #    print

    #    time.sleep(sleep)

    def main_loop(self):
        """rtu1 main loop.

            - read UF tank level from the sensor
            - update internal enip server
        """

    # ip = IP of SCADA, ip2 = IP of edge server, port = health data, port2 = process data - ip2=10.0.2.22, port=103 | ip=127.0.0.1, port2=503
    def listen(ip, ip2, port, port2):
        sockhealth = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sockprocess = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_plc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        plc_port = 501
        temp = 45
        try:
            print("UDP sending health data on Port:", port)
            print("UDP sending process data on Port: ", port2)
            # sockhealth.settimeout(5)
            # sockprocess.settimeout(5)
            # sock_plc.settimeout(5)
            while True:
                try:
                    # sockhealth.bind(('',port))
                    sock_plc.bind(('', plc_port))

                    #print ("Listening on port", port)
                    print("Listening on port", plc_port)

                except Exception:
                    print("ERROR: Cannot connect to Port:", port2)
                    port2 += 1

                while True:
                    data, addr = sock_plc.recvfrom(1024)
                    print("PLC1 data recived:", data.decode())
                    if "HEALTH" in data.decode():
                        print("health")
                        health_data = data.decode()
                        sockhealth.sendto(health_data.encode(), (ip2, port))
                        data2, addr2 = sockhealth.recvfrom(1024)
                        print(health_data, data2.decode())
                    if "PROCESS" in data.decode():
                        print("process")
                        process_data = data.decode()
                        sockprocess.sendto(process_data.encode(), (ip, port2))
                        data3, addr3 = sockprocess.recvfrom(1024)
                        print(process_data, data3.decode())

                    # print("Health data for server: ")
                    # msg = input('')
                    #sockhealth.sendto(health_data.encode(), (ip, port))
                    #sockhealth.sendto(health_data.encode(), (ip2, port))

                    # print('Process data for server: ')
                    # msg2 = input('')
                    #sockprocess.sendto(process_data.encode(), (ip, port2))

                    # get response on being recieved
                    #data2, addr2 = sockhealth.recvfrom(1024)
                    #print(health_data, data2.decode())
                    #print(msg, data.decode())

                    #data3, addr3 = sockprocess.recvfrom(1024)
                    #print(process_data, data3.decode())
                    #print(msg2, data2.decode())

                    time.sleep(2)

        except socket.timeout:
            print("ERROR: acknowledgement was not received")
        except Exception as ex:
            print("ERROR:", ex)
            # finally:
            # sock.close()
    listen(ip=sys.argv[1], ip2=sys.argv[2], port=int(
        sys.argv[3]), port2=int(sys.argv[4]))


if __name__ == "__main__":

    # notice that memory init is different form disk init
    rtu1 = SwatRTU1(
        name='rtu1',
        state=STATE,
        protocol=RTU1_PROTOCOL,
        memory=RTU1_DATA,
        disk=RTU1_DATA)
