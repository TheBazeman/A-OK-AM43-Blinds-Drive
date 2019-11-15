#!/usr/bin/env python3
#pip3 install Flask, bluepy, retrying
# Version 0.1 - Bas Bahlmann

#curl -i http://localhost:5000/AM43BlindsAction/Close
#curl -i http://localhost:5000/AM43BlindsAction/Open

from bluepy import btle
import configparser
import os
from flask import Flask
import datetime
from retrying import retry

#Variables
config = configparser.ConfigParser() #Read ini file for meters
config.read('//A-OK_AM43_Blind_Drive//AOK-AM43.ini')
app = Flask(__name__)


@retry(stop_max_attempt_number=2,wait_fixed=2000)
def ScanForBTLEDevices():
    scanner = btle.Scanner()
    print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Scanning for bluetooth devices....", flush=True)
    devices = scanner.scan()

    bFound = False
    for AM43BlindsDevice in config['AM43_BLE_Devices']:
        AM43BlindsDeviceMacAddress = config.get('AM43_BLE_Devices', AM43BlindsDevice)  # Read BLE MAC from ini file
   
        for dev in devices:
            if (AM43BlindsDeviceMacAddress == dev.addr):
                print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Found " + AM43BlindsDeviceMacAddress + "!", flush=True)
                bFound = True
                break
            else: 
                bFound = False
    if (bFound == True):
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Every AM43 Blinds Controller is found on BTLE network", flush=True)
        return
    else:
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Not all AM43 Blinds Controllers are found on BTLE network, restarting bluetooth stack and checking again....", flush=True)
        os.system("service bluetooth restart")
        raise ValueError(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Not all AM43 Blinds Controllers are found on BTLE network, restarting bluetooth stack and check again....")

    #print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
    #for (adtype, desc, value) in dev.getScanData():
        #print("  %s = %s" % (desc, value))


@retry(stop_max_attempt_number=5,wait_fixed=2000)
def ConnectBTLEDevice(AM43BlindsDeviceMacAddress):        
    try:
        dev = btle.Peripheral(AM43BlindsDeviceMacAddress)
        return dev
    except:
        raise ValueError(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Cannot connect to " + AM43BlindsDeviceMacAddress + " trying again....")

        
@app.route("/")
def hello():
    return "A-OK AM43 BLE Smart Blinds Drive Service\n\n"

    
@app.route("/AM43BlindsAction/<BlindsAction>",methods=['GET'])
def AM43BlindsAction(BlindsAction):
    #Variables#
    OpenBlinds = b"\x00\xff\x00\x00\x9a\x0d\x01\x00\x96"
    CloseBlinds = b"\x00\xff\x00\x00\x9a\x0d\x01\x64\xf2"

    #Code#
    try:
        ScanForBTLEDevices()
    except:
        return "ERROR SCANNINF FOR BTLE Devices\n"
    
    for AM43BlindsDevice in config['AM43_BLE_Devices']:
        bSuccess = False
        AM43BlindsDeviceMacAddress = config.get('AM43_BLE_Devices', AM43BlindsDevice)  # Read BLE MAC from ini file
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Connecting to " + AM43BlindsDeviceMacAddress + "...", flush=True)
        try:
            #dev = btle.Peripheral(AM43BlindsDeviceMacAddress)
            dev = ConnectBTLEDevice(AM43BlindsDeviceMacAddress)
        except:
            return "ERROR, Cannot connect to " + AM43BlindsDeviceMacAddress + "\n"
        
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " --> Connected to " + dev.addr, flush=True)
        #print("Get device service fe50...")
        BlindsControlService = dev.getServiceByUUID("fe50")
        if (BlindsControlService):
            #print("Get device Characteristic fe51...")
            BlindsControlServiceCharacteristic = BlindsControlService.getCharacteristics("fe51")[0]
            #print("Writing to " + str(BlindsControlServiceCharacteristic) + "...")
            if (BlindsAction == "Open"):
                result = BlindsControlServiceCharacteristic.write(OpenBlinds)
            elif (BlindsAction == "Close"):
                result = BlindsControlServiceCharacteristic.write(CloseBlinds)
            else:
                print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Unknown Blindsaction command: " + BlindsAction, flush=True)
                bSuccess = False
                result = None
            
            if (result["rsp"][0] == "wr"):
                print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " --> Writing to " + AM43BlindsDevice + " was succesfull!", flush=True)
                bSuccess = True
            else:
                print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " --> Writing to " + AM43BlindsDevice + " FAILED", flush=True)
                bSuccess = False
    if (bSuccess):
        return "OK\n"
    else:
        return "ERROR\n"


if __name__ == "__main__":
    os.system('clear')  # Clear screen
    app.run(host='0.0.0.0') #Listen to all interfaces  #,debug=True
