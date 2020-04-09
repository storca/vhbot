import configparser
from colorama import Fore
"""
Reads from the config(s) file(s)
"""
conf = configparser.ConfigParser()

#Attempt to read from default settings
conf.read_file(open("default.conf", encoding="utf-8"))

#Attempt to read from instance configuration file
f = conf.read("instance.conf", encoding="utf-8")

#Read configuration and set it as local variable
for section in conf.sections():
    for key in conf[section]:
        locals()[key] = conf.get(section, key)

print(Fore.CYAN + "[CONFIGURATION] : " + Fore.RESET + "configuration read, command prefix is %s" % cmd_prefix)