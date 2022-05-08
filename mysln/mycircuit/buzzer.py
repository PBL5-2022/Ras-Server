from gpiozero import Buzzer
from time import sleep
buzzer = Buzzer(27)

while True:
    try:
        buzzer.on()
    except KeyboardInterrupt:
        buzzer.off()
        GPIO.cleanup()