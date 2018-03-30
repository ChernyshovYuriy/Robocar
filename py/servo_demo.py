#!/usr/bin/env python

# servo_demo.py
# 2016-10-07
# Public Domain

import time

import pigpio

PIN = 4

pi = pigpio.pi()

if not pi.connected:
    exit()

while True:

    try:
        pi.set_servo_pulsewidth(PIN, 500)
        time.sleep(1)
        pi.set_servo_pulsewidth(PIN, 2500)
        time.sleep(1)
    except KeyboardInterrupt:
        break

print("\nTidying up")

pi.set_servo_pulsewidth(PIN, 0)

pi.stop()
