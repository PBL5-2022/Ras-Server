import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

in1 = 19
in2 = 26
pwmPin = 18


# in1 = 5
# in2 = 6
# pwmPin = 17


GPIO.setup(pwmPin, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
# GPIO.output(pwmPin, 0)
# pwm = GPIO.PWM(pwmPin, 100)

GPIO.cleanup()
# stop
# pwm.stop()


# pwm = GPIO.PWM(pwmPin, 100)
# pwm.stop()
# GPIO.cleanup()


# GPIO.output(in1, 0)
# GPIO.output(in2, 1)

# pwm.start(30)
