import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

in1 = 15
in2 = 14
pwmPin = 17
GPIO.setup(pwmPin, GPIO.OUT)
GPIO.output(pwmPin, 0)
# GPIO.setup(in1, GPIO.OUT)
# GPIO.setup(in2, GPIO.OUT)


# pwm = GPIO.PWM(pwmPin, 100)
# pwm.stop()
# GPIO.cleanup()


# GPIO.output(in1, 0)
# GPIO.output(in2, 1)

# pwm.start(30)
