# WEB SOCKETS
def awsSimulationWS():
    from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
    import logging
    import time
    import argparse
    import json
    import random

    deviceName = "awsDevice"
    frequency = 5
    timeInterval = 10
    minRange = 10
    maxRange = 100
    topic = "sdk/test/Python"
    obtainedSessionToken = "FQoGZXIvYXdzELH//////////wEaDB4pvTJDS5l4fphjniKYAXKoJCbvQSsAwk23qFdIzESPpKcts38dSpTgyoZtsPLZg/aDL3NR1Vj1LXJpL36z8f3Syt/F7gdNIDME6ZdpH1G/xCAWT10YHM5GL6FKkoJLHiFL3vHAmQU5Tqgqfko+gy4PRJ5yijhQcg/FiR4IYcHVAox9Kl/5d0M59RusolYfGiBygprF9HXn914lZO4A962qS7kEs9R/KP7q8OwF"
    # For certificate based connection
    # myMQTTClient = AWSIoTMQTTClient("basicPubSub")
    # For Websocket connection
    myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
    # Configurations
    # For TLS mutual authentication
    # myMQTTClient.configureEndpoint("a2on3hwushji1e-ats.iot.us-east-2.amazonaws.com", 8883)
    # For Websocket
    myMQTTClient.configureEndpoint(
        "a2on3hwushji1e-ats.iot.us-east-2.amazonaws.com", 443)

    myMQTTClient.configureIAMCredentials(
        "ASIA6FC44LEDBU2CLYC7", "/I7X+ieIAv20k0UGxq3hi0CpIdKQw3Sy4kb3+PGC", obtainedSessionToken)
# AWS IoT MQTT Shadow Client
    # For TLS mutual authentication with TLS ALPN extension
    # myMQTTClient.configureEndpoint("a2on3hwushji1e-ats.iot.us-east-2.amazonaws.com", 443)
    # myMQTTClient.configureCredentials("../static/certificates/awsDevice/root-CA.crt","../static/certificates/awsDevice/testDevice.private.key", "../static/certificates/awsDevice/testDevice.cert.pem")
    # For Websocket, we only need to configure the root CA
    myMQTTClient.configureCredentials(
        "../static/certificates/awsDevice/root-CA.crt")
    # Infinite offline Publish queueing
    myMQTTClient.configureOfflinePublishQueueing(-1)
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    myMQTTClient.connect()
    print("done==================================================================")
    # myMQTTClient.publish("sdk/test/Python", "myPayload", 0)
    # #myMQTTClient.subscribe("sdk/test/Python", 1, customCallback)
    # # myMQTTClient.unsubscribe("sdk/test/Python")
    # myMQTTClient.disconnect()

    def valueGen():
        a = random.randint(minRange, maxRange)
        return a

    loopCount = 0
    while loopCount < frequency:

        message = {}
        value = valueGen()
        message['value'] = value
        messageJson = json.dumps(message)
        myMQTTClient.publish(topic, messageJson, 1)
        print('Published topic %s: %s\n' % (topic, messageJson))
        loopCount += 1
        time.sleep(timeInterval)


# awsSimulationWS()

# {'Credentials': {'AccessKeyId': 'ASIA6FC44LEDBU2CLYC7', 'SecretAccessKey': '/I7X+ieIAv20k0UGxq3hi0CpIdKQw3Sy4kb3+PGC', 'SessionToken': 'FQoGZXIvYXdzELH//////////wEaDB4pvTJDS5l4fphjniKYAXKoJCbvQSsAwk23qFdIzESPpKcts38dSpTgyoZtsPLZg/aDL3NR1Vj1LXJpL36z8f3Syt/F7gdNIDME6ZdpH1G/xCAWT10YHM5GL6FKkoJLHiFL3vHAmQU5Tqgqfko+gy4PRJ5yijhQcg/FiR4IYcHVAox9Kl/5d0M59RusolYfGiBygprF9HXn914lZO4A962qS7kEs9R/KP7q8OwF',
#                  'Expiration': datetime.datetime(2019, 10, 8, 7, 21, 38, tzinfo=tzutc())}, 'ResponseMetadata': {'RequestId': '2bcd70c5-e99a-11e9-9017-13874b9cf453', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '2bcd70c5-e99a-11e9-9017-13874b9cf453', 'content-type': 'text/xml', 'content-length': '784', 'date': 'Tue, 08 Oct 2019 07:06:37 GMT'}, 'RetryAttempts': 0}}
