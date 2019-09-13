import time

from mqttinquisitor.runtime import isDebug

class Main():
    def __init__(self):
        self.exit = False

    def start(self):
        if isDebug():
            print("Debugger detected.")

        while not self.exit:
            time.sleep(0.2)

    def stop(self):
        self.exit = True
