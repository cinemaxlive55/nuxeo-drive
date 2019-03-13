# coding: utf-8
import json
import stat
from enum import Enum
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtNetwork import QHostAddress, QTcpServer, QTcpSocket

from ..engine.engine import Engine
from ..objects import DocPair
from ..utils import force_decode, force_encode

if TYPE_CHECKING:
    from ..manager import Manager  # noqa

log = getLogger(__name__)


class Status(Enum):
    SYNCED = 1
    SYNCING = 2
    CONFLICTED = 3
    ERROR = 4
    LOCKED = 5
    UNSYNCED = 6


class ExtensionListener(QTcpServer):
    """
    Server listening to the OS extensions.

    This TCP server is instantiated during the Manager.__init__(),
    and starts listening once the signal Manager.started() is emitted.

    It handles requests coming from any FinderSync extension or overlay DLL instance.
    These requests are JSON-formatted and follow this pattern:
    {
        "command": "<command>",
        "value": "<value>",  # parameters
        ...
    }
    It will look for the callable associated with the command in its `handlers` dict.
    """

    listening = pyqtSignal()
    explorer_name = ""

    def __init__(self, manager: "Manager", *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.manager = manager
        self.host = "localhost"
        self.port = 10650
        self.handlers: Dict[str, Callable] = {}
        self.newConnection.connect(self._handle_connection)

    def _listen(self):
        """
        Called once the Manager.started() is emitted.

        Starts listening and emits a signal so that the extension can be started.
        """
        self.listen(QHostAddress(self.host), self.port)
        log.info(f"Listening to {self.explorer_name} on {self.host}:{self.port}")
        self.listening.emit()

    def _handle_connection(self) -> None:
        """ Called when an Explorer instance is connecting. """
        con: QTcpSocket = self.nextPendingConnection()

        if not con or not con.waitForConnected():
            log.error(
                f"Unable to open extension handler server socket: {con.errorString()}"
            )
            return

        if con.waitForReadyRead():
            payload = con.readLine()

            try:
                content = self._parse_payload(payload.data())
            except:
                log.info(f"Unable to decode payload: {payload}")
            else:
                response = self._handle_content(content)
                if response:
                    con.write(self._format_response(response))

        con.disconnectFromHost()
        con.waitForDisconnected()
        del con

    def _parse_payload(self, payload: bytes) -> str:
        """ Called on the bytes received through the socket. """
        return force_decode(payload)

    def _format_response(self, response: str) -> bytes:
        """ Called on the string to send through the socket. """
        return force_encode(response)

    def _handle_content(self, content: str) -> Optional[str]:
        """ Called on the parsed payload, runs the handler associated with the command. """
        try:
            data = json.loads(content)
        except Exception:
            log.info(f"Unable to parse JSON: {content}")
            return None

        cmd = data.get("command")
        value = data.get("value")

        handler = self.handlers.get(cmd)
        if not handler:
            log.info(f"No handler for the listener command {cmd}")
            return None

        response = handler(value)
        return json.dumps(response)

    def get_engine(self, path: Path) -> Optional[Engine]:
        for engine in self.manager._engines.values():
            if engine.local_folder in path.parents:
                return engine
        return None


def get_formatted_status(state: DocPair, path: Path) -> Dict[str, str]:
    """ For a given file and its state info, get a JSON-compatible status. """
    status = Status.UNSYNCED

    readonly = (path.stat().st_mode & (stat.S_IWUSR | stat.S_IWGRP)) == 0
    if readonly:
        status = Status.LOCKED
    elif state:
        if state.error_count > 0:
            status = Status.ERROR
        elif state.pair_state == "conflicted":
            status = Status.CONFLICTED
        elif state.local_state == "synchronized":
            status = Status.SYNCED
        elif state.pair_state == "unsynchronized":
            status = Status.UNSYNCED
        elif state.processor != 0:
            status = Status.SYNCING
    return {"value": str(status.value), "path": str(path)}