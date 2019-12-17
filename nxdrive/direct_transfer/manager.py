"""
The Direct Transfer feature.

What: the transfers manager.

For now, transfers are done in sequence as it eases the implementation.
For better performances, one should really use Nuxeo Drive.
"""
from logging import getLogger
from pathlib import Path
from typing import TYPE_CHECKING, Callable

from . import bootstrap

if TYPE_CHECKING:
    from nuxeo.handlers.default import Uploader  # noqa
    from nuxeo.models import Document  # noqa

    from .client.remote_client import Remote  # noqa


log = getLogger(__name__)


class DirectTransferManager:
    """Direct Transfer manager.
    This is the core of the feature, separated from Nuxeo Drive.
    It is used to create a new Direct Transfer, keep track of the progression,
    pause/resume transfers and it is connected to a (beautiful) custom QML component.
    """

    def __init__(
        self,
        db: str,
        engine_uid: str,
        remote: "Remote",
        chunk_callback: Callable[["Uploader"], None] = lambda *_: None,
        done_callback: Callable[[bool, int], None] = lambda *_: None,
        dupe_callback: Callable[[Path, "Document"], None] = lambda *_: None,
    ) -> None:
        """
        *chunk_callback* is triggered when a chunk is successfully transferred.
        *done_callback* is triggered when a transfer was successfully done.
        *dupe_callback* is triggered when a given upload would generate a duplicate on the server.
        """
        self.db = db
        self.engine_uid = engine_uid
        self.remote = remote
        self.chunk_callback = chunk_callback
        self.done_callback = done_callback
        self.dupe_callback = dupe_callback

        self.bus = bootstrap.bootstrap()

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}<uid={self.engine_uid!r}"
            f", started={self.is_started!r}"
            f", sessions={len(self.sessions)}"
            f", session={self.current_session}"
            f", db={self.db!r}"
            ">"
        )
