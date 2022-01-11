import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

while True:
    try:
        time.sleep(1)
        kafka_producer = KafkaProducer(bootstrap_servers=["kafka_server:9092"])
        break
    except NoBrokersAvailable as e:
        print(e)

