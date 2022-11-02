"""
swat-s1 topology
"""

from mininet.topo import Topo

from utils import IP, MAC, NETMASK


class SwatTopo(Topo):

    """SWaT 3 plcs + attacker + private dirs."""

    def build(self):

        switch = self.addSwitch('s1')

        # plc1 = self.addHost(
        #     'plc1',
        #     ip=IP['plc1'] + NETMASK,
        #     mac=MAC['plc1'])
        # self.addLink(plc1, switch)

        # plc2 = self.addHost(
        #     'plc2',
        #     ip=IP['plc2'] + NETMASK,
        #     mac=MAC['plc2'])
        # self.addLink(plc2, switch)

        # plc3 = self.addHost(
        #     'plc3',
        #     ip=IP['plc3'] + NETMASK,
        #     mac=MAC['plc3'])
        # self.addLink(plc3, switch)
       
        rtu1 = self.addHost(
            'rtu1',
            ip=IP['rtu1'] + NETMASK,
            mac=MAC['rtu1'])
        self.addLink(rtu1, switch)
        
        rtu2 = self.addHost(
            'rtu2',
            ip=IP['rtu2'] + NETMASK,
            mac=MAC['rtu2'])
        self.addLink(rtu2, switch)

        rtu3 = self.addHost(
            'rtu3',
            ip=IP['rtu3'] + NETMASK,
            mac=MAC['rtu3'])
        self.addLink(rtu3, switch)

        rtu4 = self.addHost(
            'rtu4',
            ip=IP['rtu4'] + NETMASK,
            mac=MAC['rtu4'])
        self.addLink(rtu4, switch)

        scada = self.addHost(
            'scada',
            ip=IP['scada'] + NETMASK,
            mac=MAC['scada'])
        self.addLink(scada, switch)

        # controller = self.addHost(
        #     'controller',
        #     ip=IP['controller'] + NETMASK,
        #     mac=MAC['controller'])
        # self.addLink(controller, switch)

        # attacker = self.addHost(
        #     'attacker',
        #     ip=IP['attacker'] + NETMASK,
        #     mac=MAC['attacker'])
        # self.addLink(attacker, switch)
