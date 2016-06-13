# EE/CSE 475 Embedded Capstone
# Car detection
# Eeshan Londhe, Nakul Malhotra, Sorav Sharma, Henry Zhao

import smbus
import time
import sys
from datetime import datetime
import math
import json
import requests


with open("config.json") as json_file:
    json_data = json.load(json_file)


server_url = json_data["server"]
initialTime = time.time()

bus0 = smbus.SMBus(0)
bus1 = smbus.SMBus(1)
bus0.write_byte_data(0x0E, 0x10, 0x01)
bus1.write_byte_data(0x0E, 0x10, 0x01)
time.sleep(0.5)
f = open("sdfresults0.csv", "w+")
f1 = open("sdfresults1.csv", "w+")
log = open("log.txt", "w+")

initMagnitude0 = json_data["initMag0"]
initMagnitude1 = json_data["initMag1"]

carInBoolean = True
carOutBoolean = True

netCars = 0

carData = {"garageID": json_data["garageID"], "spots": 0, "address": json_data["address"]}

def main():
    global bus0, bus1, f, f1, log, initMagnitude0, initMagnitude1, netCars, initialTime, server_url, carInBoolean, carOutBoolean
    # magetometers are initialized the first time the system is set up
    if (initMagnitude0 == 0 and initMagnitude1 == 0):
        print "init called"
        initMags()

    count = 1

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

            magnitude0 = math.sqrt(math.pow(xMag0, 2) + math.pow(yMag0, 2) + math.pow(zMag0, 2)) # magnetometer0 reading
            magnitude1 = math.sqrt(math.pow(xMag1, 2) + math.pow(yMag1, 2) + math.pow(zMag1, 2)) # magnetometer1 reading


            print "dif0: " + str(magnitude0 - initMagnitude0)
            print "dif1: " + str(magnitude1 - initMagnitude1)

            # sees if either of the sensors detected anything
            sensor0Detect(magnitude0, magnitude1)
            sensor1Detect(magnitude0, magnitude1)


            if (math.fabs(magnitude0 - initMagnitude0) <= 10): # should be 10
                carInBoolean = True


            if (math.fabs(magnitude1 - initMagnitude1) <= 10): # should be 10
                carOutBoolean = True


            currTime = time.time()
            if (currTime - initialTime > 3 && netCars != 0):
                initialTime = currTime
                carData["spots"] = netCars
                netCars = 0

                print "requesting"
                r = requests.put("http://" + server_url + ":8080/garages/" + carData["garageID"], data=carData)
                # logs data everytime a request is made
                log.write("Current Time: " + currTime + ", " + "netCars: " + carData["netCars"] + ", " + "Status Code: " + r.status_code + ", " + "Text: " + r.text + "\n")


            # writes to a file for testing purposes

            #f.write(str(count) + "," + str(xMag0) + "," + str(yMag0) + "," + str(zMag0) + "\n")
            #f1.write(str(count) + "," + str(xMag1) + "," + str(yMag1) + "," + str(zMag1) + "\n")
        except IOError:
            print("magnetometer error, but its ok")
        count += 1
        time.sleep(0.0166667)

# returns true if a car is detected, false otherwise. Also updates the netCars value accordingly.
# this sensor is for the right lane
def sensor0Detect(magnitude0, magnitude1):
    global carInBoolean, netCars, initMagnitude0
    if ((magnitude0 - initMagnitude0) > 50 and carInBoolean): # should be 30
        print "0 Updated"
        carInBoolean = False
        netCars -= 1
        return True
    return False

# returns true if a car is detected, false otherwise. Also updates the netCars value accordingly.
# this sensor is for the left lane
def sensor1Detect(magnitude0, magnitude1):
    global carOutBoolean, netCars, initMagnitude1
    if ((magnitude1 - initMagnitude1) > 50 and carOutBoolean): # should be 30
        print "1 Updated"
        carOutBoolean = False
        netCars += 1
        return True
    return False

# initializes the magnetometers. Does this by averages 100 sample data points of the magnetometer data.
# only call this function when no cars or large metalic objects are near.

def initMags():
    global initMagnitude0, initMagnitude1, initialTime

    xMag0init = 0
    xMag1init = 0

    yMag0init = 0
    yMag1init = 0

    zMag0init = 0
    zMag1init = 0


    realX0 = 0
    realX1 = 0

    realY0 = 0
    realY1 = 0

    realZ0 = 0
    realZ1 = 0
    time.sleep(1)

    for i in range(100):

        data0 = bus0.read_i2c_block_data(0x0E, 0x01, 6)
        data1 = bus1.read_i2c_block_data(0x0E, 0x01, 6)

        # x
        xMag0init = data0[0] * 256 + data0[1]
        if xMag0init > 32767:
            xMag0init -= 65536

        realX0 += xMag0init

        xMag1init = data1[0] * 256 + data1[1]
        if xMag1init > 32767:
            xMag1init -= 65536

        realX1 += xMag1init

        # y
        yMag0init = data0[2] * 256 + data0[3]
        if yMag0init > 32767:
            yMag0init -= 65536

        realY0 += yMag0init

        yMag1init = data1[2] * 256 + data1[3]
        if yMag1init > 32767:
            yMag1init -= 65536

        realY1 += yMag1init

        # z
        zMag0init = data0[4] * 256 + data0[5]
        if zMag0init > 32767:
            zMag0init -= 65536

        realZ0 += zMag0init

        zMag1init = data1[4] * 256 + data1[5]
        if zMag1init > 32767:
            zMag1init -= 65536

        realZ1 += zMag1init


    realX0 = realX0 / 100.0
    realY0 = realY0 / 100.0
    realZ0 = realZ0 / 100.0

    realX1 = realX1 / 100.0
    realY1 = realY1 / 100.0
    realZ1 = realZ1 / 100.0

    initMagnitude0 = math.sqrt(math.pow(realX0, 2) + math.pow(realY0, 2) + math.pow(realZ0, 2))
    initMagnitude1 = math.sqrt(math.pow(realX1, 2) + math.pow(realY1, 2) + math.pow(realZ1, 2))

    json_data["initMag0"] = initMagnitude0
    json_data["initMag1"] = initMagnitude1

    print "0: " + str(initMagnitude0)
    print "1: " + str(initMagnitude1)

    # updates json file
    with open("config.json", 'w') as outfile:
        json.dump(json_data, outfile)

    # makes a post request until the request succeeds
    while requests.post("http://" + server_url + ":8080/garages", data=json_data).status_code != 200:
       pass

    initialTime = time.time()

main()
