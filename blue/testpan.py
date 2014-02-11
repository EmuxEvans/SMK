#!/usr/bin/python

import sys
import time
import dbus
from optparse import OptionParser, make_option

bus = dbus.SystemBus()

manager = dbus.Interface(bus.get_object("org.bluez", "/"),
                         "org.bluez.Manager")

option_list = [
    make_option("-i", "--device", action="store",
                type="string", dest="dev_id"),
]
parser = OptionParser(option_list=option_list)

(options, args) = parser.parse_args()

if options.dev_id:
    adapter_path = manager.FindAdapter(options.dev_id)
else:
    adapter_path = manager.DefaultAdapter()

server = dbus.Interface(bus.get_object("org.bluez", adapter_path),
                        "org.bluez.NetworkServer")

service = "nap"

if (len(args) < 1):
    bridge = "tether"
else:
    bridge = args[0]

server.Register(service, bridge)

print "Server for %s registered for %s" % (service, bridge)

print "Press CTRL-C to disconnect"

try:
    time.sleep(1000)
    print "Terminating connection"
except:
    pass

server.Unregister(service)
