import os
import datetime
# os.system("sudo systemctl stop logDHT.service")
status = os.system('systemctl is-active --quiet logDHT.service')
s = "Led1"
x = s.replace("Led","")
print(datetime.datetime.now())
print(status)
