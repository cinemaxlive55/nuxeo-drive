from nxdrive.direct_transfer.domain.model import TransferItemAction
from nxdrive.direct_transfer.transfer import add_uploads


def test_add_uploads_one_file(tmp_path):
    file = tmp_path / "file.txt"
    file.touch()

    expected = [TransferItemAction("UP", file, "/remote-path")]
    got = list(add_uploads(file, "/remote-path"))
    assert got == expected


def test_add_uploads_recursive(tmp_path):
    file = tmp_path / "file.txt"
    file.touch()
    subfolder = tmp_path / "subfolder"
    subfolder.mkdir()
    subfile = tmp_path / "subfolder" / "file.txt"
    subfile.touch()

    expected = [
        TransferItemAction("UP", tmp_path, "/remote-path"),
        TransferItemAction("UP", file, f"/remote-path/{tmp_path.name}"),
        TransferItemAction("UP", subfolder, f"/remote-path/{tmp_path.name}"),
        TransferItemAction("UP", subfile, f"/remote-path/{tmp_path.name}/subfolder"),
    ]
    got = list(add_uploads(tmp_path, "/remote-path"))
    assert got == expected
