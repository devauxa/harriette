#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import time
import json
from utils import getRandom, execCmdBackground

class User:
    admin = False
    def __init__(self, jsonUser, config):
        self.loadJson(jsonUser)
        self.config = config
        self.last_date = None

    def leave(self):
        execCmdBackground('{0} -s "{1}"'.format(self.config.get("jarvis"), self.config.get_lang("DISCONNECTED").format(getRandom(self.name))))

    def enter(self):
        execCmdBackground('{0} -s "{1}"'.format(self.config.get("jarvis"), self.config.get_lang("CONNECTED").format(getRandom(self.name))))

    def update(self, find=True):
        if find == True:
            if self.last_date == None:
                self.enter()
            self.last_date = time.time()
        elif self.last_date != None and time.time() - self.last_date > 200:
            self.last_date = None
            self.leave()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def loadJson(self, jsonUser):
        self.mac = jsonUser["mac"]
        self.ip = jsonUser["ip"]
        self.name = jsonUser["name"]
        if "tel" in jsonUser:
            self.tel = jsonUser["tel"]
            self.admin = True
        if "email" in jsonUser:
            self.email = jsonUser["email"]
            self.admin = True
