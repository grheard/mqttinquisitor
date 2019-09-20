import argparse
import json
import os
import sys
import time

from mqttinquisitor.logger import logger
from mqttinquisitor.runtime import isDebug
from mqttinquisitor.mqtt import Mqtt
from mqttinquisitor.webserver import WebServer


class Main():
    def __init__(self):
        self.__config = {}

        self.__parseCommandLineArguments()

        self.mqtt = Mqtt(self.__config)

        self.server = WebServer(self.__config)


    def start(self):
        if isDebug():
            logger.info("Debugger detected.")

        self.mqtt.start()

        # Does not return from start.
        self.server.start()


    def stop(self):
        self.server.stop()
        self.mqtt.stop()


    def __parseCommandLineArguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--config', nargs=1, default='', help='Configuration json in string or file form')
        args = parser.parse_args()

        if args.config:
            config = self.__parseConfig(args.config[0])
            if config is None:
                print('--config could not be reconciled. See log for details.')
                parser.print_help()
                sys.exit(1)
            self.__config = config


    def __parseConfig(self,input):
        try:
            # Try to parse a json object directly
            config = json.loads(input)
            logger.info("configuration successfully parsed from the command line.")
            return config
        except json.JSONDecodeError:
            logger.info(f"'{input}' is not JSON, it will be attempted as a file.")

        # Try loading it as a file
        if not os.path.isfile(input):
            logger.error(f"'{input}' is neither a JSON object or a file.")
            return None

        try:
            file = open(input)
        except OSError:
            logger.error(f"'{input}' cannot be opened.")
            return None

        try:
            config = json.load(file)
            logger.info(f"'{input}' successfully parsed.")
            return config
        except json.JSONDecodeError:
            logger.error(f"'{input}' does not contain a valid JSON object.")
            return None
