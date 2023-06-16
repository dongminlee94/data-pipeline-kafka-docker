"""Glue client."""

import rpyc
from kafka import KafkaConsumer, KafkaProducer


class GlueClient:
    """Glue client using RPyC SocketStream connection."""

    def __init__(self) -> None:
        self.rpyc_client = rpyc.connect(host="localhost", port="12345")
        self.producer = KafkaProducer(bootstrap_servers="localhost:9092")
        self.conumer = KafkaConsumer(
            "iris_data",
            bootstrap_servers="localhost:9092",
            auto_offset_reset="earliest",
        )

    def run(self) -> None:
        """Consumes messages from topic_in and send outputs to topic_out."""
        for message in self.conumer:
            # schema_in = message.value["schema"]["fields"]
            data_in = message.value
            print(f"\ndata_in: {data_in}\n")

            data_out = self.rpyc_client.root.pipeline(data_in)
            print(f"data_out: {data_out}\n")

            response = self.producer.send(topic="new_iris_data", value=data_out).get()
            print(
                f"response.topic: {response.topic}\n"
                f"response.partition: {response.partition}\n"
                f"response.offset: {response.offset}\n",
            )


if __name__ == "__main__":
    glue_client = GlueClient()
    glue_client.run()
