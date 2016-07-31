#!/usr/bin/env python
# -*- coding: utf-8 -*-
#(c) Florian Lagg (info@lagg.at) 2012
#Created on 30.07.2016

#Licensed under the terms of the General Public License 2.0
#see http://www.gnu.org/licenses/gpl-2.0-standalone.html

#uses nagiosplugin under Zope Public License (ZPL)
#see http://packages.python.org/nagiosplugin/
#uses calmh/unifi-api under MIT License
#see https://github.com/calmh/unifi-api
#uses argp (not included in python 2.7, but in 3.x)

import argparse
import nagiosplugin
#from unifi.controller import Controller --> did not work, so copy just what we need
try:
    # Ugly hack to force SSLv3 and avoid
    # urllib2.URLError: <urlopen error [Errno 1] _ssl.c:504:
    # error:14077438:SSL routines:SSL23_GET_SERVER_HELLO:tlsv1 alert internal error>
    import _ssl
    _ssl.PROTOCOL_SSLv23 = _ssl.PROTOCOL_TLSv1
except:
    pass

try:
    # Updated for python certificate validation
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
except:
    pass

import sys
PYTHON_VERSION = sys.version_info[0]

if PYTHON_VERSION == 2:
    import cookielib
    import urllib2
elif PYTHON_VERSION == 3:
    import http.cookiejar as cookielib
    import urllib3
    import ast

import urllib

import json


""" Check unifi ap online state
    EXAMPLE USE:
	python check_unifi.py -w 1 -c 1 -h my-unifi-controller.com -u USER -p PASSWORD -s MYSITENAME
"""
class Ap_down(nagiosplugin.Resource):
    def __init__(self, host, user, passwd, site):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.site = site

        super(nagiosplugin.Resource, self).__init__()

    def probe(self):
        self.aps = self.getData()
        self.failing_aps = []
        for ap in self.aps:
            if(ap[u'state'] != 1 # do we need the rest?
               or not ap[u'uplink'][u'up']
               or ap[u'isolated']
               ):
                self.failing_aps.append(ap)
        return nagiosplugin.Metric('ap_down', len(self.failing_aps), )

    def getData(self):
        # todo: rewrite a api class when we have time
        baseurl = "https://%s:8443/api" % (self.host,)
        loginurl = "%s/login" % (baseurl,)
        params = {'username': self.user, 'password': self.passwd}
        params = json.dumps(params)

        cj = cookielib.CookieJar()
        if PYTHON_VERSION == 2:
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        elif PYTHON_VERSION == 3:
            self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

        ret = self.opener.open(loginurl, params).read()

        deviceurl = "%s/s/%s/stat/device" % (baseurl, self.site)
        ret = self.opener.open(deviceurl).read()
        return self.__jsondec(ret)

    def __jsondec(self, data):
        if PYTHON_VERSION == 3:
            data = data.decode()
        obj = json.loads(data)
        if 'meta' in obj:
            if obj['meta']['rc'] != 'ok':
                raise Exception(obj['meta']['msg'])
        if 'data' in obj:
            return obj['data']
        return obj

class Ap_down_Context(nagiosplugin.Context):
    def __init__(self, name, warning, critical, fmt_metric=None, result_cls=nagiosplugin.Result):
        self.warning = int(warning)
        self.critical = int(critical)
        super(Ap_down_Context, self).__init__(name, fmt_metric, result_cls)

    def evaluate(self, metric, resource):
        if metric.value >= self.critical:
            return nagiosplugin.state.Critical
        elif metric.value >= self.warning:
            return nagiosplugin.state.Warn
        return nagiosplugin.state.Ok

class Ap_down_Summary(nagiosplugin.Summary):
    def problem(self, results):
        return "failing AP's: %s'" % (', '.join(
            ["%s (%s)" % (ap[u'name'],ap[u'mac'],) for ap in results.results[0].resource.failing_aps]
            )
        )

@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument(
        '-w', '--warning', default='1', metavar='RANGE',
        help='warning threshold (default: %default%)')
    argp.add_argument(
        '-c', '--critical', default='1', metavar='RANGE',
        help='critical threshold (default: %default%)')
    argp.add_argument(
        '-i', '--host', default='127.0.0.1', metavar='STRING',
        help='controller host/ip')
    argp.add_argument(
        '-u', '--user', default='', metavar='STRING',
        help='user')
    argp.add_argument(
        '-p', '--passwd', default='', metavar='STRING',
        help='password')
    argp.add_argument(
        '-s', '--site', default='', metavar='STRING',
        help='Site to monitor')
    # later ...
    argp.add_argument(
        '-t', '--checktype', default='ap_down', metavar='STRING',
        help='What to check (ap_down = Number of offline APs, no other types for now)')
    args = argp.parse_args()

    if (args.checktype == 'ap_down'):
        check = nagiosplugin.Check(
            Ap_down(args.host, args.user, args.passwd, args.site),
            Ap_down_Context('ap_down', args.warning, args.critical, fmt_metric='{valueunit} AP down'),
            Ap_down_Summary()
        )
        check.main()
    else:
        raise Exception("no check named %s" % (args.checktype,))

if __name__ == '__main__':
    main()
