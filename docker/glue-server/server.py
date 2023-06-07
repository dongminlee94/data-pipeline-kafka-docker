"""Glue server."""

import rpyc
from rpyc.utils.server import ThreadedServer


class GlueServer(rpyc.Service):
    """Glue server using RPyC Service."""

    def exposed_pipeline(self) -> None:
        """Invoke User-defined handler function with message and state."""
        return 42


if __name__ == "__main__":
    t = ThreadedServer(GlueServer, port=12345)
    t.start()
