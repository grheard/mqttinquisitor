import time

class Main():
    def __init__(self):
        self.exit = False

    def start(self):
        while not self.exit:
            time.sleep(0.2)

    def stop(self):
        self.exit = True
