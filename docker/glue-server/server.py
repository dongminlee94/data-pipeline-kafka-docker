"""Glue server."""

import rpyc
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext
from rpyc.utils.server import ThreadedServer


class GlueServer(rpyc.Service):
    """Glue server using RPyC Service."""

    def __init__(self) -> None:
        schema_registry_client = SchemaRegistryClient({"url": "http://localhost:8081"})

        old_schema_str = schema_registry_client.get_latest_version("iris_data-value").schema.schema_str
        self.avro_deserializer = AvroDeserializer(
            schema_registry_client=schema_registry_client,
            schema_str=old_schema_str,
        )
        self.serialization_context = SerializationContext("iris_data", MessageField.VALUE)

    def exposed_pipeline(self, data_in: bytes) -> bytes:
        """Invoke User-defined handler function with message and state."""
        if not isinstance(data_in, bytes):
            raise RuntimeError("data_in must be of type 'bytes'.")

        # Run pipeline
        data_out = self.reconstruct_data(data_in)
        return data_out

    def reconstruct_data(self, data_in: bytes) -> bytes:
        """Reconstruct data_in into data_out."""
        data_out = self.avro_deserializer(data=data_in, ctx=self.serialization_context)
        return data_out


if __name__ == "__main__":
    t = ThreadedServer(GlueServer, port=12345)
    t.start()
