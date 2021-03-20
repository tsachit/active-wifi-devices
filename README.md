# active-wifi-devices

To list all my wifi connected devices on all of my routers. My main router is RaiseComm(Vianet) `Device Model: HT803-N` and Secondary router is Trade-Link `Device Model: T31D`

This is just a personal project. I only made this so I dont' have to keep track of all the mac address connected to my router and see which device is which.

### Enviroment Variables

Run this line to copy and add the mac address and credentials for routers
```
cp env_example.py env.py
```

macDeviceDict format in `env.py` is
```
{
  "ab-12-cd-34-ef-56": "One plus 9 Pro"
}
```

### Preview
![Preview](https://raw.githubusercontent.com/tsachit/active-wifi-devices/main/ScreenShot.png)
