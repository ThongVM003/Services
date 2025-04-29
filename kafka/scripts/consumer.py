import time
from confluent_kafka import Consumer, KafkaError, OFFSET_END, TopicPartition
import json
from rich import print
from rich.console import Console
from time import sleep
import msgpack

import cv2
import numpy as np

# Define Kafka consumer configuration
consumer_config = {
    "bootstrap.servers": "180.148.0.215:9092",  # Replace with your Kafka broker(s)z
    "group.id": "my-consumer-group",  # Consumer group ID
    "auto.offset.reset": "latest",  # Start consuming from the beginning of the topic
    "enable.auto.commit": False,  # Do not commit offsets automatically
    "fetch.max.bytes": 10000000,
    "broker.version.fallback": "0.10.2",
}


def deserialize_data(packed_data):
    unpacked_data = msgpack.unpackb(packed_data, raw=False)
    frame_bytes = unpacked_data["frame"]
    metadata = unpacked_data["metadata"]

    return frame_bytes, metadata


# Create a Kafka consumer instance
consumer = Consumer(consumer_config)
# Subscribe to the Kafka topic
topic = "stream.CAM_XE_RA"
consumer.subscribe([topic])  # Replace with your topic name
partition = TopicPartition(topic, 0, OFFSET_END)
consumer.assign([partition])
consumer.seek(partition)
console = Console()
met = True
pack = True
with console.status("Start Consumer") as status:
    try:
        while True:
            start_time = time.time()
            # consumer.seek(partition)
            msg = consumer.poll(1)  # Poll for new messages with a timeout of 1 second
            if msg is None:
                status.update("Waiting...")
                continue

            if msg.error():
                # Handle Kafka errors
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print("Reached end of partition")
                else:
                    print("Error: {}".format(msg.error()))
            else:
                if met:
                    image_bytes = msg.value()
                    if pack:
                        image_bytes, _ = deserialize_data(image_bytes)
                    np_array = np.frombuffer(image_bytes, np.uint8)
                    image = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
                    cv2.imshow("img", image)
                    key = cv2.waitKey(1)
                    if key & 0xFF == ord("q"):
                        break
                    # print(msg.value())
                fps = f"{(1 / (time.time() - start_time)):.2f}"
                status.update(f"Receiving with FPS: {fps}")
                # print(f"Receiving with FPS: {fps}")
                pass
    except KeyboardInterrupt:
        pass

    finally:
        # Close the Kafka consumer gracefully
        # print("Closing Kafka consumer...", end="\r")
        # cv2.destroyAllWindows()
        # print("Kafka consumer closed.")
        status.update("Closing kafka consumer...")
        consumer.close()
        sleep(1)
