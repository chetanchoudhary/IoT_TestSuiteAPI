def simulation(broker, topic, frequency, timeInterval):
    import sys
    import paho.mqtt.client as mqtt
    import time
    import json
    import random

    # Callback from MQTT call
    def on_message(client, userdata, message):
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        print("message qos=", message.qos)
        print("message retain flag=", message.retain)


##############################################################################################################################
# Configurations
    broker = broker
    client = mqtt.Client("simulator")


##############################################################################################################################
# Publishing Data to Cloud


    def tempHumidityChange(test):
        client.on_message = on_message
        print("Connecting to Broker : ", broker)
        client.connect(broker)
        client.loop_start()
        client.publish(topic, test)
        print("published")
        time.sleep(4)
        client.loop_stop()

##############################################################################################################################


# Getting Temperature and Humidity from DHT11 sensor.

    def tempGen():
        a = random.randint(10, 100)
        return a

    def humidityGen():
        a = random.randint(10, 100)
        return a
# Sending data to Thingworx Cloud Continously using MQTT
    i = 0
    while i < frequency:
        humidity = humidityGen()
        temperature = tempGen()
        test = {"temperature": str(temperature), "humidity": str(humidity)}
        testJson = json.dumps(test)
        tempHumidityChange(testJson)
        i = i + 1
        time.sleep(timeInterval)
