def simulationAWSSample(connection, deviceName, frequency, timeInterval, minRange, maxRange):
    # from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
    from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
    from pathlib import Path
    import logging
    import time
    import argparse
    import json
    import random
    import os

    AllowedActions = ['both', 'publish', 'subscribe']

    # Custom MQTT message callback
    # deviceName = "awsDevice"
    # frequency = 1
    # timeInterval = 5
    # minRange = 10
    # maxRange = 100

    def customCallback(client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

    parser = argparse.ArgumentParser()

    host = connection["endpoint"]
    rootCAPath = Path("static/certificates/" + deviceName + "/root-CA.crt")
    certificatePath = Path("static/certificates/" +
                           deviceName + "/" + deviceName + ".cert.pem")
    privateKeyPath = Path(
        "static/certificates/" + deviceName + "/" + deviceName + ".private.key")

    print(os.getcwd())
    port = None
    useWebsocket = False
    clientId = "simulator"
    topic = connection["topic"]
    mode = 'publish'

    if mode not in AllowedActions:
        parser.error("Unknown --mode option %s. Must be one of %s" %
                     (mode, str(AllowedActions)))
        exit(2)

    if useWebsocket and certificatePath and privateKeyPath:
        parser.error(
            "X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
        exit(2)

    if not useWebsocket and (not certificatePath or not privateKeyPath):
        parser.error("Missing credentials for authentication.")
        exit(2)

    # Port defaults
    if useWebsocket and not port:  # When no port override for WebSocket, default to 443
        port = 443
    if not useWebsocket and not port:  # When no port override for non-WebSocket, default to 8883
        port = 8883

    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    print("Coming here ..................................................................0")
    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None
    if useWebsocket:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath)
    else:

        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(
            rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
# Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

  # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    if mode == 'both' or mode == 'subscribe':
        myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
    time.sleep(2)

    # Publish to the same topic in a loop forever

    def valueGen():
        a = random.randint(minRange, maxRange)
        return a

    loopCount = 0

    while loopCount < frequency:
        if mode == 'both' or mode == 'publish':

            message = {}
            value = valueGen()
            message['value'] = value
            messageJson = json.dumps(message)

            myAWSIoTMQTTClient.publish(topic, messageJson, 1)

            if mode == 'publish':
                print('Published topic %s: %s\n' % (topic, messageJson))
            loopCount += 1
        time.sleep(timeInterval)


# simulationAWSSample("con", "awsDevice", 5, 10, 5, 15)
