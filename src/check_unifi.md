# Check Unifi WIFI state.

Unifi Controller has it's own up check, but I wanted to include it in my Icinga2 installation. So I can see all outages from one place. 

This is a quick script, which should partly be rewritten very soon. Especially the Unifi API should be encapsulated into it's own class. If you have time to help, feel free to fork me. Anyway: It works for me with my controller version, please file a bug if it doesn't for you. 

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

* [Get latest version from here](https://raw.githubusercontent.com/LaggAt/LaggAt-Nagioschecks/master/src/check_unifi.py)

## Links:

* [Site on NagiosExchange](https://exchange.nagios.org/directory/Addons/Active-Checks/check_unifi/details)

