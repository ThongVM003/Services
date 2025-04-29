from confluent_kafka import Producer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from time import sleep
import os
import time
from rich import print
from rich.console import Console
import cv2
import uuid

try:
    listener = os.environ["LISTENER"]
except KeyError:
    listener = "192.168.103.252:9092"

admin = AdminClient({"bootstrap.servers": listener})
fs = admin.create_topics(
    [
        NewTopic(
            "topic",
            num_partitions=1,
            replication_factor=1,
            config={
                "retention.bytes": "500000",
                "retention.ms": "600000",
                "cleanup.policy": "delete",
                "compression.type": "zstd",
            },
        )
    ]
)

producer_configs = {
    "bootstrap.servers": listener,
    "linger.ms": 100,
    "compression.type": "zstd",
    "acks": "1",
    "batch.size": 200000,
}

producer = Producer(producer_configs)

console = Console()
cap = cv2.VideoCapture(
    "rtsp://admin:Vntt%40123@192.168.1.101/PSIA/Streaming/channels/1?videoCodecType=MPEG4"
)


if __name__ == "__main__":
    with console.status("Start Producer") as status:
        try:
            while True:
                ret, frame = cap.read()
                key = str(uuid.uuid4())
                if ret:
                    key = str(uuid.uuid4())
                    _, buffer = cv2.imencode(".jpg", frame)
                    try:
                        producer.produce("topic", value=buffer.tobytes(), key=key)
                        producer.poll(0)
                    # Catch kafka exception local queue is full
                    except BufferError as e:
                        producer.flush()
                        producer.produce("topic", value=buffer.tobytes(), key=key)
                        producer.poll(0)
        except KeyboardInterrupt:
            pass
    producer.flush()
