#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from utils import getRandom
from lang import Lang

class Config:
    _config = {}
    _lang = Lang()
    def __init__(self):
        with open("config.json", "r", encoding="ISO-8859-1") as fd:
            self._config=json.load(fd)

    def get_lang(self, key):
        if key not in self._lang.lang:
            return "Key %s Language not found" % key
        ret = self._lang.get(key)[self.get("lang")]
        if type(ret) is list:
            return getRandom(ret)
        return ret

    def get(self, key):
        if key not in self._config:
            return "Key %s config not found" % key
        return self._config[key]
