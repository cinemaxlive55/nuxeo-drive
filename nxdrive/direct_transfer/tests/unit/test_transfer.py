from nxdrive.direct_transfer.domain.model import Transfer, TransferItem


def test_transfer_add_items():
    transfer = Transfer(42)
    item1 = TransferItem(0, "/foo")
    item2 = TransferItem(1, "/foo")
    item1_dupe = TransferItem(0, "/foo")
    transfer.add(item1)
    transfer.add(item1_dupe)
    transfer.add(item2)
    assert transfer._items == {item1, item2}


def test_transfer_remove_items():
    transfer = Transfer(42)
    item1 = TransferItem(0, "/foo")
    item2 = TransferItem(1, "/foo")
    transfer.add(item1)
    transfer.add(item2)
    transfer.remove(item1)
    assert transfer._items == {item2}


def test_transfer_with_same_priorities():
    transfer1 = Transfer(0)
    transfer2 = Transfer(1)
    transfer3 = Transfer(2)
    assert transfer1.priority == transfer2.priority == transfer3.priority
    assert transfer1 < transfer2 < transfer3


def test_transfer_with_different_priorities():
    transfer1 = Transfer(0, priority=1)
    transfer2 = Transfer(1, priority=2)
    transfer3 = Transfer(2, priority=0)
    assert transfer3 < transfer1 < transfer2
