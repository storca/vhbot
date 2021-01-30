"""
Read documentation from config files and set them to local variables
"""

import configparser
from colorama import Fore
"""
Read some a r t
"""
artf = open("./ressources/text/art.txt", "r", encoding="utf8")
art = artf.read()
art = art.split("-$")
#print(secrets.choice(art))
print(art[0])
artf.close()
"""
Reads from the config(s) file(s)
"""
conf = configparser.ConfigParser()

# Attempt to read from default settings
conf.read_file(open("default.conf", encoding="utf-8"))

# Attempt to read from instance configuration file
f = conf.read("instance.conf", encoding="utf-8")

# Read configuration and set it as local variable
for section in conf.sections():
    for key in conf[section]:
        locals()[key] = conf.get(section, key)

print(Fore.CYAN + "[CONFIGURATION] : " + Fore.RESET + "configuration read, command prefix is %s" % cmd_prefix)
