import Adafruit_DHT
import channels
import json
print(Adafruit_DHT.__file__)
print(channels.__version__)
# print(asgiref.sync.__file__)
x = {"name": "John", "age": 30, "city": "New York"}
s = json.dumps(x)
print(x["name"])
