# Python A-OK AM43 Blinds Motor Control
A-OK AM43 Blinds Drive BTLE control from a Raspberry Pi

Configure the AM43 Blinds Drive with the app on your phone. Make sure you set the beginning (0%) and endpoint (100%).

This python3 script only provides an Open and Close command. That's what I have debugged on Bluetooth and is enough for me (now). If somebody can provide me with the byte array for other percentages than 0% or 100% I encourage them to deliver it to me.

To run BTLE scanning which is done with this script, you need elevated rights. So when it fails, look at that.

I have created a service for it with the following (use the raw view to copy):
sudo tee -a /lib/systemd/system/AOK-AM43.service <<_EOF_
[Unit]
Description = AOK-AM43 Web service
After = network-online.target
Wants = network-online.target

[Service]
User = root
Group = root
Type = simple
ExecStart = /usr/bin/python3 /A-OK_AM43_Blind_Drive/AOK-AM43.py
Restart = on-failure
RestartSec = 30

[Install]
WantedBy = multi-user.target
_EOF_

systemctl enable AOK-AM43.service
systemctl daemon-reload
service AOK-AM43 status


To Do list:
- get the battery level 
- retrieve the percentage of the current postition for the blinds
- Give percentage instead of open/close


The byte string to look for is:

[Service UUID: (0xfe50)]

--->    [Characteristic UUID: (0xfe51)]

--------->  100% close command = 00ff00009a0d0164f2  --> 64 byte/hex = 100

--------->  0% close command   = 00ff00009a0d010096  --> 00 byte/hex = 0

The last byte seems a checksum which I havent figured out yet.

Created a simple python script with a Flask Webservice which you can provide a "Open" (0%) or Close (100%) command so you can give youre Home Automation access to them. BLE seems not too reliable so I had to write some more code for fault handling

HTTP Get commands:

curl -i http://WEB_service_IP_address:5000/AM43BlindsAction/Close
  
curl -i http://WEB_service_IP_address:5000/AM43BlindsAction/Open


Have fun with it :-)
-Bas

PS: Blinds drivers I have bought (Ask for an EU power adapter when you need to):

https://nl.aliexpress.com/item/4000025499519.html

