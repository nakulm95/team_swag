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
#f = open("results0.csv", "w+")
#f1 = open("results1.csv", "w+")
log = open("log.txt", "w+")

initMagnitude0 = json_data["initMag0"]
initMagnitude1 = json_data["initMag0"]

carInBoolean = True
carOutBoolean = True

netCars = 0


carData = {"garageID": "Team Swag Garage", "netCars": 0}

if (initMagnitude0 == 0 and initMagnitude1 == 0):
    initMags()

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

        if ((magnitude0 - initMagnitude0) < -30 and carInBoolean):
            carInBoolean = False
            netCars -= 1
        if ((magnitude1 - initMagnitude1) < -30 and carOutBoolean):
            carOutBoolean = False
            netCars += 1


        if (Math.abs(magnitude0 - initMagnitude0) <= 10):
            carInBoolean = True

        if (Math.abs(magnitude1 - initMagnitude1) <= 10):
            carOutBoolean = True


        currTime = time.time()
        if (currTime - initialTime > 59):
            initialTime = currTime
            carData["netCars"] = netCars
            netCars = 0
            r = requests.post(server_url, data=json.dumps(carData))
            log.write("Current Time: " + currTime + ", " + "netCars: " + carData["netCars"] + ", " + "Status Code: " + r.status_code + ", " + "Text: " + r.text)
            # TODO: reset log file every month
            # TODO: new thread for communicating with the server


        #f.write(str(count) + "," + str(xMag0init) + "," + str(yMag0init) + "," + str(zMag0init) + "\n")
        #f1.write(str(count) + "," + str(xMag1init) + "," + str(yMag1init) + "," + str(zMag1init) + "\n")
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

    for i in range(100):

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

    json_data["initMag0"] = initMagnitude0
    json_data["initMag1"] = initMagnitude1

    with open("config.json", 'w') as outfile:
        json.dump(json_data, outfile)


    while (requests.post(server_url + "/init", data=json.dumps(json_data)).status_code != 200):
        pass

    initialTime = time.time()
