"""
The Direct Transfer feature.

What: constants.
"""

from enum import Enum


class TransferAction(Enum):
    """Represent a session state."""

    DOWNLOAD = "DOWN"
    UPLOAD = "UP"
    REPLACE_BLOB = "REPLACE"


class SessionState(Enum):
    """Represent a session state."""

    DRAFT = 0
    PENDING = 1
    RUNNING = 2
    SUSPENDED = 3
    ON_HOLD = 4
    ENDED = 5


class SessionTerminationStatus(Enum):
    """Represent a session final status."""

    NONE = 0
    SUCCESS = 1
    FAILURE = 2
    CANCELLED = 3


class TransferStatus(Enum):
    """Represent a single item transfer status."""

    NONE = 0
    ONGOING = 1
    PAUSED = 2
    SUSPENDED = 3
    DONE = 4
    ABORTED = 5
