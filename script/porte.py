#!/usr/bin/python
import RPi.GPIO as GPIO
import sys
import time
import subprocess

porte=12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(porte, GPIO.OUT)
GPIO.output(porte, not GPIO.input(porte))
time.sleep(2)
GPIO.output(porte, not GPIO.input(porte))
time.sleep(2)
GPIO.cleanup()
