# Check the balance on Clickatell.com SMS gateway using HTTP-API

## Prequisites

* Python 2.7 (not tested on other versions, please give feedback)
* nagiosplugin (install with 'pip install nagiosplugin')
* Icinga2, Nagios, ... server.

## Usage: check_unifi.py [options] 

```
-w RANGE, --warning=RANGE 
warning threshold (default: 1) 
-c RANGE, --critical=RANGE 
critical threshold (default: 1) 
-i STRING, --host=STRING 
host name or ip of unifi controller
-u STRING, --user=STRING 
user
-p STRING, --passwd=STRING 
password
-s Default, --site=Default
Site to monitor (this is not the site name, take the site-id from the unifi controller url)
```

Tested on Python 2.7 with nagiosplugin 1.2.4

## DOWNLOAD: 

* [Get latest version from here](TODO)

## Links:

* [Site on NagiosExchange](TODO)

