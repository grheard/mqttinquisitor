import time
from paho.mqtt import client as pahoMqtt
from mqttinquisitor.logger import logger


class Mqtt():


    def __init__(self):
        self.client = pahoMqtt.Client('mqttinquisitor')
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.on_message = self.__on_message
        self.client.on_log = self.__on_log

        self.__callback_on_message = None

        self.__callback_on_status = None


    def __on_connect(self, client, userdata, flags, rc):
        logger.info(f"{pahoMqtt.connack_string(rc)}")
        if self.__callback_on_status:
            self.__callback_on_status('connect')
        client.subscribe('#',qos=2)


    def __on_disconnect(self, client, userdata, rc):
        if rc:
            logger.error('disconnected')
            if self.__callback_on_status:
                self.__callback_on_status('disconnect')


    def __on_message(self, client, userdata, message):
        # Replace the monotonic receive time with current UTC
        message.timestamp = time.time()
        logger.debug(f"{message.timestamp} :: {message.topic} :: {message.payload.decode('utf-8')}")
        if self.__callback_on_message:
            self.__callback_on_message(message)


    def __on_log(self, client, userdata, level, buf):
        if pahoMqtt.MQTT_LOG_ERR == level:
            logger.error(buf)
        elif pahoMqtt.MQTT_LOG_WARNING == level:
            logger.warning(buf)
        elif pahoMqtt.MQTT_LOG_INFO == level or pahoMqtt.MQTT_LOG_NOTICE == level:
            logger.info(buf)
        elif pahoMqtt.MQTT_LOG_DEBUG == level:
            logger.debug(buf)


    def start(self):
        logger.info('Start')
        self.client.loop_start()
        self.client.connect('192.168.2.50')


    def stop(self):
        logger.info('Stop')
        self.client.loop_stop()
        self.client.disconnect()


    @property
    def on_message(self):
        return self.__callback_on_message

    @on_message.setter
    def on_message(self, func):
        self.__callback_on_message = func


    @property
    def on_status(self):
        return self.__callback_on_status

    @on_status.setter
    def on_status(self, func):
        self.__callback_on_status = func
