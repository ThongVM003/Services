from confluent_kafka import Producer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from time import sleep
import os
import time
from rich import print
from rich.console import Console


try:
    listener = os.environ["LISTENER"]
except KeyError:
    listener = "100.93.170.37:9092"

producer_configs = {
    "bootstrap.servers": listener,
    "api.version.request": False,
    "broker.version.fallback": "0.10.2",
}

producer = Producer(producer_configs)

console = Console()


if __name__ == "__main__":
    with console.status("Start Producer") as status:
        try:
            while True:
                start_time = time.time()
                producer.produce("test", "1")
                producer.poll(0)
                sleep(0.1)
                fps = f"{(1 / (time.time() - start_time)):.2f}"
                # status.update(f"Sending with FPS: {fps}")
                print(f"Sending with FPS: {fps}")
        except KeyboardInterrupt:
            pass
    producer.flush()
