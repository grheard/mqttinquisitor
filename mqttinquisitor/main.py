import argparse
import json
import os
import sys

from mqttinquisitor.logger import logger, parse_logger_config


def __parse_command_line_arguments() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', nargs=1, default='', help='Configuration json in string or file form')
    args = parser.parse_args()

    if args.config:
        config = __parse_config(args.config[0])
        if config is None:
            print('--config could not be reconciled. See log for details.')
            parser.print_help()
            sys.exit(1)
        return config


def __parse_config(input) -> dict:
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


config = __parse_command_line_arguments()

# Parse the logger configuration ahead of any other import
# in case a module also modifies the logger
parse_logger_config(config)


from mqttinquisitor.mqtt import Mqtt
from mqttinquisitor.webserver import WebServer
from mqttinquisitor.processor import Processor
from mqttinquisitor.db_factory import create_db_interface


class Main():
    def __init__(self):

        self.mqtt = Mqtt(config)

        self.db = create_db_interface(config)

        self.processor = Processor(self.mqtt,self.db)

        self.server = WebServer(config,self.processor)


    def start(self):
        self.mqtt.start()

        # Does not return from start.
        self.server.start()


    def stop(self):
        self.server.stop()
        self.mqtt.stop()
