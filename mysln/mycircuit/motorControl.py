import RPi.GPIO as GPIO
import os
import time
import traceback


class MotorControl:
    def __init__(self):
        self.file_path = "/home/pi/MyPBL5/DjangoAPI/mysln/mycircuit/data_motor.txt"
        self.modifiedOn = os.path.getmtime(self.file_path)

        self.pwmPinA = 17
        self.in1 = 5
        self.in2 = 6

        # self.pwmPinB = 13
        # self.in3 = 27
        # self.in4 = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pwmPinA, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)

        # GPIO.setup(self.pwmPinB, GPIO.OUT)
        # GPIO.setup(self.in3, GPIO.OUT)
        # GPIO.setup(self.in4, GPIO.OUT)

        GPIO.output(self.in1, 0)
        GPIO.output(self.in2, 1)

        self.pwmA = GPIO.PWM(self.pwmPinA, 100)

    def detectChange(self):
        value1 = 0
        try:
            while (True):
                time.sleep(0.5)
                modified = os.path.getmtime(self.file_path)
                if modified != self.modifiedOn:
                    self.modifiedOn = modified
                    value1 = self.readFile()
                    print(value1)
                if value1 == 0:
                    self.pwmA.stop()
                else:
                    self.pwmA.start(value1)

        except Exception as e:
            print(traceback.format_exc())

    def readFile(self):
        value1 = 0
        with open(self.file_path) as f:
            lines = f.readlines()
            for line in lines:
                line = line.split(",")
                print(f"{line[0]}{line[1]}")
                if str(line[0].strip()) == "motor1":
                    value1 = int(line[1])

        f.close()
        return value1


if __name__ == "__main__":
    g = MotorControl()
    g.detectChange()
