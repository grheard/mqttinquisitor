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


    def get_document_instance(self):
        return Message()


    def query(self,ts=None,count=None) -> []:
        if count is None:
            return []
        if ts is None:
            ts = datetime.utcnow()

        results = Message.objects(ts__lt=ts)
        return results[:count]


class Message(Document):
    ts = DateTimeField(primary_key=True,required=True)
    msgtype = StringField(default='')
    topic = StringField(default='')
    payload = StringField(default='')

    meta = {
        'ordering': ['-ts']
    }
