# Check Urbackup state in Nagios/Icinga.

Urbackup is a nice and easy backup solution, supporting image and file backups. Setup is straightforward and easy, and you will forget about it once running. 

Urbackup can monitor his own client backups, and alert by mail if something goes wrong. For such a critical job as backup I wanted more: I want to monitor the backup server itself, and that all backups are up to date and working. So I decided to use my Icinga2 monitoring.

## Prequisites

* Python 3.5 (will NOT work on 2.7 because of a used library)
* nagiosplugin (install with 'pip install nagiosplugin')
* urbackup-server-web-api-wrapper (pip3 install urbackup-server-web-api-wrapper)
* Icinga2, Nagios, ... server.
* Urbackup server. We recommend creating a user/password in the web gui.

## Usage: check3_urbackup.py [options] 

```
-w RANGE, --warning=RANGE 
warning threshold (default: 1) 
-c RANGE, --critical=RANGE 
critical threshold (default: 1) 
-i STRING, --host=STRING 
host name or ip or urbackup server
-u STRING, --user=STRING 
user
-p STRING, --passwd=STRING 
password
```

## Firewall:

The check uses the Port TCP/55414 which is the default in Urbackup.

## DOWNLOAD: 

* [Get latest version from here](https://raw.githubusercontent.com/LaggAt/LaggAt-Nagioschecks/master/src/check3_urbackup.py)

## Links:

* [Urbackup](https://www.urbackup.org/)
* pending [Site on NagiosExchange](https://exchange.nagios.org/directory/Addons/)

