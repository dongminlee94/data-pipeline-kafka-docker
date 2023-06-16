"""Glue client."""

import rpyc
from confluent_kafka import DeserializingConsumer, SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from schema import deserializer_schema, serializer_schema


class GlueClient:
    """Glue client using RPyC SocketStream connection."""

    def __init__(self) -> None:
        self.rpyc_client = rpyc.connect(host="localhost", port="12345")

        schema_registry_client = SchemaRegistryClient({"url": "http://localhost:8081"})

        avro_deserializer = AvroDeserializer(
            schema_registry_client=schema_registry_client,
            schema_str=deserializer_schema,
        )
        self.conumer = DeserializingConsumer(
            {
                "bootstrap.servers": "localhost:9092",
                "group.id": "data-pipeline-kafka",
                "auto.offset.reset": "earliest",
                "value.deserializer": avro_deserializer,
            },
        )
        self.conumer.subscribe(["iris_data"])

        avro_serializer = AvroSerializer(
            schema_registry_client=schema_registry_client,
            schema_str=serializer_schema,
        )
        self.producer = SerializingProducer(
            {
                "bootstrap.servers": "localhost:9092",
                "value.serializer": avro_serializer,
            },
        )

    def run(self) -> None:
        """Consumes messages from topic_in and send outputs to topic_out."""
        while True:
            message = self.conumer.poll(timeout=1.0)

            if message is not None:
                data_in = message.value()
                print(f"\ndata_in: {data_in}\n")

                data_out = self.rpyc_client.root.pipeline(data_in)
                print(f"data_out: {data_out}\n")

                self.producer.produce(topic="new_iris_data", value=data_out)
                self.producer.flush()


if __name__ == "__main__":
    glue_client = GlueClient()
    glue_client.run()
