"""
swat-s1 utils.py

sqlite and enip use name (string) and pid (int) has key and the state stores
values as strings.

Actuator tags are redundant, we will use only the XXX_XXX_OPEN tag ignoring
the XXX_XXX_CLOSE with the following convention:
    - 0 = error
    - 1 = off
    - 2 = on

sqlite uses float keyword and cpppo use REAL keyword.
"""

from minicps.utils import build_debug_logger

swat = build_debug_logger(
    name=__name__,
    bytes_per_file=10000,
    rotating_files=2,
    lformat='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    ldir='logs/',
    suffix='')

# physical process {{{1
# SPHINX_SWAT_TUTORIAL PROCESS UTILS(
GRAVITATION = 9.81             # m.s^-2
TANK_DIAMETER = 1.38           # m
TANK_SECTION = 1.5             # m^2
PUMP_FLOWRATE_IN = 2.55        # m^3/h spec say btw 2.2 and 2.4
PUMP_FLOWRATE_OUT = 2.45       # m^3/h spec say btw 2.2 and 2.4

# periods in msec
# R/W = Read or Write
T_PLC_R = 100E-3
T_PLC_W = 100E-3

T_PP_R = 200E-3
T_PP_W = 200E-3
T_HMI_R = 100E-3

# ImageTk
DISPLAYED_SAMPLES = 14

# Control logic thresholds
LIT_101_MM = {  # raw water tank mm
    'LL': 250.0,
    'L': 500.0,
    'H': 800.0,
    'HH': 1200.0,
}
LIT_101_M = {  # raw water tank m
    'LL': 0.250,
    'L': 0.500,
    'H': 0.800,
    'HH': 1.200,
}

LIT_301_MM = {  # ultrafiltration tank mm
    'LL': 250.0,
    'L': 800.0,
    'H': 1000.0,
    'HH': 1200.0,
}
LIT_301_M = {  # ultrafiltration tank m
    'LL': 0.250,
    'L': 0.800,
    'H': 1.000,
    'HH': 1.200,
}

TANK_HEIGHT = 1.600  # m

PLC_PERIOD_SEC = 0.40  # plc update rate in seconds
PLC_PERIOD_HOURS = PLC_PERIOD_SEC / 3600.0
PLC_SAMPLES = 1000

RTU_PERIOD_SEC = 0.50
RTU_SAMPLES = 1000

PP_RESCALING_HOURS = 100
PP_PERIOD_SEC = 0.20  # physical process update rate in seconds
PP_PERIOD_HOURS = (PP_PERIOD_SEC / 3600.0) * PP_RESCALING_HOURS
PP_SAMPLES = int(PLC_PERIOD_SEC / PP_PERIOD_SEC) * PLC_SAMPLES

RWT_INIT_LEVEL = 0.500  # l

# m^3 / h
FIT_201_THRESH = 1.00
# SPHINX_SWAT_TUTORIAL PROCESS UTILS)

# topo {{{1
IP = {
    'controller': '192.168.1.10',
    'rtu1': '192.168.1.20',
    'rtu2': '192.168.1.30',
    'rtu3': '192.168.1.40',
    'rtu4': '192.168.1.50',
    'scada': '192.168.1.60',
    'attacker': '192.168.1.70',
    'historian': '192.168.1.80'
}

NETMASK = '/24'

MAC = {
    'controller': '00:1D:9C:C8:BC:2E',
    'rtu1': '00:1D:9C:C8:BC:2A',
    'rtu2': '00:1D:9C:C8:BC:2B',
    'rtu3': '00:1D:9C:C8:BC:2C',
    'rtu4': '00:1D:9C:C8:BC:2D',
    'scada': '64:00:6A:70:86:D0',
    'historian': '64:00:6A:70:86:D3'

}



# TODO
RTU1_DATA = {
    'TODO': 'TODO',
}
# TODO
RTU2_DATA = {
    'TODO': 'TODO',
}
# TODO
RTU3_DATA = {
    'TODO': 'TODO',
}
# TODO
RTU4_DATA = {
    'TODO': 'TODO',
}
# TODO
CONTROLLER_DATA = {
    'TODO': 'TODO',
}

HISTORIAN_DATA = {
     'TODO':'TODO',
}

# SPHINX_SWAT_TUTORIAL PLC1 UTILS(
# PLC1_ADDR = IP['plc1']
# PLC1_TAGS = (
#     ('FIT101', 1, 'REAL'),
#     ('MV101', 1, 'INT'),
#     ('LIT101', 1, 'REAL'),
#     ('P101', 1, 'INT'),
#     # interlocks does NOT go to the statedb
#     ('FIT201', 1, 'REAL'),
#     ('MV201', 1, 'INT'),
#     ('LIT301', 1, 'REAL'),
# )
# PLC1_SERVER = {
#     'address': PLC1_ADDR,
#     'tags': PLC1_TAGS
# }
# PLC1_PROTOCOL = {
#     'name': 'enip',
#     'mode': 1,
#     'server': PLC1_SERVER
# }
# # SPHINX_SWAT_TUTORIAL PLC1 UTILS)



RTU1_ADDR = IP['rtu1']
RTU1_TAGS = (
    ('LIT301', 3, 'REAL'),
    # no interlocks
)
RTU1_SERVER = {
    'address': RTU1_ADDR,
    'tags': RTU1_TAGS
}
RTU1_PROTOCOL = {
    'name': 'enip',
    'mode': 1,
    'server': RTU1_SERVER
}

SCADA_ADDR = IP['scada']
SCADA_TAGS = (10, 10, 10, 10)

SCADA_SERVER = {
    'address': SCADA_ADDR,
    'tags': SCADA_TAGS
}
SCADA_PROTOCOL = {
    'name': 'modbus',
    'mode': 1,
    'server': SCADA_SERVER
}
SCADA_PERIOD_SEC = 2.0

# state {{{1
# SPHINX_SWAT_TUTORIAL STATE(
PATH = 'project_topo_db.sqlite'
NAME = 'project_topo'

STATE = {
    'name': NAME,
    'path': PATH
}
# SPHINX_SWAT_TUTORIAL STATE)

SCHEMA = """
CREATE TABLE swat_s1 (
    name              TEXT NOT NULL,
    pid               INTEGER NOT NULL,
    value             TEXT,
    PRIMARY KEY (name, pid)
);
"""

SCHEMA_INIT = """
    INSERT INTO swat_s1 VALUES ('FIT101',   1, '2.55');
    INSERT INTO swat_s1 VALUES ('MV101',    1, '0');
    INSERT INTO swat_s1 VALUES ('LIT101',   1, '0.500');
    INSERT INTO swat_s1 VALUES ('P101',     1, '1');

    INSERT INTO swat_s1 VALUES ('FIT201',   2, '2.45');
    INSERT INTO swat_s1 VALUES ('MV201',    2, '0');

    INSERT INTO swat_s1 VALUES ('LIT301',   3, '0.500');
"""

# tags {{{1
CO_0_2a = ('CO', 0, '2a')
CO_1_2a = ('CO', 1, '2a')
CO_2_2a = ('CO', 2, '2a')
CO_3_2a = ('CO', 3, '2a')
HR_0_2a = ('HR', 0, '2a')
HR_1_2a = ('HR', 1, '2a')
HR_2_2a = ('HR', 2, '2a')

# IR_0_2a = ('IR', 0, '2a')
# IR_1_2a = ('IR', 1, '2a')
# DI_0_2a = ('DI', 0, '2a')
# DI_1_2a = ('DI', 1, '2a')

CO_0_2b = ('CO', 0, '2b')
CO_1_2b = ('CO', 1, '2b')
CO_2_2b = ('CO', 2, '2b')
CO_3_2b = ('CO', 3, '2b')
HR_0_2b = ('HR', 0, '2b')
HR_1_2b = ('HR', 1, '2b')
HR_2_2b = ('HR', 2, '2b')