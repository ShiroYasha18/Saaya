from pydub import AudioSegment
from pydub.utils import make_chunks
from confluent_kafka import Producer, Consumer
from testcontainers.kafka import KafkaContainer
import os
import json
import time
import threading
import logging

#  logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

KAFKA_TOPIC = "audio_chunks"
CHUNK_SIZE_MS = 2000  # 2 seconds per chunk
OVERLAP_MS = 500  # 0.5-second overlap


def delivery_report(err, msg):
    if err:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")



class AudioProducer:
    def __init__(self, kafka_broker):
        self.producer = Producer({'bootstrap.servers': kafka_broker})

    def process_and_send(self, file_path):

        logging.info(f"Processing {file_path}...")
        try:
            audio = AudioSegment.from_file(file_path)
            chunks = make_chunks(audio, CHUNK_SIZE_MS - OVERLAP_MS)

            for i, chunk in enumerate(chunks):
                if i > 0:
                    chunk = chunks[i - 1][-OVERLAP_MS:] + chunk  # Add overlap

                chunk_data = {
                    "file_name": os.path.basename(file_path),
                    "chunk_id": i,
                    "audio_data": chunk.raw_data.hex()
                }
                self.producer.produce(KAFKA_TOPIC, key=str(i), value=json.dumps(chunk_data), callback=delivery_report)

            self.producer.flush()  # Ensure all chunks are sent
            logging.info(f"Finished processing {file_path}.")
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")



class AudioConsumer:
    def __init__(self, kafka_broker):
        self.consumer = Consumer({
            'bootstrap.servers': kafka_broker,
            'group.id': 'audio-processing-group',
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([KAFKA_TOPIC])

    def listen(self):

        logging.info("Listening for audio chunks...")
        while True:
            try:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    logging.error(f"Consumer error: {msg.error()}")
                    continue

                chunk_data = json.loads(msg.value().decode('utf-8'))
                logging.info(f"Received chunk {chunk_data['chunk_id']} from {chunk_data['file_name']}")

                # ML Preprocessing step can be added here
            except Exception as e:
                logging.error(f"Error in consumer loop: {e}")
                time.sleep(2)  # Avoid rapid crash loops


if __name__ == "__main__":
    with KafkaContainer() as kafka:
        kafka_broker = kafka.get_bootstrap_server()

        # Start Consumer in a separate thread
        consumer = AudioConsumer(kafka_broker)
        consumer_thread = threading.Thread(target=consumer.listen, daemon=True)
        consumer_thread.start()

        # Start Producer
        producer = AudioProducer(kafka_broker)
        audio_folder = "./audio_folder"
        os.makedirs(audio_folder, exist_ok=True)

        for file in os.listdir(audio_folder):
            if file.endswith(".wav"):
                producer.process_and_send(os.path.join(audio_folder, file))

        # Keep running to process messages
        while True:
            time.sleep(5)
