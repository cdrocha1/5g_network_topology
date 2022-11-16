

from minicps.devices import PLC
from utils import RTU1_DATA, STATE, RTU1_PROTOCOL
from utils import RTU_SAMPLES, RTU_PERIOD_SEC
from utils import IP

import time


RTU1_ADDR = IP['rtu1']
RTU2_ADDR = IP['rtu2']
RTU3_ADDR = IP['rtu3']
RTU4_ADDR = IP['rtu4']
SCADA_ADDR = IP['scada']
CTRL_ADDR = IP['controller']
HISTORIAN_ADDR = IP['historian']

class controller(PLC):

    def pre_loop(self, sleep=0.5):
        """scada pre loop.

            - sleep
        """

        time.sleep(sleep)


    def main_loop(self):
        """rtu2 main loop.

            - read UF tank level from the sensor
            - update internal enip server
        """

        print 'DEBUG: swat-s1 rtu2 enters main_loop.'
        print

        count = 0
        while(count <= RTU_SAMPLES):

            lit301 = float(self.get(LIT301_3))
            print "DEBUG RTU - get lit301: %f" % lit301

            self.send(LIT301_3, lit301, RTU2_ADDR)

            time.sleep(RTU_PERIOD_SEC)
            count += 1

        print 'DEBUG swat rtu2 shutdown'


if __name__ == "__main__":

    scada = controller(
        name='controller',
        state=STATE,
        protocol=RTU1_PROTOCOL,
        memory=RTU1_DATA,
        disk=RTU1_DATA)