from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from ..domain import events
from ..constants import SessionState, SessionTerminationStatus


@dataclass(unsafe_hash=True)
class TransferItem:
    uid: int
    local_path: str
    is_file: Optional[bool] = field(default=True, hash=False)
    size: Optional[bool] = field(default=0, hash=False)
    transferred: Optional[bool] = field(default=False, hash=False)
    status: Optional[int] = field(default=SessionState.DRAFT, hash=False)
    remote_ref: Optional[str] = field(default="", hash=False)
    remote_path: Optional[str] = field(default="", hash=False)
    batch: Optional[Dict[str, Any]] = field(default_factory=dict, hash=False)

    def transferred_size(self) -> int:
        if self.transferred:
            return self.size
        return 0


class Transfer:
    def __init__(
        self,
        uid: str,
        state: Optional[SessionState] = SessionState.DRAFT,
        priority: Optional[int] = 0,
    ):
        self.uid = uid
        self.state = state
        self.priority = priority
        self._items: Set[TransferItem] = set()
        self.events: List[events.Event] = []

    def __repr__(self) -> str:
        return f"Transfer(uid={self.uid}, priority={self.priority})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Transfer):
            return False
        return other.uid == self.uid

    def __hash__(self) -> int:
        return hash(self.uid)

    def __gt__(self, other) -> bool:
        return self.priority > other.priority or self.uid > other.uid

    @property
    def status(self) -> SessionTerminationStatus:
        if self.state is not SessionState.ENDED:
            return SessionTerminationStatus.NONE
        if all(item.transferred for item in self._items):
            return SessionTerminationStatus.SUCCESS
        return SessionTerminationStatus.FAILURE

    def add(self, item: TransferItem) -> None:
        self._items.add(item)
        self.events.append(events.Added(item.uid))

    def remove(self, item: TransferItem) -> None:
        self._items.remove(item)
        self.events.append(events.Removed(item.uid))


@dataclass(frozen=True)
class TransferItemAction:
    uid: int
    transfer_id: int
    transfer_item_id: int
    action: str


@dataclass(frozen=True)
class TransferItemError:
    uid: int
    transfer_item_id: int
    error_count: int
    error_count_total: int
    last_error: str
