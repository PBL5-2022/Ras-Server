import serial
from gpiozero import Buzzer
from datetime import datetime, timezone
import requests
import json
 
def timestamp(dt):
    return dt.replace(tzinfo=timezone.utc).timestamp() * 1000
import time
mytime = datetime.now()
ser = serial.Serial('/dev/ttyUSB0',9600)
s = [0,1]
buzzer = Buzzer(27)
while True:
    read_serial=ser.readline()
    value = int (ser.readline(),16)
    # print(timestamp(datetime.now()) - timestamp(mytime))
    if (timestamp(datetime.now()) - timestamp(mytime) > 3000 ):
        print("uhm");
        mytime = datetime.now()
        print(value)
        if value > 900 :
            requests.post(
                    'http://localhost:8000/notification', json={
                        "group_name" :'group_gas',
                        "target" : 'gas',
                        "type" : 'gas_collect',
                        "value" :json.dumps({"action": {'status': 1} , "name" : 'gas leakage warning'})
                    })
            buzzer.on()
        else :
            buzzer.off();
            
