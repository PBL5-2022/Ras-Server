
import RPi.GPIO as GPIO
import time
import sqlite3
import requests
dbname = '/home/pi/MyPBL5/DjangoAPI/mysln/db.sqlite3'


class Led:
    def __init__(self):
        self.ledpin = [12, 20]
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.ledpin[0], GPIO.OUT)
        GPIO.setup(self.ledpin[1], GPIO.OUT)

    def turnOn(self, lednum, issocketused=True):
        GPIO.output(self.ledpin[lednum], GPIO.HIGH)
        self.logData("1", lednum, issocketused)
        return f"Led{lednum} on"

    def turnOff(self, lednum, issocketused=True):
        GPIO.output(self.ledpin[lednum], GPIO.LOW)
        self.logData("0", lednum, issocketused)
        return f"Led{lednum} off"

    def status(self, lednum):
        if(GPIO.input(self.ledpin[self.lednum]) == GPIO.LOW):
            return f"Led{lednum} off"
        if(GPIO.input(self.ledpin[self.lednum]) == GPIO.HIGH):
            return f"Led{lednum} on"

    def logData(self, status, lednum, issocketused):
        try:
            ledname = "Led"+str(lednum)
            conn = sqlite3.connect(dbname)
            curs = conn.cursor()

            curs.execute(
                "INSERT INTO myapi_led_data(timestamp,status,ledname) values(datetime('now'), (?),(?))", (status, ledname))
            if status == "1":
                status = "on"
            else:
                status = "off"
            curs.execute(
                "UPDATE myapi_device SET status = (?) WHERE name = (?)", (status, ledname))
            conn.commit()
            conn.close()

            if issocketused == False:
                response = requests.post(
                    'http://localhost:8000/led', data={
                        "status": status,
                        "ledname": ledname
                    })

        except Exception as e:
            print(e)


if __name__ == "__main__":
    g = Led()
    if g.status == "On":
        g.turnOff(False)
    else:
        g.turnOn(False)
    g.turnOff(False)
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
