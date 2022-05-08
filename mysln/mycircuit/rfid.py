import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from gpiozero import Buzzer
from time import sleep
import signal
import time
import os
import requests
file_path = "/home/pi/Ras-Server/mysln/mycircuit/data_rfid.txt"
 
####rfid
reader = SimpleMFRC522()
buzzer = Buzzer(27)
checkDoor = False;
countFalse = 0;
trigger = False;
readCardTimer = 0
timer = 0

####servo
servoPIN = 40
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
p.start(2)  # Initialization

####led
ledpin=33;
GPIO.setwarnings(False)
GPIO.setup(ledpin, GPIO.OUT)

modifiedOn = os.path.getmtime(file_path)
try:
    while True:
        modified = os.path.getmtime(file_path)
        if modified != modifiedOn:
            modifiedOn = modified
            with open(file_path) as f:
                lines = f.readlines()
                for line in lines:
                    line = line.split(":")
                    if str(line[0].strip()) == "trigger":
                        if line[1].strip() == "False" :
                            trigger =False;
                        else : 
                            trigger = True
                    if str(line[0].strip()) == "countFalse":
                        countFalse = int(line[1].strip())
                    if str(line[0].strip()) == "checkDoor":
                        if line[1].strip() == "False" :
                            checkDoor =False;
                        else : 
                            checkDoor = True
            f.close()
            if trigger :
                if checkDoor == True :
                    action = 'on'
                else :
                    action = 'off'
                
                if countFalse >3 :
                    action ='warning'
                response = requests.post(
                        'http://localhost:8000/door-notification', data={
                            "action": action
                        })

            


        print(f"count false : {countFalse}")
        if countFalse > 3 : 
            buzzer.on()
 
        if (trigger == True) :
            if (checkDoor) :
                p.ChangeDutyCycle(7.5)
                print("uhm")
                GPIO.output(ledpin, GPIO.HIGH)
                timer = (round(time.time() * 1000))
                buzzer.off();
            else :
                p.ChangeDutyCycle(2)
                print("Wrong")
                if (countFalse <= 3):
                    GPIO.output(ledpin, GPIO.HIGH)
                    time.sleep(0.2);
                    GPIO.output(ledpin, GPIO.LOW)
            trigger = False;
            with open(file_path, 'r') as file:
                data = file.readlines()
                data[0] = f'trigger:False\n'
            with open(file_path, 'w') as file:
                file.writelines(data)
            file.close()

        if checkDoor == True and (round(time.time() * 1000))  - timer > 5000 : 
            with open(file_path, 'r') as file:
                data = file.readlines()
                data[0] = f'trigger:True\n'
                data[1] = f'countFalse:{0}\n'
                data[2] = f'checkDoor:{False}\n'
            with open(file_path, 'w') as file:
                file.writelines(data)
            file.close()
     
        if ((round(time.time() * 1000)) - readCardTimer >= 500):
            print("Hold a tag near the reader")

            id, text =  reader.read_no_block()
            if id  : 
                trigger = True;
                print("what id")
                print(id)
                if id == 763296750621 : 
                    print("righttttttt")
                    countFalse = 0;
                    checkDoor = True;
                else :
                    print("ei dc")
                    countFalse += 1;
                    checkDoor = False;

                readCardTimer = (round(time.time() * 1000))

                with open(file_path, 'r') as file:
                    data = file.readlines()
                    data[0] = f'trigger:True\n'
                    data[1] = f'countFalse:{countFalse}\n'
                    data[2] = f'checkDoor:{checkDoor}\n'
                with open(file_path, 'w') as file:
                    file.writelines(data)
                file.close()
        
except KeyboardInterrupt:
    GPIO.cleanup()
    raise