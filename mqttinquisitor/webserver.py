import os

from ast import literal_eval

from advancedhttpserver import AdvancedHTTPServer, RequestHandler
from advancedhttpserver import __version__

from mqttinquisitor.logger import logger
from mqttinquisitor.webclient import WebClient


class WebHandler(RequestHandler):
    def on_init(self):
        self.web_socket_handler = WebClient
        self.processor = self.server.processor


class TheServer(AdvancedHTTPServer):
   def __init__(self, processor, *args, **kwargs):
        super(TheServer, self).__init__(*args, **kwargs)

        for server in self.sub_servers:
            server.processor = processor


class WebServer():
    def __init__(self, config, processor):
        self.__parse_config(config)

        self.server = TheServer(processor,handler_klass=WebHandler,address=self.__address)
        self.server.serve_files = True
        logger.info(f"Serving from {self.__root}")
        self.server.serve_files_root = self.__root


    def __parse_config(self, config):
        self.__root = 'webapp'
        self.__address = None
        if 'webserver' in config:
            if 'root' in config['webserver']:
                self.__root = config['webserver']['root']
            if 'address' in config['webserver']:
                try:
                    self.__address = literal_eval(config['webserver']['address'])
                    if not type(self.__address) is tuple:
                        raise TypeError('')
                except:
                    logger.error(f"Invalid address tuple '{config['webserver']['address']}'")
                    self.__address = None


    def start(self):
        self.server.serve_forever()


    def stop(self):
        self.server.shutdown()
