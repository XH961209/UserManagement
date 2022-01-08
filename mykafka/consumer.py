from kafka import KafkaConsumer
from common import EMPLOYEE_USER_TOPIC

# TODO:用户管理系统启动后，之前未消费到的消息也该也能消费到，这里需要设置一下consumer的参数
kafka_consumer = KafkaConsumer(
    bootstrap_servers=["localhost:9092"],
    group_id="test")
kafka_consumer.subscribe(topics=[EMPLOYEE_USER_TOPIC])
