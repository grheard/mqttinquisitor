from datetime import datetime
from mongoengine import connect, Document, DateTimeField, StringField, QuerySetManager, QuerySet

from mqttinquisitor.logger import logger


class Mongo():
    def __init__(self, config=None):
        self.__parse_config(config)

        connect(host=self.__uri)


    def __parse_config(self, config):
        self.__uri = 'mongodb://127.0.0.1:27017/mqttinquisitor'

        if config is None: return

        if 'mongo' in config:
            config = config['mongo']
            if 'uri' in config:
                self.__uri = config['uri']


    def store(self,ts,msgtype,payload,topic=None):
        entry = Message()
        entry.ts = ts
        entry.msgtype = msgtype
        if topic is not None:
            entry.topic = topic
        entry.payload = payload
        entry.save()


    def query(self,ts=None,count=None,gt=False) -> []:
        if ts is None:
            ts = datetime.utcnow()

        if gt:
            results = Message.objects(ts__gt=ts)
        else:
            results = Message.objects(ts__lt=ts)
        if count is not None:
            results = results[:count]
        lst = []
        for doc in results:
            dct = {"ts": f"{doc.ts}", "msgtype": doc.msgtype, "payload": doc.payload}
            if len(doc.topic) != 0:
                dct['topic'] = doc.topic
            lst.append(dct)
        return lst


class Message(Document):
    ts = DateTimeField(primary_key=True,required=True)
    msgtype = StringField(default='')
    topic = StringField(default='')
    payload = StringField(default='')

    meta = {
        'ordering': ['-ts']
    }
