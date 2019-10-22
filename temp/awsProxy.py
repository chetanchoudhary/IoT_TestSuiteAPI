def awsProxy():

    import socks
    from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
    import logging
    import time
    import argparse
    import json
    import random
    from pathlib import Path

    AllowedActions = ['both', 'publish', 'subscribe']

    # Custom MQTT message callback

    def customCallback(client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()
    # parser.add_argument("-e", "--endpoint", action="store", required=True,
    #                     dest="host", help="Your AWS IoT custom endpoint")
    # parser.add_argument("-r", "--rootCA", action="store",
    #                     required=True, dest="rootCAPath", help="Root CA file path")
    # parser.add_argument("-c", "--cert", action="store",
    #                     dest="certificatePath", help="Certificate file path")
    # parser.add_argument("-k", "--key", action="store",
    #                     dest="privateKeyPath", help="Private key file path")
    # parser.add_argument("-p", "--port", action="store",
    #                     dest="port", type=int, help="Port number override")
    # parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
    #                     help="Use MQTT over WebSocket")
    # parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
    #                     help="Targeted client id")
    # parser.add_argument("-t", "--topic", action="store", dest="topic",
    #                     default="sdk/test/Python", help="Targeted topic")
    # parser.add_argument("-m", "--mode", action="store", dest="mode", default="both",
    #                     help="Operation modes: %s" % str(AllowedActions))
    # parser.add_argument("-M", "--message", action="store", dest="message", default="Hello World!",
    #                     help="Message to publish")

    args = parser.parse_args()
    host = "a2on3hwushji1e-ats.iot.us-east-2.amazonaws.com"
    rootCAPath = Path("../static/certificates/awsDevice/root-CA.crt")
    certificatePath = Path(
        "../static/certificates/awsDevice/testDevice.cert.pem")
    privateKeyPath = Path(
        "../static/certificates/awsDevice/testDevice.private.key")
    port = 443
    useWebsocket = False
    clientId = "basicPubSub"
    deviceName = "awsDevice"
    frequency = 5
    timeInterval = 10
    minRange = 10
    maxRange = 100
    topic = "simulator/test"
    mode = "publish"
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

    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None
    if useWebsocket:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
        myAWSIoTMQTTClient.configureEndpoint(host, port)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath)
    else:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        proxy_config = {"proxy_addr": "http://127.0.0.1",
                        "proxy_port": 5000, "proxy_type": 3}

    # create anonymous function to handle socket creation

        def socket_factory(): return socks.create_connection((host, port), **proxy_config)

        myAWSIoTMQTTClient.configureSocketFactory(socket_factory)
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

    # AWSIoTMQTTClient socket configuration
    # import pysocks to help us build a socket that supports a proxy configuration

    # set proxy arguments (for SOCKS5 proxy: proxy_type=2, for HTTP proxy: proxy_type=3)

    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    if args.mode == 'both' or args.mode == 'subscribe':
        myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
    time.sleep(2)

    # Publish to the same topic in a loop forever
    # loopCount = 0
    # while True:
    #     if args.mode == 'both' or args.mode == 'publish':
    #         message = {}
    #         message['message'] = args.message
    #         message['sequence'] = loopCount
    #         messageJson = json.dumps(message)
    #         myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    #         if args.mode == 'publish':
    #             print('Published topic %s: %s\n' % (topic, messageJson))
    #         loopCount += 1
    #     time.sleep(1)

    def valueGen():
        a = random.randint(minRange, maxRange)
        return a

    loopCount = 0
    print("Frequency === ", frequency)
    while loopCount < frequency:
        if mode == 'both' or mode == 'publish':
            print("Coming here ...1")
            message = {}
            value = valueGen()
            message['value'] = value
            messageJson = json.dumps(message)
            print("Coming here ...2")
            myAWSIoTMQTTClient.publish(topic, messageJson, 1)
            print("Coming here ...3")
            if mode == 'publish':
                print('Published topic %s: %s\n' % (topic, messageJson))
            loopCount += 1
        time.sleep(timeInterval)


# awsProxy()
