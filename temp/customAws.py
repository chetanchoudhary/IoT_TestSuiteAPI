# def awsPub():

#     import paho.mqtt.client as paho
#     import os
#     import socket
#     import ssl
#     from time import sleep
#     from random import uniform
#     from pathlib import Path

#     topic = "test/awsDevice"
#     connflag = False

#     def on_connect(client, userdata, flags, rc):
#         global connflag
#         connflag = True
#         print("Connection returned result: " + str(rc))

#     def on_message(client, userdata, msg):
#         print(msg.topic+" "+str(msg.payload))

#     # def on_log(client, userdata, level, buf):
#     #    print(msg.topic+" "+str(msg.payload))
#     print(1)
#     mqttc = paho.Client()
#     mqttc.on_connect = on_connect
#     mqttc.on_message = on_message
#     # mqttc.on_log = on_log

#     awshost = "a2on3hwushji1e-ats.iot.us-east-2.amazonaws.com"
#     awsport = 8883
#     clientId = "basicPubSub"
#     print()
#     print(2)
#     thingName = "awsDevice"
#     caPath = Path("../static/certificates/awsDevice/root-CA.crt")
#     certPath = Path("../static/certificates/awsDevice/testDevice.cert.pem")
#     keyPath = Path("../static/certificates/awsDevice/testDevice.private.key")

#     mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath,
#                   cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
#     print(3)
#     mqttc.connect(awshost, awsport, keepalive=60)
#     print(4)
#     mqttc.loop_start()

#     while 1 == 1:
#         sleep(0.5)
#         if connflag == True:
#             tempreading = uniform(20.0, 25.0)
#             mqttc.publish(topic, tempreading, qos=1)
#             print("msg sent: temperature " + "%.2f" % tempreading)
#         else:
#             print("waiting for connection...")


# awsPub()
from __future__ import print_function


def awsPub():

    from pathlib import Path
    import sys
    import ssl
    import time
    import datetime
    import logging
    import traceback
    import paho.mqtt.client as mqtt

    IoT_protocol_name = "x-amzn-mqtt-ca"
    # <random>.iot.<region>.amazonaws.com
    aws_iot_endpoint = "a2on3hwushji1e-ats.iot.us-east-2.amazonaws.com"
    url = "https://{}".format(aws_iot_endpoint)

    ca = Path("../static/certificates/awsDevice/root-CA.crt")
    cert = Path("../static/certificates/awsDevice/testDevice.cert.pem")
    private = Path("../static/certificates/awsDevice/testDevice.private.key")

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(log_format)
    logger.addHandler(handler)

    print(1)

    def ssl_alpn():
        try:
            # debug print opnessl version
            logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
            ssl_context = ssl.create_default_context()
            ssl_context.set_alpn_protocols([IoT_protocol_name])
            ssl_context.load_verify_locations(cafile=ca)
            ssl_context.load_cert_chain(certfile=cert, keyfile=private)

            return ssl_context
        except Exception as e:
            print("exception ssl_alpn()")
            raise e
    print(2)
    if __name__ == '__main__':
        topic = "test/date"
        try:
            mqttc = mqtt.Client()
            ssl_context = ssl_alpn()
            mqttc.tls_set_context(context=ssl_context)
            logger.info("start connect")
            mqttc.connect(aws_iot_endpoint, port=443)
            logger.info("connect success")
            mqttc.loop_start()
            print(3)
            while True:
                now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                logger.info("try to publish:{}".format(now))
                mqttc.publish(topic, now)
                time.sleep(5)

        except Exception as e:
            logger.error("exception main()")
            logger.error("e obj:{}".format(vars(e)))
            logger.error("message:{}".format(e.message))
            traceback.print_exc(file=sys.stdout)


# awsPub()
