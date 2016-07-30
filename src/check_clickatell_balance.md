Check the balance on Clickatell.com SMS gateway using HTTP-API

Check the balance on Clickatell.com SMS gateway using HTTP-API 
Usage: check_clickatell_balance.py [options] 

Options: 

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

Tested on Python 2.7 with nagiosplugin 0.4.4 
Install nagiosplugin with 'easy_install nagiosplugin' 

Links:

https://exchange.nagios.org/directory/Addons/Active-Checks/check_clickatell_balance
