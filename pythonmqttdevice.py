# Copyright 2014 Aeris Communications Inc
#
# AerCloud sample code for using the Paho MQTT Library 
#
# Dependencies
#    Paho Library   https://pypi.python.org/pypi/paho-mqtt
#
# To get the sample running, you'll need to fill in the following parameters below
#
#   AerCloud API Key: 
#   AerCloud Account ID: aercloud_account_id
#   AerCloud API Key: aercloud_api_key
#   AerCloud Container: aercloud_container
#
# and you'll also need to create an AerCloud contianer with the following schema:
#
#  Parameter Name      Data Type     Unit           Index
#  LocationTimeStamp	INT	          millisecond	 Yes
#  Latitude	            FLOAT	      second	     Yes
#  Longitude	        FLOAT	      second	     Yes
#  Accuracy	            FLOAT	      meter	         No
#

import paho.mqtt.client as mqtt
import json
import os
import time

aercloud_account_id = "_ADD_YOUR_ACCOUNT_NUMBER_HERE_"
aercloud_api_key = "_ADD_YOUR_API_KEY_HERE_"
aercloud_container = "MyFirstContainer_"

broker = "mqtt.aercloud.aeris.com"
port = 1883
 
client_uniq = "MyFirstDevice"

connect_error = False
publish_complete = False

def log_level_to_str(level):
	if level == mqtt.MQTT_LOG_DEBUG:
		return "DEBUG";
	if level == mqtt.MQTT_LOG_INFO:
		return "INFO"
	elif level == mqtt.MQTT_LOG_NOTICE:
		return "NOTICE"
	elif level == mqtt.MQTT_LOG_WARNING:
		return "WARNING";
	elif level == mqt.MQTT_LOG_ERR:
		return "ERROR"
	else:
		return "UNKNOWN"

def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))

def on_log(client, userdata, level, buf):
	if level == mqtt.MQTT_LOG_WARNING or level == mqtt.MQTT_LOG_ERR:
		print(log_level_to_str(level) + ": '" + str(buf))

def on_publish(client, userdata, mid):
	global publish_complete
	publish_complete = True
	
	print("Published Message for " + str(client) + " with id " + str(mid))
	

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+ mqtt.connack_string(rc))

def on_disconnect(client, userdata, rc):
	global connect_error
	connect_error = True
	
	print("Disconnected. " + mqtt.connack_string(rc))	
	
mqttc = mqtt.Client(client_id=client_uniq, protocol=mqtt.MQTTv31)

mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message
mqttc.on_log = on_log
mqttc.on_publish = on_publish
 
mqttc.username_pw_set(aercloud_account_id, password=aercloud_api_key)

#connect to broker
mqttc.connect(broker, port, 60)
mqttc.loop()

msg = json.dumps({
	"Accuracy": "11",
	"Latitude": "37.61",
	"LocationTimeStamp": "1366361979315",
	"Longitude": "-122.385979"

	})
	
mqttc.publish(aercloud_container, msg, qos=1)
mqttc.loop()

while publish_complete == False and connect_error == False:
	mqttc.loop()
	time.sleep(0.50)

if publish_complete == True:
	print("Published: " + msg)
