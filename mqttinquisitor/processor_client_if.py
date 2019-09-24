from abc import ABC


class ProcessorIf(ABC):

    @classmethod
    def register_client(self, client):
        return NotImplemented

    @classmethod
    def unregister_client(self, client):
        return NotImplemented

    @classmethod
    def receive(self, message):
        return NotImplemented


class ClientIf(ABC):

    @classmethod
    def send(self, message):
        return NotImplemented
