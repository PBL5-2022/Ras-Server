import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

in1 = 26
in2 = 19
pinpwm = 18
GPIO.setup(pinpwm, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

direction = int(input('Please define the direction (Left=1 or Right=2): '))
dc = int(input('Please define the Motor PWM Duty Cycle (0-100): '))
hz = int(input('HZ: '))
pwm = GPIO.PWM(pinpwm, hz)
print(direction)

if direction == 1:
    print("cc")
    GPIO.output(in1, 1)
    GPIO.output(in2, 0)
elif direction == 2:
    print("oke")
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)

try:
    while True:
        pwm.start(dc)

except KeyboardInterrupt:
    pwm.start(0)
    GPIO.cleanup()
