Check the balance on Clickatell.com SMS gateway using HTTP-API
Usage: check_clickatell_balance.py [options] 

Check the balance on Clickatell.com SMS gateway using HTTP-API 

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

There is no git repository for it until now, I'll place the source on a git repo as soon as I find some time :) 
You'll find the complete source attached in the meantime. 
