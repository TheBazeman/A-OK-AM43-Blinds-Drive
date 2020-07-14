# Python A-OK AM43 Blinds Motor Control
A-OK AM43 Blinds Drive BTLE control from a Raspberry Pi (Zero W)

Configure the AM43 Blinds Drive with the app on your phone. Make sure you set the beginning (0%) and endpoint (100%).

This python3 script provides an <number 0-100>, Open, Close and CheckStatus command. It returns a JSON string with all info.

Install the script and ini file in path "/A-OK_AM43_Blind_Drive/" or change the "inifilepath" parameter in the script and the path in below example service file. Otherwise it cannot find the ini file with your blind mac address(es) and the service wont start. Run the script with Python3! If you get the following error you are probably running the script with Python 2:<br>
  File "AOK-AM43.py", line 57<br>
    print("ERROR: Cannot find ini file: " + inifilepath + "! Correct the path in this script or put the ini file in the correct directory. Exiting", flush=True)<br>
                                                                                                                                                          ^<br>

How to get the MAC Addresses:<br>
Give the blind controller(s) a proper name in the app on your phone, exit the app and then run “blescan” on your raspberry. The MAC addresses should be visible for all your blind controllers within range.<br>

I have created a service for it with the following:<br>
sudo tee -a /lib/systemd/system/AOK-AM43.service <<_EOF_<br>
[Unit]<br>
Description = AOK-AM43 Web service<br>
After = network-online.target<br>
Wants = network-online.target<br>
<br>
[Service]<br>
User = root<br>
Group = root<br>
Type = simple<br>
ExecStart = /usr/bin/python3 /A-OK_AM43_Blind_Drive/AOK-AM43.py<br>
Restart = on-failure<br>
RestartSec = 30<br>
<br>
[Install]<br>
WantedBy = multi-user.target<br>
_EOF_<br>
<br>
systemctl enable AOK-AM43.service<br>
systemctl daemon-reload<br>
service AOK-AM43 status<br>
<br>

To Do list (time is not my best friend, so be patient please):
- MQTT support


Created a simple python script with a Flask Webservice which you can provide a <number 0-100> (set percentage yourself), "Open" (0%), Close (100%) or CheckStatus command so you can give youre Home Automation access to them. BLE seems not too reliable so I had to write some more code for fault handling.

<br>
HTTP Get commands:<br>
curl -i http://localhost:5000/AM43BlindsAction/"Action"  --> For the default setup<br>  
curl -i http://localhost:5000/AM43BlindsAction/"Action"/"DeviceGroup"  --> For the devicegroup setup you can specify in the ini file<br>
<br>

"Action" options:<br>
  number 0-100      --> Set blinds to position wanted<br>
  Open              --> Opening blinds<br>
  Close             --> Closing blinds<br>
  CheckStatus       --> Get battery status, current position and light in %<br>
<br>

Have fun with it :-)
-Bas

PS: Blinds drivers I have bought (Ask for an EU power adapter when you need to):

https://nl.aliexpress.com/item/4000025499519.html


-Special thanks to Richard Taylor for providing me several pieces of code to get to this-
