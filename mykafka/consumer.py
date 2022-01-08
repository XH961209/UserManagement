from kafka import KafkaConsumer

kafka_consumer = KafkaConsumer(
    bootstrap_servers=["localhost:9092"],
    group_id="test")
kafka_consumer.subscribe(topics=["topic1"])
