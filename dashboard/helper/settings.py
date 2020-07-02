"""
Kraity Settings File:
    Using Python Syntax
    if 2 variable was exist the last one will be used
"""
# set this true to make dashboard automatically rendered in dark mode
# value type : boolean (True or False)
DARK_THEME = "False"


# session expire in seconds
# value type : integer (number)
SESSION_EXPIRE = 300


SYSLOG = "/var/log/syslog"

# getting help with dmesg --help
KERNLOG_PARAM = "dmesg --time-format ctime --color=never"


AUTHLOG = "/var/log/auth.log"


