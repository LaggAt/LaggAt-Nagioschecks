#!/usr/bin/python3
# -*- coding: utf-8 -*-
#(c) Florian Lagg (info@lagg.at) 2016

#Python3 setup Ubuntu
# apt-get install python3-setuptools
# easy_install3 pip
# cd /usr/local/bin
# cp pip2 pip
# pip3 install urbackup-server-web-api-wrapper
# pip3 install nagiosplugin

import argparse
import nagiosplugin
import urbackup_api

class Failing_Backup(nagiosplugin.Resource):
    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd

        super(nagiosplugin.Resource, self).__init__()

    def probe(self):
        self.status = self.getStatus()
        self.failing_backups = []
        for client in self.status:
            if not "rejected" in client or ("rejected" in client and not client["rejected"]):
                name = client["name"]
                if not client["image_ok"]:
                    self.failing_backups.append({'client': name, 'fail': 'image'})
                if not client["file_ok"]:
                    self.failing_backups.append({'client': name, 'fail': 'file'})
        return nagiosplugin.Metric('failing_backups', len(self.failing_backups), )
    
    def getStatus(self):
        server = urbackup_api.urbackup_server("http://{server}:55414/x".format(
                server = self.host,
            ), 
            self.user, 
            self.passwd
        )
        return server.get_status()

class Failing_Backup_Context(nagiosplugin.Context):
    def __init__(self, name, warning, critical, fmt_metric=None, result_cls=nagiosplugin.Result):
        self.warning = int(warning)
        self.critical = int(critical)
        super(Failing_Backup_Context, self).__init__(name, fmt_metric, result_cls)

    def evaluate(self, metric, resource):
        if metric.value >= self.critical:
            return nagiosplugin.state.Critical
        elif metric.value >= self.warning:
            return nagiosplugin.state.Warn
        return nagiosplugin.state.Ok

class Failing_Backup_Summary(nagiosplugin.Summary):
    def problem(self, results):
        return "failing backups: %s'" % (', '.join(
            ["%s.%s failed" % (b[u'client'],b[u'fail'],) for b in results.results[0].resource.failing_backups]
            )
        )

@nagiosplugin.guarded
def main():
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument(
        '-w', '--warning', default='1', metavar='RANGE',
        help='warning threshold')
    argp.add_argument(
        '-c', '--critical', default='1', metavar='RANGE',
        help='critical threshold')
    argp.add_argument(
        '-i', '--host', default='127.0.0.1', metavar='STRING',
        help='host/ip')
    argp.add_argument(
        '-u', '--user', default='', metavar='STRING',
        help='user')
    argp.add_argument(
        '-p', '--passwd', default='', metavar='STRING',
        help='password')
    args = argp.parse_args()
    
    check = nagiosplugin.Check(
        Failing_Backup(args.host, args.user, args.passwd),
        Failing_Backup_Context('failing_backups', args.warning, args.critical, fmt_metric='{valueunit} backups failing'),
        Failing_Backup_Summary()
    )
    check.main()
    
if __name__ == '__main__':
    main()

