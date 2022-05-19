import RPi.GPIO as GPIO
import os
import time
import traceback
import json
import requests 

class MotorControl:
    def __init__(self):
        self.file_path = "/home/pi/Ras-Server/mysln/mycircuit/data_motor.txt"
        self.modifiedOn = os.path.getmtime(self.file_path)

        self.pwmPinA = 17
        self.in1 = 5
        self.in2 = 6

        # self.pwmPinB = 18
        # self.in3 = 19
        # self.in4 = 26
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

        # GPIO.output(self.in3, 0)
        # GPIO.output(self.in4, 1)

        self.pwmA = GPIO.PWM(self.pwmPinA, 50)
        # self.pwmB = GPIO.PWM(self.pwmPinB, 50)

    def detectChange(self):
        valueA = 0
        valueB = 0
        try:
            while (True):
                time.sleep(0.5)
                modified = os.path.getmtime(self.file_path)
                if modified != self.modifiedOn:
                    self.modifiedOn = modified
                    valueA, valueB = self.readFile()
                    print(f"{valueA} {valueB}")
                    self.pwmA.start(valueA)
                    # self.pwmB.ChangeDutyCycle(valueB)

        except Exception as e:
            print(traceback.format_exc())

    def readFile(self):
        valueA = 0
        valueB = 0
        
        with open(self.file_path) as f:
            lines = f.readlines()
            for line in lines:
                line = line.split(",")
                if str(line[0].strip()) == "motor1":
                    valueA = int(line[1])
                if str(line[0].strip()) == "motor2":
                    valueB = int(line[1])

        f.close()
        return (valueA, valueB)


if __name__ == "__main__":
    g = MotorControl()
    g.detectChange()
