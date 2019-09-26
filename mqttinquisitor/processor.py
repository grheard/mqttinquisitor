import datetime
import json
import threading

from mqttinquisitor.logger import logger
from mqttinquisitor.processor_client_if import ProcessorIf


class Processor(ProcessorIf):
    def __init__(self, mqtt):
        self.__clientLock = threading.Lock()
        self.__clients = {}

        self.__mqtt = mqtt
        mqtt.on_message = self.__on_mqtt_message
        mqtt.on_status = self.__on_mqtt_status


    def __on_mqtt_status(self, status):
        pass


    def __on_mqtt_message(self, message):
        m = {
            "ts": f"{datetime.datetime.utcfromtimestamp(message.timestamp)}"
            ,"topic": message.topic
            ,"payload": message.payload.decode('utf-8')
        }
        with self.__clientLock:
            for client in self.__clients:
                client.send(json.JSONEncoder().encode(m))


    def register_client(self, client):
        with self.__clientLock:
            if client in self.__clients:
                logger.error(f"Client '{client}' is already registered")
            else:
                self.__clients[client] = {}
                logger.info(f"Added '{client}'")


    def unregister_client(self, client):
        with self.__clientLock:
            if client in self.__clients:
                del self.__clients[client]
                logger.info(f"Removed '{client}'")
            else:
                logger.error(f"Client '{client}' is not registered")


    def receive(self, client, message):
        with self.__clientLock:
            if client in self.__clients:
                logger.debug(f"{client} '{message}'")
            else:
                logger.error(f"Client '{client}' is not registered")
