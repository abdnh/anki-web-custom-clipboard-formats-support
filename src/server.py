# Adapted from Anki: https://github.com/ankitects/anki/blob/main/qt/aqt/mediasrv.py

from __future__ import annotations

import threading
from http import HTTPStatus
from typing import Any
from urllib.parse import urlparse

import flask
import flask_cors
import requests
from flask import Response
from waitress.server import create_server

app = flask.Flask(__name__, root_path="/fake")
flask_cors.CORS(app)


class CorsServer(threading.Thread):
    _ready = threading.Event()
    daemon = True

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__()
        self.config = config
        self.is_shutdown = False

    def run(self) -> None:
        try:
            desired_host = self.config["host"]
            desired_port = self.config["port"]
            self.server = create_server(
                app,
                host=desired_host,
                port=desired_port,
                clear_untrusted_proxy_headers=True,
            )

            self._ready.set()
            self.server.run()

        except Exception:
            if not self.is_shutdown:
                raise

    def shutdown(self) -> None:
        self.is_shutdown = True
        sockets = list(self.server._map.values())  # type: ignore
        for socket in sockets:
            socket.handle_close()
        # https://github.com/Pylons/webtest/blob/4b8a3ebf984185ff4fefb31b4d0cf82682e1fcf7/webtest/http.py#L93-L104
        self.server.task_dispatcher.shutdown()

    def get_port(self) -> int:
        self._ready.wait()
        return int(self.server.effective_port)  # type: ignore

    def server_url(self) -> str:
        return f'{self.config["host"]}:{self.get_port()}/'


def is_absolute(url: str) -> bool:
    return bool(urlparse(url).netloc)


@app.route("/<path:pathin>", methods=["GET"])
def handle_request(pathin: str) -> Response:
    if not is_absolute(pathin):
        return flask.make_response(
            "URL should be absolute",
            HTTPStatus.BAD_REQUEST,
        )
    res = requests.get(
        pathin,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        },
        timeout=30,
    )
    response = flask.make_response(res.content)
    response.headers["Content-Type"] = res.headers["Content-Type"]

    return response
