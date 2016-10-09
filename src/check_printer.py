#!/usr/bin/env python
# -*- coding: utf-8 -*-
#(c) Florian Lagg (github@florian.lagg.at) 2012-2016
#Created on 20.05.2012

#Licensed under the terms of the General Public License 2.0
#see http://www.gnu.org/licenses/gpl-2.0-standalone.html

#uses nagiosplugin under Zope Public License (ZPL)
#see http://packages.python.org/nagiosplugin/
#uses pysnmp, see pip install pysnmp

import argparse
import nagiosplugin
from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
from datetime import timedelta

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
pagecounter = "1.3.6.1.2.1.43.10.2.1.4"
printername = "1.3.6.1.2.1.25.3.2.1.3.1"
uptime = "1.3.6.1.2.1.1.3.0"

class SnmpResource(nagiosplugin.Resource):
    def __init__(self, host, passwd):
        self.host = host
        self.passwd = passwd
        super(nagiosplugin.Resource, self).__init__()

    def myNextCmd(self, *ids):
        for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(SnmpEngine(),
                    CommunityData(self.passwd, mpModel=0),
                    UdpTransportTarget((self.host, 161)),
                    ContextData(),
                    *ids,
                    lexicographicMode=False):
            if errorIndication:
                raise Exception(errorIndication)
            else:
                if errorStatus:
                    raise Exception('%s at %s' % (
                        errorStatus.prettyPrint(),
                            errorIndex and varBinds[-1][int(errorIndex) - 1] or '?'
                        ))
                else:
                    yield varBinds

    def myGetCmd(self, *ids):
        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            CommunityData(self.passwd, mpModel=0),
            UdpTransportTarget((self.host, 161)),
            *ids
        )
        if errorIndication:
            raise Exception(errorIndication)
        else:
            if errorStatus:
                raise Exception('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[-1][int(errorIndex) - 1] or '?'
                ))
            else:
                return varBinds

    def probe(self):
        metrics = []
        # supplies
        for varBinds in self.myNextCmd(
                ObjectType(ObjectIdentity(supplies_table + '.5')),  # type
                ObjectType(ObjectIdentity(supplies_table + '.6')),  # description
                ObjectType(ObjectIdentity(supplies_table + '.7')),  # unit
                ObjectType(ObjectIdentity(supplies_table + '.8')),  # capacity
                ObjectType(ObjectIdentity(supplies_table + '.9')),  # level
        ):
            metrics.append(nagiosplugin.Metric(
                name = 'supplies_[%s]%s' % (supplies_types[ varBinds[0][1] ], varBinds[1][1]),
                context = 'supplies',
                value = varBinds[4][1],
                uom = " "+supplies_units[ varBinds[2][1] ],
                min = 0, max = varBinds[3][1],
            ))
        # informantional data:
        # pagecounter
        self.Pagecounter = []
        for varBinds in self.myNextCmd(
                ObjectType(ObjectIdentity(pagecounter)),  # page counters
        ):
            self.Pagecounter.append(varBinds[0][1])
        # printer name and uptime
        varBinds = self.myGetCmd(
            cmdgen.MibVariable(printername),    # printer name
            cmdgen.MibVariable(uptime)          # uptime
        )
        self.PrinterName = varBinds[0][1]
        self.Uptime = varBinds[1][1]

        return metrics

class Context_num(nagiosplugin.Context):
    def __init__(self, name, warning, critical, special_levels=[], lower_is_better = True, fmt_metric=None, result_cls=nagiosplugin.Result):
        self.warning = float(warning)
        self.critical = float(critical)
        self.special_levels = special_levels
        self.lower_is_better = lower_is_better
        super(Context_num, self).__init__(name, fmt_metric, result_cls)

    def evaluate(self, metric, resource):
        warning = self.warning
        critical = self.critical
        for search,warn,crit in self.special_levels:
            if search in metric.name:
                warning = float(warn)
                warning = float(crit)
                break
        percent = float(metric.value) / float(metric.max) * float(100)
        if(self.lower_is_better):
            if percent >= critical:
                return nagiosplugin.state.Critical
            elif percent >= warning:
                return nagiosplugin.state.Warn
        else:
            if percent <= warning:
                return nagiosplugin.state.Warn
            elif percent <= critical:
                return nagiosplugin.state.Critical
        return nagiosplugin.state.Ok

class SnmpSummary(nagiosplugin.Summary):
    def commonSummary(self, results):
        res = results[0].metric.resource
        printername = res.PrinterName
        uptime = timedelta(seconds=float(res.Uptime)*0.01)
        pagecounters = ", ".join([str(pc) for pc in res.Pagecounter])
        supplies = ", ".join(["{0} {1} ({2})".format(r.metric.name,r.metric.valueunit,r.state) for r in results])
        return "{0} running since {1}, printed {2} pages, supplies left: {3}".format(
            printername,
            uptime,
            pagecounters,
            supplies,
        )

    def ok(self, results):
        return self.commonSummary(results)

    def problem(self, results):
        return self.commonSummary(results)

@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument(
        '-w', '--warning', default='50', metavar='RANGE',
        help='default warning threshold (default: %default%)')
    argp.add_argument(
        '-c', '--critical', default='25', metavar='RANGE',
        help='default critical threshold (default: %default%)')
    argp.add_argument(
        '--special', nargs=3, action='append',
        help='special warning and critical levels for metrics containing string. use --special <TEXT> <warn> <critical>. Example: --special Drum 10 5'
    )
    argp.add_argument(
        '-i', '--host', default='127.0.0.1', metavar='STRING',
        help='host/ip of printer')
    argp.add_argument(
        '-p', '--passwd', default='public', metavar='STRING',
        help='Community name (SNMP)')
    args = argp.parse_args()

    check = nagiosplugin.Check(
        SnmpResource(args.host, args.passwd),
        Context_num('supplies', args.warning, args.critical, args.special, lower_is_better=False),
        SnmpSummary()
    )
    check.main()


if __name__ == '__main__':
    main()
