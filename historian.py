l"""
historian.py
"""

from minicps.devices import SCADAServer
from utils import SCADA_PROTOCOL, STATE
from utils import SCADA_PERIOD_SEC
from utils import IP
from utils import CO_0_2a, CO_1_2a, CO_2_2a, CO_3_2a
from utils import HR_0_2a

import time

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']
RTU1_ADDR = IP['rtu1']
RTU2_ADDR = IP['rtu2']
RTU3_ADDR = IP['rtu3']
RTU4_ADDR = IP['rtu4']
SCADA_ADDR = IP['scada']
HISTORIAN_ADDR = IP['historian']

class Historian(SCADAServer):

    def pre_loop(self, sleep=0.5):
        """scada pre loop.

            - sleep
        """

        time.sleep(sleep)


    def main_loop(self):
        """scada main loop.

        For each RTU in the network
            - Read the pump status
        """

        while(True):

            #co_00_2a = self.receive(CO_0_2a, RTU2A_ADDR)
            co_00_2a = self.receive(CO_0_2a, HISTORIAN_ADDR)

            # NOTE: used for testing first challenge
            #print('DEBUG scada from rtu2a: CO 0-0 2a: {}'.format(co_00_2a))

            # NOTE: used for testing second challenge
            # NOTE: comment out
            # hr_03_2a = self.receive(HR_0_2a, RTU2B_ADDR, count=3)
            # print('DEBUG scada from rtu2b: HR 0-2 2a: {}'.format(hr_03_2a))


            # print("DEBUG: scada main loop")
            time.sleep(SCADA_PERIOD_SEC)


if __name__ == "__main__":

    SCADAServer = historian(
        name='historian',
        state=STATE,
        protocol=SCADA_PROTOCOL)