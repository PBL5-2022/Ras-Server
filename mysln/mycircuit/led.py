
import RPi.GPIO as GPIO
import time
import sqlite3
dbname = '/home/pi/MyPBL5/DjangoAPI/mysln/db.sqlite3'


class Led:
    def __init__(self):
        self.ledpin = 20
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.ledpin, GPIO.OUT)

    def turnOn(self):
        GPIO.output(self.ledpin, GPIO.HIGH)
        self.logData("1")
        return "Turned on successfullly"

    def turnOff(self):
        GPIO.output(self.ledpin, GPIO.LOW)
        self.logData("0")
        return "Turned off successfullly"

    def status(self):
        if(GPIO.input(self.ledpin) == GPIO.LOW):
            return "Off"
        if(GPIO.input(self.ledpin) == GPIO.HIGH):
            return "On"

    def logData(self, status):

        conn = sqlite3.connect(dbname)
        curs = conn.cursor()

        curs.execute(
            "INSERT INTO myapi_led_data(timestamp,status) values(datetime('now'), (?))", status)
        conn.commit()
        conn.close()


if __name__ == "__main__":
    g = Led()
    if g.status == "On":
        g.turnOff()
    else:
        g.turnOn()
    print(g.status())

# Ledpin = 20
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(Ledpin, GPIO.OUT)

# # While loop
# # while True:
# #     # set GPIO14 pin to HIGH
# #     GPIO.output(Ledpin, GPIO.HIGH)
# #     # show message to Terminal
# #     print("LED is ON")
# #     # pause for one second
# #     time.sleep(1)

# #     # set GPIO14 pin to HIGH
# #     GPIO.output(Ledpin, GPIO.LOW)
# #     # show message to Terminal
# #     print("LED is OFF")
# #     # pause for one second
# #     time.sleep(1)
# GPIO.output(Ledpin, GPIO.LOW)
