#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

class Lang:
    lang = {}
    def __init__(self):
        with open("lang.json", "r", encoding="ISO-8859-1") as fd:
            self.lang=json.load(fd)

    def get(self, key):
        if key not in self.lang:
            return "Key %s language not found" % key
        return self.lang[key]
