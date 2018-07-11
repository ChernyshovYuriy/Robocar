## Robocar

This is prototype of a robot which is based on vehicle-like chassis and which is trying to self-drive in a closed area such as living room.
The goal of this project is to link together different types of sensors and try to manage those through software.
Obtained experience can be applied to different tasks of everyday life, for instance house keeping or garden keeping robots, robots which can handle factory related tasks, suach as load or unload cargo, etc ...

Computational unit is based on Raspberry Pi 3, programming language is Python.

Robocar consists of:

1. [Chassis](https://www.ebay.ca/sch/sis.html?_nkw=4WD+Smart+Robot+Car+Chassis+Kits+W%2F+Magneto+Speed+Encoder+For+Arduino+51+Replace&_id=162809513764&&_trksid=p2057872.m2749.l2658) (or similar, it is really an opened choice question).
2. [Rasbperry Pi 3, model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/).
3. Set of ultrasonic sensors [HC-SR04](https://www.ebay.ca/sch/sis.html?_nkw=HC-SR04+Ultrasonic+Module+Distance+Measuring+Transducer+Sensor+Mount+Bracket&_id=192394073637&&_trksid=p2057872.m2749.l2658).
4. [Octasonic 8 x HC-SR04 Ultrasonic Breakout Board](https://www.tindie.com/products/andygrove73/octasonic-8-x-hc-sr04-ultrasonic-breakout-board/) to handle ultrasonic sensors.
5. 2 DC motors, 5V, comes with cassis.
6. [L298N Dual H Bridge DC Motor Driver Controller](https://www.ebay.ca/sch/sis.html?_nkw=L298N+Dual+H+Bridge+DC+stepper+Motor+Driver+Controller+module+Board+for+ArduiCeV&_id=272998220971&&_trksid=p2057872.m2749.l2658).
7. [Port expander, I/O extension module, MCP23017 board, I2C](https://www.ebay.ca/sch/sis.html?_nkw=Port+expander%2C+I%2FO+extension+module%2C+MCP23017+board%2C+I2C%2C+Arduino%2CRaspberry-EU&_id=232073040811&&_trksid=p2057872.m2749.l2658) to expand GPIO ports in order to get more I/O.
8. [Wireless USB Adapter](https://www.ebay.ca/sch/i.html?_odkw=raspberri+pi+wireless+usb+adaptor+ourlink+802.11n+150v&_osacat=0&_from=R40&_trksid=m570.l1313&_nkw=raspberri+pi+wireless+usb+adaptor+ourlink+802.11n+150m&_sacat=0) to connect Raspberri Pi to internet.
9. Two power blocks. One is for the Raspberi Pi iteslf, another one is for motors.

TODO list:

1. Use [Gyroscope chip](https://www.ebay.ca/sch/sis.html?_nkw=High+Quality+GY-521+MPU-6050+Module+3-Axis+Acceleration+Gyro+Module+Arduino+CA&_id=292383350169&&_trksid=p2057872.m2749.l2658) to measure distance and movement which could help to build internal offline map of the area.
2. Equip with different sensors in order to process surrounded environment.

View of the prototype (not annotated, annotation is coming):

![Robocar view](https://bitbucket.org/ChernyshovYuriy/robocar/raw/aa9f61e1b011cbf8b574b4dec8208b67efea4958/py/img/robocar_1.jpg)

![Robocar view](https://bitbucket.org/ChernyshovYuriy/robocar/raw/aa9f61e1b011cbf8b574b4dec8208b67efea4958/py/img/robocar_2.jpg)

![Robocar view](https://bitbucket.org/ChernyshovYuriy/robocar/raw/aa9f61e1b011cbf8b574b4dec8208b67efea4958/py/img/robocar_3.jpg)

![Robocar view](https://bitbucket.org/ChernyshovYuriy/robocar/raw/aa9f61e1b011cbf8b574b4dec8208b67efea4958/py/img/robocar_4.jpg)

---