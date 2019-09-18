import time

from mqttinquisitor.logger import logger
from mqttinquisitor.runtime import isDebug
from mqttinquisitor.mqtt import Mqtt


class Main():
    def __init__(self):
        self.exit = False

        self.mqtt = Mqtt()


    def start(self):
        if isDebug():
            logger.info("Debugger detected.")

        self.mqtt.start()

        while not self.exit:
            time.sleep(0.2)


    def stop(self):
        self.mqtt.stop()
        self.exit = True
