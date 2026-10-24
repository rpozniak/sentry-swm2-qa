import time

import pytest

pytestmark = [pytest.mark.hardware, pytest.mark.lamp]


@pytest.mark.case("TC-LM-01")
@pytest.mark.smoke
@pytest.mark.parametrize("initial,command,expected", [
    pytest.param(False, "on", True, id="off-on"),
    pytest.param(True, "off", False, id="on-off"),
    pytest.param(False, "toggle", True, id="off-toggle"),
    pytest.param(True, "toggle", False, id="on-toggle"),
])
def test_lamp_state(device, initial, command, expected):
    device.ok("lamp on" if initial else "lamp off")
    device.command(f"lamp {command}")
    assert device.lamp_status()["on"] == expected


@pytest.mark.case("TC-LM-02")
@pytest.mark.parametrize("state", ["on", "off"])
def test_repeated_state(device, state):
    device.ok(f"lamp {state}")
    assert "W510" in device.command(f"lamp {state}")


@pytest.mark.case("TC-LM-03")
@pytest.mark.parametrize("rgb", [(0, 0, 0), (255, 255, 255), (255, 0, 128)],
                         ids=["black", "white", "mixed"])
def test_rgb(lamp, rgb):
    lamp.command("lamp color " + " ".join(map(str, rgb)))
    assert lamp.lamp_status()["rgb"] == rgb


@pytest.mark.case("TC-LM-04")
@pytest.mark.parametrize("value,code", [
    ("-1 0 0", "E502"), ("256 0 0", "E502"),
    ("0 -1 0", "E502"), ("0 256 0", "E502"),
    ("0 0 -1", "E502"), ("0 0 256", "E502"), ("ultraviolet", "E503"),
], ids=["red-low", "red-high", "green-low", "green-high", "blue-low", "blue-high", "unknown-name"])
def test_invalid_color(device, value, code):
    device.ok("lamp color white")
    assert code in device.command(f"lamp color {value}")


@pytest.mark.case("TC-LM-05")
@pytest.mark.parametrize("brightness", [0, 1, 50, 100])
def test_brightness(lamp, brightness):
    lamp.command(f"lamp brightness {brightness}")
    assert lamp.lamp_status()["brightness"] == brightness


@pytest.mark.case("TC-LM-06")
@pytest.mark.parametrize("brightness", [-1, 101])
def test_invalid_brightness(device, brightness):
    device.ok("lamp brightness 50")
    assert "E504" in device.command(f"lamp brightness {brightness}")


@pytest.mark.case("TC-LM-07")
@pytest.mark.slow
def test_timer_expires(lamp):
    lamp.command("lamp timer 5")
    started = lamp.last_tx
    lamp.read_for(max(0, started + 1 - time.monotonic()))
    during_countdown = lamp.lamp_status()["on"]
    lamp.read_for(max(0, started + 6 - time.monotonic()))
    after_deadline = lamp.lamp_status()["on"]
    assert (during_countdown, after_deadline) == (True, False)


@pytest.mark.case("TC-LM-08")
@pytest.mark.slow
def test_timer_cancelled(lamp):
    lamp.command("lamp timer 5")
    deadline = lamp.last_tx + 6
    lamp.command("lamp timer 0")
    lamp.read_for(max(0, deadline - time.monotonic()))
    assert lamp.lamp_status()["on"] is True
