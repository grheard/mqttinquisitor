import json

from advancedhttpserver import WebSocketHandler

from mqttinquisitor.webserver import logger
from mqttinquisitor.processor_client_if import ClientIf


class WebClient(WebSocketHandler, ClientIf):
    def on_connected(self):
        self.processor = self.handler.processor
        logger.info(f"{self}")
        self.processor.register_client(self)


    def on_closed(self):
        logger.info(f"{self}")
        self.processor.unregister_client(self)


    def on_message_binary(self, message):
        logger.error("Received binary message")


    def on_message_text(self, message):
        logger.debug(f"{message}")
        try:
            jmsg = json.loads(message)
        except json.JSONDecodeError:
            logger.error(f"Invalid message '{message}'")
            return
        self.processor.receive(self, jmsg)


    def send(self, message):
        self.send_message(self._opcode_text, message)
