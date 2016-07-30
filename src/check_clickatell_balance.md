# Check the balance on Clickatell.com SMS gateway using HTTP-API

## Prequisites

* Python 2.7 (not tested on other versions, please give feedback)
* nagiosplugin (install with 'easy_install nagiosplugin')
* Icinga2, Nagios, ... server.

## Usage: check_clickatell_balance.py [options] 

```
-w RANGE, --warning=RANGE 
warning threshold (default: 50%) 
-c RANGE, --critical=RANGE 
critical threshold (default: 25%) 
-a STRING, --api=STRING 
api-id for clickatell 
-u STRING, --user=STRING 
user for clickatell 
-p STRING, --passwd=STRING 
password for clickatell 
```

Tested on Python 2.7 with nagiosplugin 0.4.4

## DOWNLOAD: 

* [Get latest version from here](https://raw.githubusercontent.com/LaggAt/LaggAt-Nagioschecks/master/src/check_clickatell_balance.py)

## Links:

* [Site on NagiosExchange](https://exchange.nagios.org/directory/Addons/Active-Checks/check_clickatell_balance)

