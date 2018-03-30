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

idx = 0
direction = True
sleep_time = 0.15
steps = [500, 833, 1166, 1500, 1833, 2166, 2500]

pi.set_servo_pulsewidth(PIN, 500)
time.sleep(1)

# while True:
#     try:
#         print("Step:%d" % steps[idx])
#         pi.set_servo_pulsewidth(PIN, steps[idx])
#         time.sleep(sleep_time)
#
#         if direction:
#             idx += 1
#         else:
#             idx -= 1
#         if idx == len(steps) - 1:
#             direction = False
#         if idx == 0:
#             direction = True
#     except KeyboardInterrupt:
#         break

for i in range(0, 50):
    print("Iteration %d, Step:%d" % (i, steps[idx]))
    pi.set_servo_pulsewidth(PIN, steps[idx])
    time.sleep(sleep_time)

    if direction:
        idx += 1
    else:
        idx -= 1
    if idx == len(steps) - 1:
        direction = False
    if idx == 0:
        direction = True

print("\nTidying up")

pi.set_servo_pulsewidth(PIN, 0)

pi.stop()
