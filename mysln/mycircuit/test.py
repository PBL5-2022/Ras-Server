import os
# os.system("sudo systemctl stop logDHT.service")
status = os.system('systemctl is-active --quiet logDHT.service')
print(status)
