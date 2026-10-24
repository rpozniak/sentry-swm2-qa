import re

import pytest

pytestmark = [pytest.mark.hardware, pytest.mark.account]


@pytest.mark.case("TC-AU-01")
@pytest.mark.smoke
def test_login(device):
    device.ok("logout")
    success, response = device.try_login()
    assert success, response


@pytest.mark.case("TC-AU-02")
@pytest.mark.slow
@pytest.mark.parametrize("sequence", ["same-user", "mixed-users"])
def test_lockout(device, sequence):
    device.ok("logout")
    wrong = device.secret("Wrong7x!")
    names = [device.username] * 3 if sequence == "same-user" else ["qa_no1", "qa_no2", device.username]
    try:
        replies = [device.command(f"login {name} {wrong}") for name in names]
        correct_during_lock = device.command(f"login {device.username} {device.password}")
        other_during_lock = device.command(f"login qa_no1 {wrong}")
        assert "E209" in replies[0] and re.search(r"Attempts:\s*1/3", replies[0]), replies[0]
        assert "E209" in replies[1] and re.search(r"Attempts:\s*2/3", replies[1]), replies[1]
        assert "E210" in replies[2], replies[2]
        assert "E207" in correct_during_lock, correct_during_lock
        assert "E207" in other_during_lock, other_during_lock
    finally:
        device.note("Wait beyond the 30-second lockout before restoring the session")
        device.read_for(31)
        device.ensure_login()


@pytest.mark.case("TC-AU-03")
def test_wrong_old_password(device):
    original = device.password
    candidate = device.secret("QaNew7")
    wrong = device.secret("Wrong7x!")
    response = device.command(f"passwd {wrong} {candidate}")
    try:
        assert "E215" in response, response
    finally:
        if "password changed" in response:
            device.restore_password(original, candidate)


@pytest.mark.case("TC-AU-04")
@pytest.mark.parametrize("length", [5, 33])
def test_invalid_new_password(device, length):
    original = device.password
    candidate = device.secret("Q" + "a" * (length - 2) + "7")
    response = device.command(f"passwd {original} {candidate}")
    try:
        assert "E205" in response, response
    finally:
        if "password changed" in response:
            device.restore_password(original, candidate)


@pytest.mark.case("TC-AU-05")
@pytest.mark.slow
@pytest.mark.parametrize("length", [6, 32])
def test_password_survives_reboot(device, length):
    original = device.password
    candidate = device.secret("Q" + "a" * (length - 2) + "7")
    device.note(f"Change original P0 to P{length}; both values are masked")
    response = device.command(f"passwd {original} {candidate}")
    changed = "password changed" in response
    try:
        assert changed, response
        device.password = candidate
        device.note(f"After reboot, login must succeed with the changed P{length}")
        device.reboot()
        assert re.search(rf"user:\s*{re.escape(device.username)},\s*access:\s*user", device.command("whoami"))
    finally:
        if changed:
            device.restore_password(original, candidate)


@pytest.mark.case("TC-AU-06")
def test_logout_removes_access(device):
    device.ok("logout")
    assert "E003" in device.command("lamp on")
