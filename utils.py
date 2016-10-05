#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import random
import subprocess

def getRandom(l):
    return l[random.randint(0, len(l)-1)]

def execCmdBackground(cmd):
    print(cmd)
    os.system('%s &' % cmd)

def execCmd(cmd):
    proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
    lines = []
    while True:
        line = proc.stdout.readline().decode("utf-8").strip("\n")
        if len(line) == 0:
            break
        lines.append(line)
    return lines

def getLights(info):
    lights = []
    for line in execCmd("python {0}".format(info)):
        lights.append(json.loads(line.strip("\n")))
    return lights

def getStateLight(info, lights=None):
    if lights == None:
        lights = getLights(info)
    for light in lights:
        if light["power"] > 0:
            return True
    return False
