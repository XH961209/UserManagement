import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from common import EMPLOYEE_USER_TOPIC

while True:
    time.sleep(1)
    try:
        kafka_consumer = KafkaConsumer(
            bootstrap_servers=["kafka_server:9092"],
            group_id="test")
        kafka_consumer.subscribe(topics=[EMPLOYEE_USER_TOPIC])
        break
    except NoBrokersAvailable as e:
        print(e)
