from datetime import datetime
import threading
from copy import deepcopy

from mqttinquisitor.logger import logger


class ListDb():

    def __init__(self, config=None):
        self.__lock = threading.Lock()
        self.__list = []


    def store(self,ts,msgtype,payload,topic=None):
        with self.__lock:
            entry = {"ts": ts, "msgtype": msgtype, "payload": payload}
            if topic is not None:
                entry['topic'] = topic

            self.__list.append(entry)
            if len(self.__list) > 1000:
                self.__list.pop(0)


    def query(self,ts=None,count=None,gt=False) -> []:
        if ts is None:
            ts = datetime.utcnow()
        elif isinstance(ts,str):
            ts = datetime.fromisoformat(ts)

        lst = []
        with self.__lock:
            for entry in reversed(self.__list):
                _entry = deepcopy(entry)
                _entry['ts'] = f"{_entry['ts']}"
                if gt:
                    if entry['ts'] > ts:
                        lst.append(_entry)
                else:
                    if entry['ts'] < ts:
                        lst.append(_entry)
        if count is not None:
            lst = lst[:count]
        return lst
