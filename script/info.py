#!/usr/bin/env python
from lifxlan import *
import json
import sys

def main():
    lifx = LifxLAN()
    devices = lifx.get_lights()    
    for d in devices:
        print(json.dumps({"label" : d.get_label(), "power": d.get_power()}))

if __name__=="__main__":
    main()
