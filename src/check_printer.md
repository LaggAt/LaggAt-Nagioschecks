# Check Printer supplies.

Monitors your printer supplies fill state. Tested with an OKI printer, but should work with many IP printers supporting SNMP.

## Prequisites

* Python 2.7 (not tested on other versions, please give feedback)
* nagiosplugin (install with 'pip install nagiosplugin')
* pysnmp (install with 'pip install pysnmp')
* Icinga2, Nagios, ... server.

## Usage: check_printer.py [options] 

```
For "Percent" measurements (e.g. toner):
--percentWarn=RANGE 
warning threshold (default: 40%) 
--percentCrit=RANGE 
critical threshold (default: 20%) 
For "Impressions" measurements (e.g. transferUnit):
--impressionWarn=RANGE 
warning threshold for "impressions" (default: 500) 
--impressionCrit=RANGE 
critical threshold for "impressions"  (default: 250) 
All other measure-units will be calculated in % and compared to these thresholds:
-w RANGE, --warning=RANGE 
warning threshold (default: 20%) 
-c RANGE, --critical=RANGE 
critical threshold (default: 10%) 
-i STRING, --host=STRING 
host name or ip of printer
-u STRING, --user=STRING 
community name (default: public)
```

Tested on Python 2.7 with nagiosplugin 1.2.4

## DOWNLOAD: 

* [Get latest version from here](https://raw.githubusercontent.com/LaggAt/LaggAt-Nagioschecks/master/src/check_printer.py)
