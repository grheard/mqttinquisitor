import sys

def isDebug() -> bool:
    gettrace = getattr(sys, 'gettrace', None)

    if gettrace is None:
        return False
    elif gettrace():
        return True
    else:
        return None
