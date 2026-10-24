import time

import pytest

pytestmark = [pytest.mark.hardware, pytest.mark.relay]


@pytest.mark.case("TC-RL-01")
@pytest.mark.smoke
@pytest.mark.parametrize("initial,command,expected", [
    pytest.param(False, "on", True, id="off-on"),
    pytest.param(True, "off", False, id="on-off"),
    pytest.param(False, "toggle", True, id="off-toggle"),
    pytest.param(True, "toggle", False, id="on-toggle"),
])
def test_relay_state(device, initial, command, expected):
    device.set_relay(initial)
    device.command(f"relay {command}")
    assert device.relay_status()["on"] == expected


@pytest.mark.case("TC-RL-04")
@pytest.mark.parametrize("duration", [-1, 0, 99, 10001])
def test_invalid_pulse(device, duration):
    assert "E603" in device.command(f"relay pulse {duration}")


@pytest.mark.case("TC-RL-05")
@pytest.mark.slow
@pytest.mark.parametrize("duration", [100, 1000, 10000])
def test_pulse(device, duration):
    start = len(device.events)
    device.command(f"relay pulse {duration}")
    deadline = device.last_tx + duration / 1000 + 0.5
    device.read_for(max(0, deadline - time.monotonic()))
    assert device.relay_status()["on"] is False
    events = device.valve_events(start)
    opened = next((stamp for stamp, on in events if on), None)
    closed = next((stamp for stamp, on in events if not on and opened is not None and stamp > opened), None)
    if opened is None or closed is None:
        pytest.skip("Blocked: UART does not expose both pulse transitions; instrument required")
    measured = closed - opened
    device.note(f"Logical pulse: {measured:.3f}s; UART timing observation window ±0.050s")
    assert measured == pytest.approx(duration / 1000, abs=0.05)


@pytest.mark.case("TC-RL-06")
@pytest.mark.parametrize("enabled", [True, False], ids=["off-on", "on-off"])
def test_cycle_increment(device, enabled):
    device.set_relay(not enabled)
    initial = device.relay_status()["cycles"]
    device.command("relay on" if enabled else "relay off")
    assert device.relay_status()["cycles"] == initial + 1


@pytest.mark.case("TC-RL-07")
@pytest.mark.slow
def test_cycles_survive_reboot(device):
    initial = device.relay_status()["cycles"]
    device.reboot()
    assert device.relay_status()["cycles"] == initial


@pytest.mark.case("TC-RL-08")
@pytest.mark.slow
def test_schedule(device):
    start = len(device.events)
    device.command("relay schedule 2 2")
    device.read_for(8.5)
    events = device.valve_events(start)
    if len(events) < 5:
        pytest.skip("Blocked: UART does not expose two full schedule cycles")
    events = events[:5]
    assert [on for _, on in events] in ([True, False, True, False, True],
                                       [False, True, False, True, False])
    durations = [second[0] - first[0] for first, second in zip(events, events[1:])]
    device.note(f"Schedule intervals: {durations}; UART observation window ±0.100s")
    assert durations == pytest.approx([2, 2, 2, 2], abs=0.1)


@pytest.mark.case("TC-RL-09")
@pytest.mark.parametrize("on,off", [(1, 2), (2, 1), (3601, 2), (2, 3601)],
                         ids=["on-low", "off-low", "on-high", "off-high"])
def test_invalid_schedule(device, on, off):
    assert "E606" in device.command(f"relay schedule {on} {off}")
