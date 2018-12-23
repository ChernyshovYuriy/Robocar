## Robocar

This is prototype of a robot which is based on vehicle-like chassis and which is trying to self-drive in a closed area such as living room.
The goal of this project is to link together different types of sensors and try to manage those through software.
Obtained experience can be applied to different tasks of everyday life, for instance house keeping or garden keeping robots, robots which can handle factory related tasks, suach as load or unload cargo, etc ...

Computational unit is based on Raspberry Pi 3, programming language is Python 3.

Robocar consists of:

1. Chassis - LEGO.
2. [Rasbperry Pi 3, model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/).
3. Set of ultrasonic sensors [HC-SR04](https://www.ebay.ca/sch/sis.html?_nkw=HC-SR04+Ultrasonic+Module+Distance+Measuring+Transducer+Sensor+Mount+Bracket&_id=192394073637&&_trksid=p2057872.m2749.l2658).
4. [Octasonic 8 x HC-SR04 Ultrasonic Breakout Board](https://www.tindie.com/products/andygrove73/octasonic-8-x-hc-sr04-ultrasonic-breakout-board/) to handle ultrasonic sensors.
5. 2 DC motors, 5V.
6. [L298N Dual H Bridge DC Motor Driver Controller](https://www.ebay.ca/sch/sis.html?_nkw=L298N+Dual+H+Bridge+DC+stepper+Motor+Driver+Controller+module+Board+for+ArduiCeV&_id=272998220971&&_trksid=p2057872.m2749.l2658).
7. [Port expander, I/O extension module, MCP23017 board, I2C](https://www.ebay.ca/sch/sis.html?_nkw=Port+expander%2C+I%2FO+extension+module%2C+MCP23017+board%2C+I2C%2C+Arduino%2CRaspberry-EU&_id=232073040811&&_trksid=p2057872.m2749.l2658) to expand GPIO ports in order to get more I/O.
8. [Gyroscope chip](https://www.ebay.ca/sch/sis.html?_nkw=High+Quality+GY-521+MPU-6050+Module+3-Axis+Acceleration+Gyro+Module+Arduino+CA&_id=292383350169&&_trksid=p2057872.m2749.l2658) to measure distance and movement which could help to build internal offline map of the area.
9. [LM393 Optocoupler Detection Sensor Module](https://www.ebay.ca/sch/sis.html?_nkw=LM393+Speed+Optocoupler+Detection+Sensor+Module+for+Arduino+Raspberry+Pi&_id=391323881559&&_trksid=p2057872.m2749.l2658) to track wheel pulse , for instance to detect speed.
10. Two power blocks. One is for the Raspberi Pi itself, another one is for motors.

TODO list:

1. Equip with LIDAR in order to process surrounded environment.

[Android application (in develop)](https://bitbucket.org/ChernyshovYuriy/robocarandroidcontroller/src/master) to controll Robocar.

View of the prototype (details are in [Wiki](https://bitbucket.org/ChernyshovYuriy/robocar/wiki/Home)):

![Robocar view](https://bitbucket.org/ChernyshovYuriy/robocar/raw/f6376b509c4f85a6c8afbff9bf061661fe4006e8/img/robocar.jpg)

---