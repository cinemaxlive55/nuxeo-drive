from dataclasses import dataclass


class Command:
    pass


@dataclass
class Cancel(Command):
    uid: int


@dataclass
class Force(Command):
    uid: int


@dataclass
class Pause(Command):
    uid: int


@dataclass
class Resume(Command):
    uid: int


@dataclass
class Transfer(Command):
    uid: int
