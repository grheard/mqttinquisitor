from datetime import datetime
import json
import threading

from mqttinquisitor.logger import logger
from mqttinquisitor.processor_client_if import ProcessorIf


class Processor(ProcessorIf):
    def __init__(self, mqtt, db):
        self.__clientLock = threading.Lock()
        self.__clients = {}

        self.__mqtt = mqtt
        mqtt.on_message = self.__on_mqtt_message
        mqtt.on_status = self.__on_mqtt_status

        self.__db = db


    def __on_mqtt_status(self, status):
        ts = datetime.utcnow()

        self.__db.store(ts,'status',status)

        self.__send_to_clients(json.JSONEncoder().encode({
            "ts": f"{ts}"
            ,"msgtype": "status"
            ,"payload": status
        }))


    def __on_mqtt_message(self, message):
        try:
            payload = message.payload.decode('utf-8')
        except:
            try:
                h = message.payload.hex()
                payload = ' '.join([h[i:i+2] for i in range(0, len(h), 2)])
            except:
                logger.error(f"Couldn't decode payload for {message.topic}")
                return

        ts = datetime.utcfromtimestamp(message.timestamp)

        self.__db.store(ts,'mqtt',payload,message.topic)

        self.__send_to_clients(json.JSONEncoder().encode({
            "ts": f"{ts}"
            ,"msgtype": "mqtt"
            ,"topic": message.topic
            ,"payload": payload
        }))


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
            if client not in self.__clients:
                logger.error(f"Client '{client}' is not registered")
                return

        # process message
        if 'msgtype' not in message:
            logger.warning(f"'msgtype' field missing in message '{message}'")
            return

        if 'query' in message['msgtype']:
            m = self.__process_query(message)
            if m is not None:
                self.__send_to_client(client,m)


    def __process_query(self, message) -> str:
            if 'ts' not in message:
                ts = None
            else:
                ts = message['ts']

            if 'count' not in message:
                logger.warning(f"'count' field missing in query message '{message}'")
                return None

            results = self.__db.query(ts,message['count'])

            return json.JSONEncoder().encode({
                    "msgtype": "query"
                    ,"results": results
            })


    def __send_to_client(self, client, msg):
        with self.__clientLock:
            if client not in self.__clients:
                logger.error(f"Client '{client}' is not registered")
                return

            client.send(msg)


    def __send_to_clients(self, msg):
        with self.__clientLock:
            for client in self.__clients:
                client.send(msg)
