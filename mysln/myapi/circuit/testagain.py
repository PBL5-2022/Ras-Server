from myapi.consumers import NotificationConsumer
import json
NotificationConsumer.send(json.dumps({
    "type": "websocket.send",
            "data": event
}))
print("hello")
