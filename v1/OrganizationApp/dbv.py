MYSQL_DB    = 'edxapp'
MYSQL_USER  = "root"
MYSQL_PSWD  = "root"
MONGO_DB    = "edxapp"

import re
pattern = re.compile(r'[A-Za-z0-9_-][A-Za-z0-9 _-]*$')

s = '1'

if pattern.match(s):
    print 'yes'