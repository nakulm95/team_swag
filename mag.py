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
f = open("results0.csv", "w+")
f1 = open("results1.csv", "w+")
count = 0
while True:
        try:
                data0 = bus0.read_i2c_block_data(0x0E, 0x01, 6)
                data1 = bus1.read_i2c_block_data(0x0E, 0x01, 6)
                
                xMag0 = data0[0] * 256 + data0[1]
                if xMag0 > 32767:
                        xMag0 -= 65536

                xMag1 = data1[0] * 256 + data1[1]
                if xMag1 > 32767:
                        xMag1 -= 65536

                        
                yMag0 = data0[2] * 256 + data0[3]
                if yMag0 > 32767:
                        yMag0 -= 65536

                yMag1 = data1[2] * 256 + data1[3]
                if yMag1 > 32767:
                        yMag1 -= 65536

                        
                zMag0 = data0[4] * 256 + data0[5]
                if zMag0 > 32767:
                      zMag0 -= 65536

                zMag1 = data1[4] * 256 + data1[5]
                if zMag1 > 32767:
                      zMag1 -= 65536
        

                f.write(str(count) + "," + str(xMag0) + "," + str(yMag0) + "," + str(zMag0) + "\n")
                f1.write(str(count) + "," + str(xMag1) + "," + str(yMag1) + "," + str(zMag1) + "\n")
                count += 1
        except IOError:
                print("woops2222222222222222222222222222222222222222222222222222222222222")
        time.sleep(0.0166667)
