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

sleep_time = 0.5

pi.set_servo_pulsewidth(PIN, 1500)
time.sleep(1)

while True:
    try:
        pi.set_servo_pulsewidth(PIN, 500)
        time.sleep(sleep_time)
        pi.set_servo_pulsewidth(PIN, 833)
        time.sleep(sleep_time)
        pi.set_servo_pulsewidth(PIN, 1166)
        time.sleep(sleep_time)
        pi.set_servo_pulsewidth(PIN, 1500)
        time.sleep(sleep_time)
        pi.set_servo_pulsewidth(PIN, 1833)
        time.sleep(sleep_time)
        pi.set_servo_pulsewidth(PIN, 2166)
        time.sleep(sleep_time)
        pi.set_servo_pulsewidth(PIN, 2500)
        time.sleep(sleep_time)
        pi.set_servo_pulsewidth(PIN, 2166)
        time.sleep(sleep_time)
        pi.set_servo_pulsewidth(PIN, 1833)
        time.sleep(sleep_time)
        pi.set_servo_pulsewidth(PIN, 1500)
        time.sleep(sleep_time)
        pi.set_servo_pulsewidth(PIN, 1166)
        time.sleep(sleep_time)
        pi.set_servo_pulsewidth(PIN, 833)
        time.sleep(sleep_time)
    #     pi.set_servo_pulsewidth(PIN, 1500)
    #     time.sleep(sleep_time)
    #     pi.set_servo_pulsewidth(PIN, 2000)
    #     time.sleep(sleep_time)
    #     pi.set_servo_pulsewidth(PIN, 1500)
    #     time.sleep(sleep_time)
    #     pi.set_servo_pulsewidth(PIN, 1000)
    #     time.sleep(sleep_time)
    except KeyboardInterrupt:
        break

print("\nTidying up")

pi.set_servo_pulsewidth(PIN, 0)

pi.stop()
