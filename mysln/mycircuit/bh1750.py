import smbus
import time
import json
import sqlite3
import os
import requests
import decimal
dbname = '/home/pi/MyPBL5/DjangoAPI/mysln/db.sqlite3'
sampleFreq = 1  # time in seconds
# Define some constants from the datasheet

DEVICE = 0x23  # Default device I2C address

POWER_DOWN = 0x00  # No active state
POWER_ON = 0x01  # Power on
RESET = 0x07  # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

# bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1


def convertToNumber(data):
    # Simple function to convert 2 bytes of data
    # into a decimal number. Optional parameter 'decimals'
    # will round to specified number of decimal places.
    result = (data[1] + (256 * data[0])) / 1.2
    return (result)


def readLight(addr=DEVICE):
    # Read data from I2C interface
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)


def logData(lightLevel):
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    curs.execute(
        "INSERT INTO myapi_bh1750_data(timestamp,lightlevel) values(datetime('now'), (?))", [lightLevel])
    conn.commit()
    conn.close()


def main():
    while True:
        try:
            lightLevel = readLight()
            logData(format(lightLevel, '.2f'))
            # with open("/home/pi/MyPBL5/DjangoAPI/mysln/trainmodel/train_bh1750.json", "r") as f:
            #     data = json.loads(f.read())
            #     if data['status'] == True:
            #         if lightLevel < data['threshold']:
            #             os.system(
            #                 f"lib-circuit {data['devicenum']} --on{data['device']}")
            #         else:
            #             os.system(
            #                 f"lib-circuit {data['devicenum']} --off{data['device']}")
            #         f.close()

            # print("Light Level : " + format(lightLevel, '.2f') + " lx")
            response = requests.post(
                'http://localhost:8000/bh1750', data={'light': format(lightLevel, '.2f')})
            time.sleep(sampleFreq)
        except Exception as e:
            pass


if __name__ == "__main__":
    main()
