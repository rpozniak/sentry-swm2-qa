import re

import pytest

from framework.device_driver import DeviceError

pytestmark = [pytest.mark.hardware, pytest.mark.alerts]


def records(device):
    response = device.command("alert list")
    found = {}
    for line in response.splitlines():
        match = re.search(r"#(\d+)\s+\S+\s+(INFO|WARNING|CRITICAL)\b", line)
        if match:
            found[int(match[1])] = dict(level=match[2], pending="*" in line, test=bool(re.search(r"\btest\b", line)))
    if not found and not re.search(r"no alerts|empty|0 alerts", response, re.I):
        raise DeviceError(f"Alert list format: {response}")
    return found


def create_alert(device, level="info"):
    response = device.command(f"alert test {level}")
    match = re.search(r"\[CIC #(\d+)\s+", response)
    if not match:
        raise DeviceError(f"Created alert ID missing: {response}")
    return int(match[1])


@pytest.fixture
def alert_device(device):
    device.ok("alert ack all")
    device.ok("alert clear")
    try:
        yield device
    finally:
        device.ok("alert ack all")
        device.ok("alert clear")


@pytest.mark.case("TC-AL-01")
@pytest.mark.versions("2.1.0")
@pytest.mark.parametrize("command", ["alert list", "alert test info", "alert ack 1", "alert clear"],
                         ids=["list", "test", "ack", "clear"])
def test_unavailable_in_stable(device, command):
    response = device.command(command)
    assert "E099" in response and "planned in v2.3.0" in response, response


@pytest.mark.case("TC-AL-02")
@pytest.mark.versions("2.3.0")
@pytest.mark.parametrize("level", ["info", "warning", "critical"])
def test_create_alert(alert_device, level):
    device = alert_device
    identifier = create_alert(device, level)
    record = records(device)[identifier]
    assert record == dict(level=level.upper(), pending=True, test=True)


@pytest.mark.case("TC-AL-03")
@pytest.mark.versions("2.3.0")
def test_ack_selected_id(alert_device):
    device = alert_device
    older = create_alert(device)
    newer = create_alert(device)
    device.command(f"alert ack {older}")
    actual = records(device)
    assert actual[older]["pending"] is False and actual[newer]["pending"] is True, actual


@pytest.mark.case("TC-AL-04")
@pytest.mark.versions("2.3.0")
def test_repeated_ack(acknowledged_alert):
    device, identifier = acknowledged_alert
    assert "W852" in device.command(f"alert ack {identifier}")


@pytest.fixture
def acknowledged_alert(alert_device):
    device = alert_device
    identifier = create_alert(device)
    device.ok("alert ack all")
    if records(device)[identifier]["pending"]:
        raise DeviceError("Cannot prepare an acknowledged alert")
    device.note(f"PRECONDITION: alert #{identifier} acknowledged through ack all")
    return device, identifier


@pytest.mark.case("TC-AL-05")
@pytest.mark.versions("2.3.0")
def test_clear_unacknowledged(alert_device):
    device = alert_device
    identifier = create_alert(device)
    response = device.command("alert clear")
    assert "E855" in response, response
    assert identifier in records(device)


@pytest.mark.case("TC-AL-06")
@pytest.mark.versions("2.3.0")
def test_clear_acknowledged(alert_device):
    device = alert_device
    create_alert(device)
    device.ok("alert ack all")
    device.command("alert clear")
    assert records(device) == {}
