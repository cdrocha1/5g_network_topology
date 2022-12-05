"""
swat-s1 run.py
"""

from mininet.net import Mininet
from mininet.cli import CLI
from minicps.mcps import MiniCPS

from topo import SwatTopo

import sys


class SwatS1CPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        net.start()

        net.pingAll()

        # start devices
        plc1, plc2, plc3,rtu1, rtu2, rtu3, scada,historian, s1 = self.net.get(
        'plc1', 'plc2', 'plc3','rtu1', 'rtu2', 'rtu3', 'scada','historian','s1')

        # SPHINX_SWAT_TUTORIAL RUN(
        historian.cmd(sys.executable + ' historian.py &')
        scada.cmd(sys.executable + ' scada.py &')
        plc2.cmd(sys.executable + ' plc2.py 127.0.0.1 501 &')
        plc3.cmd(sys.executable + ' plc3.py 127.0.0.1 500 &')
        plc1.cmd(sys.executable + ' plc1.py 127.0.0.1 499 &')
        rtu1.cmd(sys.executable + ' rtu1.py 127.0.0.1 10.0.2.22 103 503 &')
        rtu2.cmd(sys.executable + ' rtu2.py 127.0.0.1 10.0.2.22 103 503 &')
        rtu3.cmd(sys.executable + ' rtu3.py 127.0.0.1 10.0.2.22 103 503 &')
        #controller.cmd(sys.executable + ' controller.py &')
        #s1.cmd(sys.executable + ' physical_process.py &')
        # SPHINX_SWAT_TUTORIAL RUN)

        CLI(self.net)

        net.stop()

if __name__ == "__main__":

    topo = SwatTopo()
    net = Mininet(topo=topo)

    swat_s1_cps = SwatS1CPS(
        name='swat_s1',
        net=net)
