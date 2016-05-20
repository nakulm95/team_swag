import smbus
import time
import sys
from datetime import datetime
import math

bus0 = smbus.SMBus(0)
bus1 = smbus.SMBus(1)
bus0.write_byte_data(0x0E, 0x10, 0x01)
bus1.write_byte_data(0x0E, 0x10, 0x01)
time.sleep(0.5)
#f = open("results0.csv", "w+")
#f1 = open("results1.csv", "w+")

initMagnitude0 = 0
initMagnitude1 = 0

carInBoolean = True
carOutBoolean = True

spotsAvailable = 500

initMags()


count = 0
while True:
    try:

        data0 = bus0.read_i2c_block_data(0x0E, 0x01, 6)
        data1 = bus1.read_i2c_block_data(0x0E, 0x01, 6)

        # x
        xMag0 = data0[0] * 256 + data0[1]
        if xMag0 > 32767:
            xMag0 -= 65536
        xMag1 = data1[0] * 256 + data1[1]
        if xMag1 > 32767:
            xMag1 -= 65536

        # y
        yMag0 = data0[2] * 256 + data0[3]
        if yMag0 > 32767:
            yMag0 -= 65536
        yMag1 = data1[2] * 256 + data1[3]
        if yMag1 > 32767:
            yMag1 -= 65536

        # z
        zMag0 = data0[4] * 256 + data0[5]
        if zMag0 > 32767:
            zMag0 -= 65536
        zMag1 = data1[4] * 256 + data1[5]
        if zMag1 > 32767:
            zMag1 -= 65536

        magnitude0 = math.sqrt(math.pow(xMag0, 2) + math.pow(yMag0, 2) + math.pow(zMag0, 2))
        magnitude1 = math.sqrt(math.pow(xMag1, 2) + math.pow(yMag1, 2) + math.pow(zMag1, 2))

        if ((magnitude0 - initMagnitude0) < -30 && carInBoolean)
            carInBoolean = False
            # carin++
        if ((magnitude1 - initMagnitude1) < -30 && carOutBoolean)
            carOutBoolean = False
            #carout++


        if (Math.abs(magnitude0 - initMagnitude0) <= 10)
            carInBoolean = True

        if (Math.abs(magnitude0 - initMagnitude0) <= 10)
            carOutBoolean = True


        #f.write(str(count) + "," + str(xMag0init) + "," + str(yMag0init) + "," + str(zMag0init) + "\n")
        #f1.write(str(count) + "," + str(xMag1init) + "," + str(yMag1init) + "," + str(zMag1init) + "\n")
        count += 1
    except IOError:
        print("woops2222222222222222222222222222222222222222222222222222222222222")
    time.sleep(0.0166667)


def initMags():

    xMag0init = 0
    xMag1init = 0

    yMag0init = 0
    yMag1init = 0

    zMag0init = 0
    zMag1init = 0

    for (i in range(100)):

        data0 = bus0.read_i2c_block_data(0x0E, 0x01, 6)
        data1 = bus1.read_i2c_block_data(0x0E, 0x01, 6)

        # x
        xMag0init += data0[0] * 256 + data0[1]
        if xMag0init > 32767:
            xMag0init -= 65536
        xMag1init += data1[0] * 256 + data1[1]
        if xMag1init > 32767:
            xMag1init -= 65536

        # y
        yMag0init += data0[2] * 256 + data0[3]
        if yMag0init > 32767:
            yMag0init -= 65536
        yMag1init += data1[2] * 256 + data1[3]
        if yMag1init > 32767:
            yMag1init -= 65536

        # z
        zMag0init += data0[4] * 256 + data0[5]
        if zMag0init > 32767:
            zMag0init -= 65536
        zMag1init += data1[4] * 256 + data1[5]
        if zMag1init > 32767:
            zMag1init -= 65536

    xMag0init = xMag0init / 100
    yMag0init = yMag0init / 100
    zMag0init = zMag0init / 100

    xMag1init = xMag1init / 100
    yMag1init = yMag1init / 100
    zMag1init = zMag1init / 100

    initMagnitude0 = math.sqrt(math.pow(xMag0init, 2) + math.pow(yMag0init, 2) + math.pow(zMag0init, 2))
    initMagnitude1 = math.sqrt(math.pow(xMag1init, 2) + math.pow(yMag1init, 2) + math.pow(zMag1init, 2))
