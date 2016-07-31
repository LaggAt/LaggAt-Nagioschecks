#!/usr/bin/env python
# -*- coding: utf-8 -*-
#(c) Florian Lagg (github@florian.lagg.at) 2012-2016
#Created on 20.05.2012

#Licensed under the terms of the General Public License 2.0
#see http://www.gnu.org/licenses/gpl-2.0-standalone.html

#uses nagiosplugin under Zope Public License (ZPL)
#see http://packages.python.org/nagiosplugin/

import argparse
import nagiosplugin
import urllib, urllib2

""" Check the Clickatell balance
    EXAMPLE USE:
    python check_clickatell_balance.py -w 50 -c 20 -a APP_ID -u USER -p PASSWORD
"""
class Clickatell_balance(nagiosplugin.Resource):
    def __init__(self, api, user, passwd):
        self.api_id = api
        self.user = user
        self.passwd = passwd
        
        super(nagiosplugin.Resource, self).__init__()

    def probe(self):
        self.credits = None
        #prepare http request
        url = 'http://api.clickatell.com/http/getbalance'
        values = {
              'api_id'   : self.api_id,
              'user'     : self.user,
              'password' : self.passwd }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        #query
        try:
            resp_obj = urllib2.urlopen(req)
            response = resp_obj.read()
        except Exception, e:
            return nagiosplugin.Metric('balance', self.credits, )
        #read
        preOK='Credit: '
        if response.startswith(preOK):
            self.credits = float( response.lstrip(preOK) )
        return nagiosplugin.Metric('balance', self.credits, )

class Context_num(nagiosplugin.Context):
    def __init__(self, name, warning, critical, lower_is_better = True, fmt_metric=None, result_cls=nagiosplugin.Result):
        self.warning = float(warning)
        self.critical = float(critical)
        self.lower_is_better = lower_is_better
        super(Context_num, self).__init__(name, fmt_metric, result_cls)

    def evaluate(self, metric, resource):
        if(self.lower_is_better):
            if metric.value >= self.critical:
                return nagiosplugin.state.Critical
            elif metric.value >= self.warning:
                return nagiosplugin.state.Warn
        else:
            if metric.value <= self.warning:
                return nagiosplugin.state.Warn
            elif metric.value <= self.critical:
                return nagiosplugin.state.Critical
        return nagiosplugin.state.Ok

class Clickatell_balance_Summary(nagiosplugin.Summary):
    def problem(self, results):
        balance = results.results[0].resource.credits
        return "balance is low: %s" % (balance,)

@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument(
        '-w', '--warning', default='50', metavar='RANGE',
        help='warning threshold (default: %default%)')
    argp.add_argument(
        '-c', '--critical', default='25', metavar='RANGE',
        help='critical threshold (default: %default%)')
    argp.add_argument(
        '-a', '--api', default='', metavar='STRING',
        help='clickatell api-id')
    argp.add_argument(
        '-u', '--user', default='', metavar='STRING',
        help='clickatell user')
    argp.add_argument(
        '-p', '--passwd', default='', metavar='STRING',
        help='clickatell password')
    args = argp.parse_args()
    
    check = nagiosplugin.Check(
        Clickatell_balance(args.api, args.user, args.passwd),
        Context_num('balance', args.warning, args.critical, lower_is_better = False, fmt_metric='Balance: {valueunit}'),
        Clickatell_balance_Summary()
    )
    check.main()

if __name__ == '__main__':
    main()
