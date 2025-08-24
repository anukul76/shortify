import asyncio
import json
from aiokafka import AIOKafkaConsumer, TopicPartition, AIOKafkaProducer
from aiokafka.structs import OffsetAndMetadata

from app.core.dispatcher import dispatch_event  # your message dispatch logic
from app.core.logging_config import get_logger

logger = get_logger(__name__)

class KafkaManager:
    def __init__(self, topic_group_map: dict, kafka_config: dict):
        self.topic_group_map = topic_group_map
        self.kafka_config = kafka_config
        self.consumers = []
        self.tasks = []
        self.loop = asyncio.get_event_loop()
        self.running = False

        # Producer
        self.producer: AIOKafkaProducer | None = None

    async def _consume_topic(self, topic: str, group_id: str):
        consumer = AIOKafkaConsumer(
            topic,
            loop=self.loop,
            bootstrap_servers=self.kafka_config["bootstrap.servers"],
            group_id=group_id,
            enable_auto_commit=False,  # Manual commit
            auto_offset_reset="earliest"
        )
        await consumer.start()
        self.consumers.append(consumer)
        logger.info(f"Started consuming topic: {topic} with group: {group_id}")

        try:
            async for msg in consumer:
                logger.info(msg.offset)
                try:
                    payload = json.loads(msg.value.decode("utf-8"))
                    logger.info(f"Received from {topic}: {payload}")
                    await dispatch_event(topic, payload, kafka_manager=self)

                    # Manual commit equivalent to .commit(msg)
                    tp = TopicPartition(msg.topic, msg.partition)
                    await consumer.commit({tp: OffsetAndMetadata(msg.offset + 1, "")})
                    logger.info(f"Committed offset {msg.offset + 1} for topic {topic}")

                except Exception as e:
                    logger.error(f"Error processing message from {topic}: {e}")
        except asyncio.CancelledError:
            logger.error(f"Consumer task cancelled for topic: {topic}")
        finally:
            await consumer.stop()
            logger.info(f"Stopped consumer for topic: {topic}")

    async def start_consumers(self):
        if self.running:
            logger.info("Consumers already running.")
            return

        self.running = True
        for topic, group_id in self.topic_group_map.items():
            task = asyncio.create_task(self._consume_topic(topic, group_id))
            self.tasks.append(task)
        logger.info(f"Started {len(self.tasks)} consumer tasks.")

    async def stop_consumers(self):
        logger.info("Stopping Kafka consumers...")
        self.running = False
        for task in self.tasks:
            task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()
        self.consumers.clear()
        logger.info("All Kafka consumers stopped.")

    async def start_producer(self):
        if self.producer:
            logger.info("Producer already running.")
            return

        self.producer = AIOKafkaProducer(
            loop=self.loop,
            bootstrap_servers=self.kafka_config["bootstrap.servers"],
        )
        await self.producer.start()
        logger.info("Kafka producer started.")

    async def stop_producer(self):
        if self.producer:
            await self.producer.stop()
            self.producer = None
            logger.info("Kafka producer stopped.")

    async def send_message(self, topic: str, key: str, value: dict):
        if not self.producer:
            raise RuntimeError("Producer not started. Call start_producer first.")

        try:
            await self.producer.send_and_wait(
                topic,
                json.dumps(value).encode("utf-8"),
                key=key.encode("utf-8") if key else None,
            )
            logger.info(f"Message sent to {topic}: {value}")
        except Exception as e:
            logger.error(f"Failed to send message to {topic}: {e}")

