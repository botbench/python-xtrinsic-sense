import RPi.GPIO as GPIO
import smbus
import time
import xtrinsic_sense as xtrinsic

GPIO.setmode(GPIO.BOARD)
smbus = smbus.SMBus(1)
mma8491 = xtrinsic.MMA8491(smbus, GPIO, 0x55, 15)

while True:
  print mma8491.axes()
  time.sleep(1)
