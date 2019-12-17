from typing import Callable, Dict, List, Type
from pathlib import Path

from nuxeo.models import Document

from . import unit_of_work
from ..adapters import notifications
from ..domain import commands, events


class DirectTransferPaused(Exception):
    """A transfer has been paused, the file's processing should stop."""


class DirectTransferDuplicateFoundError(ValueError):
    """
    Exception raised when a duplicate file already exists on the server
    and trying to Direct Transfer a local file with the same name.
    """

    def __init__(self, file: Path, doc: Document) -> None:
        self.file = file
        self.doc = doc

    def __repr__(self) -> str:
        return f"{type(self).__name__}<file={self.file!r}, doc={self.doc!r}>"

    def __str__(self) -> str:
        return (
            f"Document with the name {self.file.name!r} already found on the server: {self.doc}."
            f"Direct Transfer of {self.file!r} postponed after the user decided what to do."
        )


#
# Events
#


def chunk_sent(
    event: events.ChunkSent, notifications: notifications.AbstractNotifications
):
    pass


def send_transfer_error_notification(
    event: events.TransferError, notifications: notifications.AbstractNotifications
):
    pass


def transfer_cancelled(event: events.Cancelled, publish: Callable):
    pass


def transfer_done(event: events.Done, publish: Callable):
    pass


def transfer_paused(event: events.Paused, publish: Callable):
    pass


def transfer_resumed(event: events.Resumed, publish: Callable):
    pass


#
# Commands
#


def cancel(cmd: commands.Cancel, uow: unit_of_work.AbstractUnitOfWork):
    pass


def force_transfer(cmd: commands.Force, uow: unit_of_work.AbstractUnitOfWork):
    pass


def pause_transfer(cmd: commands.Pause, uow: unit_of_work.AbstractUnitOfWork):
    pass


def resume_transfer(cmd: commands.Resume, uow: unit_of_work.AbstractUnitOfWork):
    pass


def transfer(cmd: commands.Transfer, uow: unit_of_work.AbstractUnitOfWork):
    pass


EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.Cancelled: [transfer_cancelled],
    events.Done: [transfer_done],
    events.Paused: [transfer_paused],
    events.Resumed: [transfer_resumed],
    events.TransferError: [send_transfer_error_notification],
}

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.Cancel: cancel,
    commands.Force: force_transfer,
    commands.Pause: pause_transfer,
    commands.Resume: resume_transfer,
    commands.Transfer: transfer,
}
