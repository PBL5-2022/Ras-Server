import RPi.GPIO as GPIO
import time

servoPIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
# GPIO.cleanup()

p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
p.start(2)  # Initialization
time.sleep(2.5)
try:
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    p.ChangeDutyCycle(2)
    time.sleep(0.5)

    #     while True:
    #         print("cc")

    #         p.ChangeDutyCycle(5)
    #         time.sleep(0.5)
    #         p.ChangeDutyCycle(7.5)
    #         time.sleep(0.5)
    #         p.ChangeDutyCycle(10)
    #         time.sleep(0.5)
    #         p.ChangeDutyCycle(12.5)
   
    
    #         time.sleep(0.5)
    #         p.ChangeDutyCycle(10)
    #         time.sleep(0.5)
    #         p.ChangeDutyCycle(7.5)
    #         time.sleep(0.5)
    #         p.ChangeDutyCycle(5)
    #         time.sleep(0.5)
    #         p.ChangeDutyCycle(2.5)
    #         time.sleep(0.5)
    p.stop()
    GPIO.cleanup()
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
