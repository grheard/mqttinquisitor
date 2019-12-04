from mqttinquisitor.logger import logger
from mqttinquisitor.mongo import Mongo
from mqttinquisitor.listdb import ListDb


def create_db_interface(config):
    db = None

    if 'mongo' in config:
        logger.info("Creating mongo instance.")
        db = Mongo(config)

    if db is None:
        logger.info("Creating memory instance.")
        db = ListDb()

    return db
