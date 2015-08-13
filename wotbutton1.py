#!/usr/bin/env python

# From Ship.io. Modified by Charles Hamilton.

###############################
### SHIPIOT ACCOUNT DETAILS ###
###############################
shipiot_username = "<USER_NAME>"
shipiot_token = "<API_TOKEN>"
shipiot_bip_name = "<BIP_NAME>"
###############################

import Adafruit_BBIO.GPIO as gpio  
from time import sleep  
import json, requests, time, sys


def on_press():  
    ##############################
    ###### THE SHIPIOT CALL ######
    ##############################
    ## This is the important part of the integration.
    ## It shows the single HTTP call required to send the event data
    ## to bip.io, which then acts upon it according to the `bip`
    ## that was created. Note that since we are using twitter in our
    ## demo, and twitter has an anti-spam feature, 
    ############################
    r = requests.post(
        "http://%s.api.shipiot.net/bip/http/%s/" % (shipiot_username, shipiot_bip_name),
        auth=(shipiot_username, shipiot_token),
        data=json.dumps(
            {"title": "BBB", "body": "Beaglebone Black Button Pressed!\n" + time.asctime(time.localtime(time.time()))}),
        headers={"Content-Type": "application/json"}
    )
    ############################
    if r.status_code != 200:
        print "ShipIOT Lite connection failed. Please try again"
    else:
        print "event sent!"


# Prepare to read the state of pin 12 on header P8
gpio.setup("P8_12", gpio.IN)

notifyWaiting = True  
oldState = 0  
# Program loop
while True:  
    if notifyWaiting:
        print "Waiting for button press..."
        notifyWaiting = False
    sleep(0.01) # Short delay in the infinite reduces CPU usage
    if gpio.input("P8_12") == 1:
        sys.stdout.write('Pressed button...')
        notifyWaiting = True
        on_press() # Calls ShipIOT Lite, as detailed above
        while gpio.input("P8_12") == 1:
            sleep(0.01)
