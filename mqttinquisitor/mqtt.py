import time
import ssl
from paho.mqtt import client as pahoMqtt
from mqttinquisitor.logger import logger


class Mqtt():


    def __init__(self, config):
        self.__parse_config(config)

        self.client = pahoMqtt.Client('mqttinquisitor')
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.on_message = self.__on_message
        self.client.on_log = self.__on_log

        self.__callback_on_message = None

        self.__callback_on_status = None


    def __parse_config(self, config):
        self.__host = '127.0.0.1'
        self.__port = 1883
        self.__ca = None
        self.__client_ca = None
        self.__client_key = None
        if 'mqtt' in config:
            if 'host' in config['mqtt']:
                self.__host = config['mqtt']['host']
            if 'port' in config['mqtt']:
                self.__port = config['mqtt']['port']
            if 'tls' in config['mqtt']:
                if 'ca' in config['mqtt']['tls']:
                    self.__ca = config['mqtt']['tls']['ca']
                if 'client_ca' in config['mqtt']['tls']:
                    self.__client_ca = config['mqtt']['tls']['client_ca']
                if 'client_key' in config['mqtt']['tls']:
                    self.__client_key = config['mqtt']['tls']['client_key']


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
        logger.info(f"Connecting to {self.__host} port {self.__port}")
        if not self.__ca is None:
            self.client.tls_set(ca_certs=self.__ca,certfile=self.__client_ca,keyfile=self.__client_key,tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.loop_start()
        self.client.connect_async(self.__host,port=self.__port)


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
