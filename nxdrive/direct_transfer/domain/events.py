from dataclasses import dataclass


class Event:
    pass


@dataclass
class Added(Event):
    uid: int


@dataclass
class Cancelled(Event):
    uid: int


@dataclass
class ChunkSent(Event):
    uid: int


@dataclass
class Done(Event):
    uid: int


@dataclass
class Paused(Event):
    uid: int


@dataclass
class Removed(Event):
    uid: int


@dataclass
class Resumed(Event):
    uid: int


@dataclass
class TransferError(Event):
    uid: int
    error: str
