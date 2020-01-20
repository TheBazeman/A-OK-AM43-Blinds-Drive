#!/usr/bin/env python3
# To install libraries needed:
# sudo pip3 install Flask, bluepy, retrying
# Version 1.0 - Bas Bahlmann - The Netherlands

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

    bAllDevicesFound = True
    for AM43BlindsDevice in config['AM43_BLE_Devices']:
        AM43BlindsDeviceMacAddress = config.get('AM43_BLE_Devices', AM43BlindsDevice)  # Read BLE MAC from ini file
        
        bFound = False
        for dev in devices:
            if (AM43BlindsDeviceMacAddress == dev.addr):
                print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Found " + AM43BlindsDeviceMacAddress, flush=True)
                bFound = True
                break
            #else: 
                #bFound = False
        if bFound == False:
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + AM43BlindsDeviceMacAddress + " not found on BTLE network!", flush=True)
            bAllDevicesFound = False
        
    if (bAllDevicesFound == True):
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Every AM43 Blinds Controller is found on BTLE network", flush=True)
        return
    else:
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Not all AM43 Blinds Controllers are found on BTLE network, restarting bluetooth stack and checking again....", flush=True)
        os.system("service bluetooth restart")
        raise ValueError(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Not all AM43 Blinds Controllers are found on BTLE network, restarting bluetooth stack and check again....")


@retry(stop_max_attempt_number=3,wait_fixed=2000)
def ConnectBTLEDevice(AM43BlindsDeviceMacAddress):        
    try:
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Connecting to " + AM43BlindsDeviceMacAddress + "...", flush=True)
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
    # Scan for BTLE devices
    try:
        ScanForBTLEDevices()
    except:
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " ERROR SCANNING FOR ALL BTLE Devices, trying to " + BlindsAction + " the blinds anyway....", flush=True)
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " Please check any open connections to the blinds motor and close them, the Blinds Engine App perhaps?", flush=True)
        pass
        #return "ERROR SCANNING FOR ALL BTLE Devices\n"
    
    for AM43BlindsDevice in config['AM43_BLE_Devices']:
        bSuccess = False
        AM43BlindsDeviceMacAddress = config.get('AM43_BLE_Devices', AM43BlindsDevice)  # Read BLE MAC from ini file
        try:
            dev = ConnectBTLEDevice(AM43BlindsDeviceMacAddress)
        except:
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " ERROR, Cannot connect to " + AM43BlindsDeviceMacAddress, flush=True)
            continue
        
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " --> Connected to " + dev.addr, flush=True)

        BlindsControlService = dev.getServiceByUUID("fe50")
        if (BlindsControlService):
            BlindsControlServiceCharacteristic = BlindsControlService.getCharacteristics("fe51")[0]
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
        # Close connection to BLE device
        dev.disconnect()
        
    if (bSuccess):
        return "OK\n"
    else:
        return "ERROR\n"


if __name__ == "__main__":
    os.system('clear')  # Clear screen
    app.run(host='0.0.0.0') #Listen to all interfaces  #,debug=True
