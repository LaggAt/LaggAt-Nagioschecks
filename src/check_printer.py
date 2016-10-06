# pip install pysnmp

import pprint
from pysnmp.hlapi import *

# https://developer.apple.com/library/content/technotes/tn2144/_index.html
supplies_table = "1.3.6.1.2.1.43.11.1.1"
supplies_types = {
    1 : 'other',
    2 : 'unknown',
    3 : 'toner',
    4 : 'wasteToner',
    5 : 'ink',
    6 : 'inkCartridge',
    7 : 'inkRibbon',
    8 : 'wasteInk',
    9 : 'opc',
    10 : 'developer',
    11 : 'fuserOil',
    12 : 'solidWax',
    13 : 'ribbonWax',
    14 : 'wasteWax',
    15 : 'fuser',
    16 : 'coronaWire',
    17 : 'fuserOilWick',
    18 : 'cleanerUnit',
    19 : 'fuserCleaningPad',
    20 : 'transferUnit',
    21 : 'tonerCartridge',
    22 : 'fuserOiler',
    23 : 'water',
    24 : 'wasteWater',
    25 : 'glueWaterAdditive',
    26 : 'wastePaper',
    27 : 'bindingSupply',
    28 : 'bandingSupply',
    29 : 'stitchingWire',
    30 : 'shrinkWrap',
    31 : 'paperWrap',
    32 : 'staples',
    33 : 'inserts',
    34 : 'covers',
}
supplies_units = {
    1: 'other',
    2: 'unknown',
    3: 'tenThousandthsOfInches',
    4: 'micrometers',
    7: 'impressions',
    8: 'sheets',
    11: 'hours',
    12: 'thousandthsOfOunces',
    13: 'tenthsOfGrams',
    14: 'hundrethsOfFluidOunces',
    15: 'tenthsOfMilliliters',
    16: 'feet',
    17: 'meters',
    18: 'items',
    19: 'percent',
}

supplies_usage = []
for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(SnmpEngine(),
        CommunityData('public', mpModel=0),
        UdpTransportTarget(('192.168.144.200', 161)),
        ContextData(),
        ObjectType(ObjectIdentity(supplies_table + '.5')), # type
        ObjectType(ObjectIdentity(supplies_table + '.6')), # description
        ObjectType(ObjectIdentity(supplies_table + '.7')), # unit
        ObjectType(ObjectIdentity(supplies_table + '.8')), # capacity
        ObjectType(ObjectIdentity(supplies_table + '.9')), # level
        lexicographicMode=False):
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[-1][int(errorIndex) - 1] or '?'
            ))
        else:
            it = {
                'type': supplies_types[ varBinds[0][1] ],
                'description': varBinds[1][1],
                'unit': supplies_units[ varBinds[2][1] ],
                'capacity': varBinds[3][1],
                'level': varBinds[4][1]
                }
            it['percent_available'] = float(it['level']) / float(it['capacity']) * float(100)
            supplies_usage.append( it )

pprint.pprint(supplies_usage)
pass