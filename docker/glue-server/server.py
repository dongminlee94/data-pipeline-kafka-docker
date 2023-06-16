"""Glue server."""

import rpyc
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer, AvroSerializer
from confluent_kafka.serialization import MessageField, SerializationContext
from rpyc.utils.server import ThreadedServer


class GlueServer(rpyc.Service):
    """Glue server using RPyC Service."""

    def __init__(self) -> None:
        schema_registry_client = SchemaRegistryClient({"url": "http://localhost:8081"})

        # Decoder
        self.decoder = AvroDeserializer(
            schema_registry_client=schema_registry_client,
            schema_str=schema_registry_client.get_latest_version("iris_data-value").schema.schema_str,
        )
        self.decode_ctx = SerializationContext("iris_data", MessageField.VALUE)

        # Encoder
        self.encoder = AvroSerializer(
            schema_registry_client=schema_registry_client,
            schema_str=schema_registry_client.get_latest_version("new_iris_data-value").schema.schema_str,
        )
        self.encode_ctx = SerializationContext("new_iris_data", MessageField.VALUE)

    def exposed_pipeline(self, data_in: bytes) -> bytes:
        """Reconstruct data_in into data_out."""
        if not isinstance(data_in, bytes):
            raise RuntimeError("data_in must be of type 'bytes'.")

        # Deserialize data to Avro binary
        data_in = self.decoder(data=data_in, ctx=self.decode_ctx)
        print(f"\ndata_in: {data_in}\n")

        # Reconstruct data
        data_out = data_in
        print(f"data_out: {data_out}\n")

        # Serialize data to Avro binary
        data_out = self.encoder(obj=data_out, ctx=self.encode_ctx)

        if not isinstance(data_out, bytes):
            raise RuntimeError("data_out must be of type 'bytes'.")
        return data_out


if __name__ == "__main__":
    t = ThreadedServer(GlueServer, port=12345)
    t.start()
