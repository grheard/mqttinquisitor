import os

from advancedhttpserver import AdvancedHTTPServer, RequestHandler, WebSocketHandler, build_server_from_argparser
from advancedhttpserver import __version__

from mqttinquisitor.runtime import isDebug
from mqttinquisitor.logger import logger


class WSHandler(WebSocketHandler):
    def on_connected(self):
        print('Connected.')

    def on_closed(self):
        print('Disconnected.')

    def on_message_binary(self, message):
        print('Binary message')
        # self.send_message(self._opcode_binary, message)

    def on_message_text(self, message):
        logger.debug(f"{message}")
        # self.send_message(self._opcode_text, message)


class WebHandler(RequestHandler):
    web_socket_handler = WSHandler


class WebServer():


    def __init__(self, config):
        self.__parse_config(config)

        self.server = AdvancedHTTPServer(WebHandler)
        self.server.serve_files = True
        logger.info(f"Serving from {self.__root}")
        self.server.serve_files_root = self.__root


    def __parse_config(self, config):
        self.__root = 'webapp'
        if 'webserver' in config:
            if 'root' in config['webserver']:
                self.__root = config['webserver']['root']


    def start(self):
        self.server.serve_forever()


    def stop(self):
        self.server.shutdown()
