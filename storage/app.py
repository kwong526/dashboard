from platform import python_branch
from sqlite3 import connect
import requests
import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from base import Base
from price_event import PriceEvent
from buy_event import BuyEvent
import pymysql
import mysql.connector
import yaml, logging, logging.config
import datetime
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
import json
import time

with open("app_conf.yaml", "r") as f:
    app_config = yaml.safe_load(f.read())


with open("log_conf.yaml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger("basicLogger")

logger.info(f'Connecting to DB, Hostname:{app_config["datastore"]["hostname"]}, Port:{app_config["datastore"]["port"]}')

DB_ENGINE = create_engine(
    "mysql+pymysql://{}:{}@{}:{}/{}".format(
        app_config["datastore"]["user"],
        app_config["datastore"]["password"],
        app_config["datastore"]["hostname"],
        app_config["datastore"]["port"],
        app_config["datastore"]["db"],
    )
)

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def get_buy_stock(start_timestamp, end_timestamp):
    """get the  timestamp of the purchase tiem"""
    session = DB_SESSION()
    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(BuyEvent).filter(
        and_(BuyEvent.date_created >= start_timestamp_datetime,
        BuyEvent.date_created < end_timestamp_datetime)
    )

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    
    
    session.close()
    logger.info(
        "Query for purchase item after %s returns %d results"
        % (start_timestamp,len(results_list))
    )

    return results_list, 200

def get_price_check(start_timestamp, end_timestamp):
    """get the  timestamp of the purchase tiem"""
    session = DB_SESSION()
    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(PriceEvent).filter(
        and_(PriceEvent.date_created >= start_timestamp_datetime,
        PriceEvent.date_created < end_timestamp_datetime)
    )

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info(
        "Query for Search Items after %s returns %d results"
        % (start_timestamp, len(results_list))
    )

    return results_list, 200

def process_messages():
    """ Process event messages """

    count = 0
    while count < app_config['log']['max_retry']:
        try:
            server = f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}'
            client = KafkaClient(hosts=server)
            topic = client.topics[str.encode(app_config["events"]["topic"])]


            # Create a consume on a consumer group, that only reads new messages

            # (uncommitted messages) when the service re-starts (i.e., it doesn't
            # read all the old messages from the history in the message queue).
            consumer = topic.get_simple_consumer(consumer_group=b'event_group',reset_offset_on_start=False,auto_offset_reset=OffsetType.LATEST)
        # This is blocking - it will wait for a new message
        
        
            for msg in consumer:
                msg_str = msg.value.decode('utf-8')
                msg = json.loads(msg_str)
                logger.info("Message: %s" % msg)
                payload = msg["payload"]

                if msg["type"] == "purchase": # Change this to your event type
                    # Store the event1 (i.e., the payload) to the DB
                    session = DB_SESSION()
                    bp = BuyEvent(
                        payload["purchase_id"],
                        payload["traceId"],
                        payload["stockTicker"],
                        payload["buyPrice"],
                        payload["buyDate"],
                        payload["sellVolume"],
                    )
                    session.add(bp)
                    session.commit()
                    session.close()
                elif msg["type"] == "search": # Change this to your event type
                    # Store the event2 (i.e., the payload) to the DB
                    session = DB_SESSION()

                    pp = PriceEvent(
                        payload["traceId"],
                        payload["stockTicker"],
                        payload["timespanUnit"],
                        payload["timespanLen"],
                        payload["dateStartMonth"],
                        payload["dateStartDay"],
                        payload["dateSort"],
                    )
                    session.add(pp)
                    session.commit()
                    session.close()
            consumer.commit_offsets()
        except:
            logger.error('connection fail')
            time.sleep(5)
           
            count += 1
            # Commit the new message as being read

    return 200

app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
