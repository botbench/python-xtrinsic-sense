#!/usr/bin/python
import RPi.GPIO as GPIO
import smbus
import time
import xtrinsic_sense as xtrinsic

GPIO.setmode(GPIO.BOARD)
smbus = smbus.SMBus(1)
mma8491 = xtrinsic.MMA8491(smbus, GPIO, 0x55, 15)
mag3110 = xtrinsic.MAG3110(smbus, 0x0E)
mpl3115 = xtrinsic.MPL3115(smbus, 0x60)

while True:
  #print mma8491.axes()
  #print mag3110.axes()
  print mpl3115.pressure()
  print mpl3115.temperature()
  time.sleep(1)
