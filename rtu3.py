
"""
swat-s1 rtu2
"""

from minicps.devices import RTU, PLC
from utils import RTU3_DATA, STATE, RTU3_PROTOCOL
from utils import RTU_SAMPLES, RTU_PERIOD_SEC
from utils import IP

import time

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

        print ('DEBUG: swat-s1 rtu2 enters main_loop.')
        print

        count = 0
        lit301 = 0.456
        while(count <= RTU_SAMPLES):
        	if lit301 <=20:
        		print ("Tank filling - get lit301: %f" % lit301)
        	else:
        		print ("lit301 filling - get lit301: %f" % lit301)
        	
        	lit301 += 2.554
        	time.sleep (RTU_PERIOD_SEC)
        	count += 1
        	
        print ('DEBUG swat rtu2 shutdown')
        print ("lit301 filling - get lit301: %f" % lit301)
        

if __name__ == "__main__":

    # notice that memory init is different form disk init
    rtu3 = SwatRTU3(
        name='rtu3',
        state=STATE,
        protocol=RTU3_PROTOCOL,
        memory=RTU3_DATA,
        disk=RTU3_DATA)
