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
        scada, rtu1, rtu2, rtu3, rtu4, s1 = self.net.get(
            'scada', 'rtu1', 'rtu2', 'rtu3', 'rtu4', 's1')

        # SPHINX_SWAT_TUTORIAL RUN(
        
        rtu1.cmd(sys.executable + ' rtu1.py &')
        rtu2.cmd(sys.executable + ' rtu2.py &')
        rtu3.cmd(sys.executable + ' rtu3.py &')
        rtu4.cmd(sys.executable + ' rtu4.py &')
        scada.cmd(sys.executable + ' scada.py &')
        #controller.cmd(sys.executable + ' controller.py &')
        s1.cmd(sys.executable + ' physical_process.py &')
        # SPHINX_SWAT_TUTORIAL RUN)

        CLI(self.net)

        net.stop()

if __name__ == "__main__":

    topo = SwatTopo()
    net = Mininet(topo=topo)

    swat_s1_cps = SwatS1CPS(
        name='swat_s1',
        net=net)
