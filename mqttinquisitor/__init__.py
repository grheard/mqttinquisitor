import sys
import signal

from mqttinquisitor.main import Main

def __signal_handler(signal, frame):
    try:
        gmain.stop()
    except:
        sys.exit(0)


def init():
    global gmain

    print("Setting up.")

    signal.signal(signal.SIGINT, __signal_handler)

    gmain = Main()

    print("Start.")

    gmain.start()

    print("End.")
