"""
Test the Direct Transfer manager: session lifecycle.
"""
from uuid import uuid4

import pytest
from nxdrive.direct_transfer.constants import SessionState, SessionTerminationStatus
from nxdrive.direct_transfer.manager import DirectTransferManager
from nxdrive.direct_transfer.session import UploadSession, create_session, get_sessions


class FakeRemote:
    """Fake Remote client."""


@pytest.fixture
def manager(tmp_path):
    uid = str(uuid4())
    db = tmp_path / f"{uid}.db"
    remote = FakeRemote()
    yield DirectTransferManager(str(db), uid, remote)


def test_empty_sessions(manager):
    assert not get_sessions()


def test_one_session(manager):
    # Create one upload session
    create_session(is_upload=True)
    sessions = get_sessions()
    assert len(sessions) == 1
    assert isinstance(sessions[0], UploadSession)

    # The manager was init before the new session, so it is empty
    assert not manager.sessions
    assert not manager.current_session

    # Reload session, it should see the new one
    manager.reload()
    assert len(manager.sessions) == 1
    assert isinstance(manager.current_session, UploadSession)


def test_session_lifecycle(manager, tmp_path):
    """Test the session lifecycle."""
    session = create_session(is_upload=True)

    # By default, this is a draft and it has no termination status
    assert session.state is SessionState.DRAFT
    assert session.status is SessionTerminationStatus.NONE

    # Test forcing a state
    session.change_state(SessionState.PENDING)
    assert session.state is SessionState.PENDING
    assert session.status is SessionTerminationStatus.NONE
    # (reset the state for next tests)
    session.change_state(SessionState.DRAFT)
    assert session.state is SessionState.DRAFT

    # The session cannot move forward if there is no transfers
    session.change_state()
    assert session.state is SessionState.DRAFT
    assert session.status is SessionTerminationStatus.NONE

    # Let's add a transfer
    file = tmp_path / "foo.ods"
    file.write_text("bla" * 42)
    session.add(file, "/default-domain/workspaces")
    # And let's say the user decided it is good to go
    session.change_state()
    assert session.state is SessionState.PENDING
    assert session.status is SessionTerminationStatus.NONE
    # (from here, the sessions manager will prioritize the session)

    # Mimic other actions/states

    # The user clicked on the pause button
    session.pause()
    session.change_state()
    assert session.state is SessionState.SUSPENDED
    assert session.status is SessionTerminationStatus.NONE
    session.change_state(SessionState.PENDING)  # Reset

    # The user clicked on the pause button
    session.is_started = True
    session.change_state()
    assert session.state is SessionState.SUSPENDED
    assert session.status is SessionTerminationStatus.NONE
