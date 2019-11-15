# AM43-Blinds-Drive
A-OK AM43 Blinds Drive BLE control from a Raspberry Pi

Configure the AM43 Blinds Drive with the app on your phone. Make sure you set the beginning (0%) and endpoint (100%).

This python3 script only provides an Open and Close command. That's what I have debugged on Bluetooth and is enough for me (now). If somebody can provide me with the byte array for other percentages than 0% or 100% I encourage them to deliver it to me.

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

PS: Blind drivers I have bought (Ask for an EU power adapter when you need to):
https://nl.aliexpress.com/item/4000025499519
