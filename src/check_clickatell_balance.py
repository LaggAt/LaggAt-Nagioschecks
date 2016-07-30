#!/usr/bin/env python
# -*- coding: utf-8 -*-
#(c) Florian Lagg (info@lagg.at) 2012
#Created on 20.05.2012

#Licensed under the terms of the General Public License 2.0
#see http://www.gnu.org/licenses/gpl-2.0-standalone.html

#uses nagiosplugin under Zope Public License (ZPL)
#see http://packages.python.org/nagiosplugin/

import nagiosplugin
import urllib, urllib2

""" Check the Clickatell balance
    EXAMPLE USE:
    python check_clickatell_balance.py -w 50 -c 20 -a APP_ID -u USER -p PASSWORD
"""
class CBalance(nagiosplugin.Check):
    name = 'clickatell balance checker'
    version = '0.1'

    def __init__(self, optparser, logger):
        optparser.description = 'Check the balance on Clickatell.com SMS gateway using HTTP-API'
        optparser.version = '0.1'
        optparser.add_option(
            '-w', '--warning', default='50', metavar='RANGE',
            help='warning threshold (default: %default%)')
        optparser.add_option(
            '-c', '--critical', default='25', metavar='RANGE',
            help='critical threshold (default: %default%)')
        optparser.add_option(
            '-a', '--api', default='', metavar='STRING',
            help='api-id for clickatell')
        optparser.add_option(
            '-u', '--user', default='', metavar='STRING',
            help='user for clickatell')
        optparser.add_option(
            '-p', '--passwd', default='', metavar='STRING',
            help='password for clickatell')

    def process_args(self, options, args):
        self.warning = "@" + options.warning
        self.critical = "@" + options.critical
        self.api_id = options.api
        self.user = options.user
        self.passwd = options.passwd

    def obtain_data(self):
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
            return "ERR: cannot get balance, %s" % (repr(e),)
        #read
        preOK='Credit: '
        if response.startswith(preOK):
            self.credits = float( response.lstrip(preOK) )
            #performance data
            self.measures = [nagiosplugin.Measure(
               'balance', self.credits, 'credits', self.warning, self.critical)]
        else:
            #something failed
            return "Err: %s" % (response,)


main = nagiosplugin.Controller(CBalance)
if __name__ == '__main__':
    main()