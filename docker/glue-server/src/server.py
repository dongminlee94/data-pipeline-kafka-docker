"""Glue server."""

import datetime
from typing import Any

import rpyc
from rpyc.utils.server import ThreadedServer


class GlueServer(rpyc.Service):
    """Glue server using RPyC Service."""

    def exposed_pipeline(self, data: dict[str, Any]) -> dict[str, Any]:
        """Expose data pipeline."""
        if not isinstance(data, dict):
            raise RuntimeError("The data must be of type 'dict'.")
        print(f"\ndata: {data}\n")

        # Reconstruct data
        data["timestamp"] = str(
            datetime.datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=9),
        )
        data["sepal_sum"] = data["sepal_length"] + data["sepal_width"]
        data["sepal_mean"] = data["sepal_sum"] / 2
        data["petal_sum"] = data["petal_length"] + data["petal_width"]
        data["petal_mean"] = data["petal_sum"] / 2

        if not isinstance(data, dict):
            raise RuntimeError("The data must be of type 'dict'.")
        print(f"data: {data}\n")
        return data


if __name__ == "__main__":
    t = ThreadedServer(GlueServer, port=12345)
    t.start()
