# pip install pysnmp

import pprint
from pysnmp.hlapi import *

supplies_table = "1.3.6.1.2.1.43.11.1.1"

supplies_usage = []
for (errorIndication,
     errorStatus,
     errorIndex,
     varBinds) in nextCmd(SnmpEngine(),
                          CommunityData('public', mpModel=0),
                          UdpTransportTarget(('192.168.1.200', 161)),
                          ContextData(),
                          ObjectType(ObjectIdentity(supplies_table + '.6')),
                          ObjectType(ObjectIdentity(supplies_table + '.8')),
                          ObjectType(ObjectIdentity(supplies_table + '.9')),
                          lexicographicMode=False):
    if errorIndication:
        print(errorIndication)
        break
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
        break
    else:
        it = {
            'name': varBinds[0][1],
            'max': varBinds[1][1],
            'avail': varBinds[2][1]
            }
        it['percent_used'] = float(it['avail']) / float(it['max']) * float(100)
        supplies_usage.append( it )

pprint.pprint(supplies_usage)
pass