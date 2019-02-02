#!/usr/bin/env python3

"""
Found from https://github.com/pybluez/pybluez/blob/master/examples/simple/inquiry.py
    1/27/2019
"""

import bluetooth

print("Searching for Bluetooth devices...")
nearby = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
print("There are {} devices nearby:".format(len(nearby)))

for addr, name in nearby:
    try:
        print("    {} - {}".format(addr, name))
    except UnicodeEncodeError:
        print("    {} - {}".format(addr, name.encode('utf-8', 'replace')))
