"""Glue server."""

from typing import Any

import rpyc
from rpyc.utils.server import ThreadedServer


class GlueServer(rpyc.Service):
    """Glue server using RPyC Service."""

    def exposed_pipeline(self, data_in: dict[str, Any]) -> dict[str, Any]:
        """Reconstruct data_in into data_out."""
        if not isinstance(data_in, dict):
            raise RuntimeError("data_in must be of type 'dict'.")
        print(f"\ndata_in: {data_in}\n")

        # Reconstruct data
        data_out = data_in

        if not isinstance(data_out, dict):
            raise RuntimeError("data_out must be of type 'dict'.")
        print(f"data_out: {data_out}\n")
        return data_out


if __name__ == "__main__":
    t = ThreadedServer(GlueServer, port=12345)
    t.start()
