# Check Printer supplies.

Monitors your printer supplies fill state. Tested with an OKI printer, but should work with many IP printers supporting SNMP.

## Prequisites

* Python 2.7 (not tested on other versions, please give feedback)
* nagiosplugin (install with 'pip install nagiosplugin')
* pysnmp (install with 'pip install pysnmp')
* Icinga2, Nagios, ... server.

## Usage: check_printer.py [options] 

Example: check_printer.py -i 192.168.0.200 --special [opc] 20 10  --special [fuser] 5 2 --special [transferUnit] 5 2

```
-w RANGE, --warning=RANGE 
warning threshold (default: 20%) 
-c RANGE, --critical=RANGE 
critical threshold (default: 10%) 
--special <searchstring> <warning> <critical>
special thresholds for for supplies of type/name
-i STRING, --host=STRING 
host name or ip of printer
-p STRING, --pass=STRING 
community name (default: public)
```

Tested on Python 2.7 with nagiosplugin 1.2.4

## DOWNLOAD: 

* [Get latest version from here](https://raw.githubusercontent.com/LaggAt/LaggAt-Nagioschecks/master/src/check_printer.py)
