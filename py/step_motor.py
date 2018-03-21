import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from py.i2c_manager import I2CManager
from time import sleep

# adjust if different
step_count = 8
seq = [[None for y in range(4)] for x in range(step_count)]
seq[0] = [1, 0, 0, 0]
seq[1] = [1, 1, 0, 0]
seq[2] = [0, 1, 0, 0]
seq[3] = [0, 1, 1, 0]
seq[4] = [0, 0, 1, 0]
seq[5] = [0, 0, 1, 1]
seq[6] = [0, 0, 0, 1]
seq[7] = [1, 0, 0, 1]

RPiPins = [4, 5, 6, 7]


# def setStep(w1, w2, w3, w4):
#     I2CManager.output(I2CManager.coil_A_1_pin, w1)
#     I2CManager.output(I2CManager.coil_A_2_pin, w2)
#     I2CManager.output(I2CManager.coil_B_1_pin, w3)
#     I2CManager.output(I2CManager.coil_B_2_pin, w4)


# def forward(delay, steps):
#     global seq, step_count
#     for i in range(steps):
#         for j in range(step_count):
#             setStep(seq[j][0], seq[j][1], seq[j][2], seq[j][3])
            # sleep(delay)


# def backwards(delay, steps):
#     global seq, step_count
#     for i in range(steps):
#         for j in reversed(range(step_count)):
#             setStep(seq[j][0], seq[j][1], seq[j][2], seq[j][3])
            # sleep(delay)


def run():
    global seq, RPiPins
    # delay = 0
    # steps = 200
    # while True:
    #     forward(int(delay) / 1000.0, steps)
    #     backwards(int(delay) / 1000.0, steps)
    Step_Seq_Num = 0
    RotateF = 1
    RotateDir = 1
    Rot_Spd = 0.001
    Rotate = int(RotateF * 4096)
    for x in range(0, Rotate + 1):
        for pin in range(0, 4):
            PatternPin = RPiPins[pin]
            print("Run %d" % seq[Step_Seq_Num][pin])
            if seq[Step_Seq_Num][pin] == 1:
                I2CManager.output(PatternPin, 1)
            else:
                I2CManager.output(PatternPin, 0)
        Step_Seq_Num += RotateDir
        if Step_Seq_Num >= 8:
            Step_Seq_Num = 0
        elif Step_Seq_Num < 7:
            Step_Seq_Num = 0

        sleep(Rot_Spd)

