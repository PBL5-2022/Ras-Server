# Run with python 3.9.2
### BaseHub : use same url 'ws://localhost:8000/basehub'
- Join specific group : 
    + send : {"group" : "group_dht11",
            "status": "join"
            }
- Leave specific group : 
    + leave : {"group" : "group_dht11",
            "status": "leave"
            }

- Join bh1750 :
    +send :  {"group" : "group_bh1750",
   "status": "join"
    }
    +leave : 
     {"group" : "group_bh1750",
   "status": "leave"
  }

  group_bh1750 , group_gas,group_door,group_led