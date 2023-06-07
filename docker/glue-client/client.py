"""Glue client."""

import rpyc


class GlueClient:
    """Glue client using RPyC SocketStream connection."""

    def __init__(self) -> None:
        self.rpyc_client = rpyc.connect(host="glue-server", port="12345")

    def run(self) -> None:
        """Consumes messages from topic_in and send outputs to topic_out."""
        print(self.rpyc_client.root.pipeline())


if __name__ == "__main__":
    glue_client = GlueClient()
    glue_client.run()
