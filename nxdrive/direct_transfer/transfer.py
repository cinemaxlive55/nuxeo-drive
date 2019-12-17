from logging import getLogger
from pathlib import Path
from typing import Generator

from ..utils import get_tree_list
from .domain import model

log = getLogger(__name__)


def add_uploads(
    local_path: Path, remote_path: str
) -> Generator[model.TransferItemAction, None, None]:
    """Recursively plan *local_paths* upload to the given *remote_path*."""
    if local_path.is_file():
        yield model.TransferItemAction("UP", local_path, remote_path)
    elif local_path.is_dir():
        tree = get_tree_list(local_path, remote_path)
        for path, computed_remote_path in sorted(tree):
            yield model.TransferItemAction("UP", path, computed_remote_path)
