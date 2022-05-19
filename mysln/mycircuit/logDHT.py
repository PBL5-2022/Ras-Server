import json
import time
import sqlite3
import Adafruit_DHT
import requests
dbname = '/home/pi/Ras-Server/mysln/db.sqlite3'
sampleFreq = 1  # time in seconds

# get data from DHT sensorcd


class LogDHT:
    def __init__(self):
        self.destination = "group_logDHT11"

    def getDHTdata(self):

        DHT11Sensor = Adafruit_DHT.DHT11
        DHTpin = 16
        hum, temp = Adafruit_DHT.read_retry(DHT11Sensor, DHTpin)

        if hum is not None and temp is not None:
            hum = round(hum)
            temp = round(temp, 1)
        return temp, hum

    # log sensor data on database

    def logData(self, temp, hum):
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()

        curs.execute(
            "INSERT INTO myapi_dht_data(timestamp,temp,hum) values(datetime('now'), (?), (?))", (temp, hum))
        conn.commit()
        conn.close()

    # main function

    def test(self):
        while True:
            temp, hum = self.getDHTdata()
            self.logData(temp, hum)
            # with open("/home/pi/timestamp.txt", "a") as f:
            #     f.write("Temp is: " + str(temp) + "Hum is : "+str(hum) + "\n")
            #     f.close()
            # response = requests.post(
            #     'http://localhost:8000/dht11/', data={'temp': temp,
            #                                           'hump': hum})


            requests.post(
                    'http://localhost:8000/notification', json={
                        "group_name" :'group_dht11',
                        "target" : 'dht11',
                        "type" : 'logDHT11_collect',
                        "value" :json.dumps({"action": {'temp': temp,'hump': hum} , "name" : 'temperature and humidity sensor'})
                    })

            time.sleep(sampleFreq)

    # ------------ Execute program
if __name__ == "__main__":
    g = LogDHT()
    g.test()
