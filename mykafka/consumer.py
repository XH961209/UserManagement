from kafka import KafkaConsumer

kafka_consumer = KafkaConsumer(bootstrap_servers=["localhost:9092"])
kafka_consumer.subscribe(topics=["employee-user"])
