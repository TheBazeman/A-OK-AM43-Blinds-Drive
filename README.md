# Python A-OK AM43 Blinds Motor Control
A-OK AM43 Blinds Drive BTLE control from a Raspberry Pi (Zero W)

Configure the AM43 Blinds Drive with the app on your phone. Make sure you set the beginning (0%) and endpoint (100%).

This python3 script provides an <number 0-100>, Open, Close and CheckStatus command. It returns a JSON string with all info.

Install the script and ini file in path "/A-OK_AM43_Blind_Drive/" or change the "inifilepath" parameter in the script and the path in below example service file. Otherwise it cannot find the ini file with your blind mac address(es) and the service wont start.


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


To Do list (time is not my best friend, so be patient please):
- MQTT support


Created a simple python script with a Flask Webservice which you can provide a <number 0-100> (set percentage yourself), "Open" (0%), Close (100%) or CheckStatus command so you can give youre Home Automation access to them. BLE seems not too reliable so I had to write some more code for fault handling.

HTTP Get commands:

curl -i http://localhost:5000/AM43BlindsAction/<Action>  --> For the default setup
  
curl -i http://localhost:5000/AM43BlindsAction/<Action>/<DeviceGroup>  --> For the devicegroup setup you can specify in the ini file
  
"Action" options:

  number 0-100      --> Set blinds to position wanted
  
  Open              --> Opening blinds
  
  Close             --> Closing blinds
  
  CheckStatus       --> Get battery status, current position and light in %


Have fun with it :-)
-Bas

PS: Blinds drivers I have bought (Ask for an EU power adapter when you need to):

https://nl.aliexpress.com/item/4000025499519.html

