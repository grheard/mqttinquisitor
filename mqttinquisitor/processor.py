from datetime import datetime
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
        m = {
            "ts": f"{datetime.utcnow()}"
            ,"type": "status"
            ,"payload": status
        }

        with self.__clientLock:
            for client in self.__clients:
                client.send(json.JSONEncoder().encode(m))


    def __on_mqtt_message(self, message):
        m = {
            "ts": f"{datetime.utcfromtimestamp(message.timestamp)}"
            ,"type": "mqtt"
            ,"topic": message.topic
        }

        try:
            m['payload'] = message.payload.decode('utf-8')
        except:
            try:
                h = message.payload.hex()
                m['payload'] = ' '.join([h[i:i+2] for i in range(0, len(h), 2)])
            except:
                logger.error(f"Couldn't decode payload for {message.topic}")
                return

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
