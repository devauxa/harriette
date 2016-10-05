#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import json
import signal
import pickle
import random, string
from multiprocessing import Pool

from user import User
from config import Config
from utils import execCmdBackground, execCmd, getStateLight, getRandom

class Detect:
    listUser = []
    config = Config()
    state = {"nbUser": 0}
    user_waiting = ""
    lights = None

    def __init__(self):
        self.load()
        self.updateConfig()

    def save(self):
        with open(".user.pickle", "wb") as fd:
            pickle.dump(self.listUser, fd)
        with open(".state.pickle", "wb") as fd:
            pickle.dump(self.state, fd)

    def load(self):
        if os.path.exists(".user.pickle") == True:
            with open(".user.pickle", "rb") as lines:
                self.listUser = pickle.load(lines)
        if os.path.exists(".state.pickle") == True:
            with open(".state.pickle", "rb") as lines:
                self.state = pickle.load(lines)

    def updateConfig(self):
        with open("user.json", "r", encoding="ISO-8859-1") as fd:
            for user in json.load(fd):
                pos, user_find = self.findBy("mac", user["mac"])
                if pos == -1:
                    self.listUser.append(User(user, self.config))
                else:
                    self.listUser[pos].loadJson(user)
                    self.listUser[pos].config = self.config

    def findBy(self, key, value):
        for i, user in enumerate(self.listUser):
            d = user.__dict__
            if key in d and value in d[key]:
                return i, user
        return -1, None

    def nbUser(self):
        nb = 0
        nb_admin = 0
        for user in self.listUser:
            if user.last_date != None:
                if user.admin == True:
                    nb_admin += 1
                nb += 1
        return nb, nb_admin

    def genLink(self):
        link_ok = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32)) + ".php"
        link_ko = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32)) + ".php"
        pid = os.getpid()
        execCmdBackground("echo '<?php exec(\"./kill 2 %s\"); unlink(\"%s\"); unlink(__FILE__); ?>' > /var/www/html/%s" % (str(pid), link_ko, link_ok))
        execCmdBackground("echo '<?php exec(\"./kill 1 %s\"); unlink(\"%s\"); unlink(__FILE__); ?>' > /var/www/html/%s" % (str(pid), link_ok, link_ko))
        return link_ok, link_ko

    def callAdmin(self):
        link_ok, link_ko = self.genLink()
        for user in self.listUser:
            if user.last_date != None:
                self.user_waiting += getRandom(user.name) + " "
        execCmdBackground("{0} -s '{1}'".format(self.config.get("jarvis"), self.config.get_lang("CALL_ADMIN").format(self.user_waiting)))
        for user in self.listUser:
            if user.admin == True and user.email != None:
                execCmdBackground('echo "{0}" | mail -s "{1}\nContent-Type: text/html" {2}'.format(self.config.get_lang("MAIL_BODY").format(getRandom(user.name), self.user_waiting, link_ok, link_ko), self.config.get_lang("MAIL_TITLE"), user.email))

    def authorize(self):
        execCmdBackground("{0} -s '{1}'".format(self.config.get("jarvis"), self.config.get_lang("AUTHORIZE").format(self.user_waiting)))

    def unauthorize(self):
        execCmdBackground("{0} -s '{1}'".format(self.config.get("jarvis"), self.config.get_lang("UNAUTHORIZE").format(self.user_waiting)))

    def updateLights(self):
        self.lights = getStateLight(self.config.get("light_info"))

    def openDoor(self):
        execCmdBackground("python {0}".format(self.config.get("door")))

    def openLights(self):
        if self.lights == False:
            execCmdBackground("python {0} 100".format(self.config.get("light")))

    def closeLights(self):
        if self.lights == True:
            execCmdBackground("python {0} 0".format(self.config.get("light")))

    def run(self):
        while True:
            p = Pool(len(self.listUser))
            self.listUser = p.map(updateUser, self.listUser)
            p.close()
            p.terminate()
            p.join()
            nbUser, nbAdmin = self.nbUser()
            self.updateLights()
            if nbUser > 0 and self.state["nbUser"] < nbUser:
                if nbAdmin > 0:
                    self.openDoor()
                    self.openLights()
                else:
                    self.callAdmin()
            elif nbUser == 0:
                self.closeLights()
            self.state["nbUser"] = nbUser
            self.save()
            time.sleep(1)

def printUsers(users):
    for user in users:
        print(user.toJson())
            
def findUser(user):
    for line in execCmd("sudo arping -c 1 %s" % user.ip):
        if user.mac in line.strip():
            return True
    return False

def updateUser(user):
    user.update(findUser(user))
    return user

def getOK(signum, frame):
    detect.updateLights()
    detect.authorize()
    detect.openDoor()
    detect.openLights()
    
def getKO(signum, frame):
    detect.unauthorize()

detect = Detect()
signal.signal(signal.SIGUSR2, getOK)
signal.signal(signal.SIGUSR1, getKO)
detect.run()

