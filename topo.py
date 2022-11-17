
from mininet.topo import Topo
from utils import IP, MAC, NETMASK
from mininet.node import Controller
from mininet.net import Mininet


class SwatTopo(Topo):

    def build(self):

        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        #s2 = self.addSwitch('s2', protocols='OpenFlow13')
        #s3 = self.addSwitch('s3', protocols='OpenFlow13')
        
        plc1 = self.addHost(
            'plc1',
            ip=IP['plc1'] + NETMASK,
            mac=MAC['plc1'])
        self.addLink(plc1, s1)

        plc2 = self.addHost(
            'plc2',
            ip=IP['plc2'] + NETMASK,
            mac=MAC['plc2'])
        self.addLink(plc2, s1)

        plc3 = self.addHost(
            'plc3',
            ip=IP['plc3'] + NETMASK,
            mac=MAC['plc3'])
        self.addLink(plc3, s1)

        rtu1 = self.addHost(
            'rtu1',
            ip=IP['rtu1'] + NETMASK,
            mac=MAC['rtu1'])
        self.addLink(s1, rtu1)
        #self.addLink(s2, rtu1)

        rtu2 = self.addHost(
            'rtu2',
            ip=IP['rtu2'] + NETMASK,
            mac=MAC['rtu2'])
        self.addLink(s1, rtu2)
        #self.addLink(s2, rtu2)

        rtu3 = self.addHost(
            'rtu3',
            ip=IP['rtu3'] + NETMASK,
            mac=MAC['rtu3'])
        self.addLink(rtu3,s1)
        #self.addLink(rtu3,s2)

        """
        rtu4 = self.addHost(
            'rtu4',
            ip=IP['rtu4'] + NETMASK,
            mac=MAC['rtu4'])
        #self.addLink(rtu4, switch)
        """

        scada = self.addHost(
            'scada',
            ip=IP['scada'] + NETMASK,
            mac=MAC['scada'])

        self.addLink(s1, scada)
        
        historian = self.addHost(
        	'historian',
        	ip=IP['historian'] + NETMASK,
        	mac=MAC['historian'])
        self.addLink(historian,s1)
        #self.addLink(s1,s2)
        #self.addLink(s2, scada)
        #self.addLink(s3, scada)

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
