import re

import pytest

pytestmark = [pytest.mark.hardware, pytest.mark.health]


@pytest.mark.case("TC-HL-01")
@pytest.mark.smoke
def test_health_report(device):
    response = device.command("health now")
    report = re.search(r"\[TELEMETRY #\d+\][^\n]+", response)
    assert report is not None, response
    text = report[0]
    assert re.search(r"\] \S+ up \d+:\d+:\d+", text), text
    for field in ("heap", "rssi", "temp", "depth", "hull", "batt", "valve", "sonar", "state"):
        assert re.search(rf"\b{field}\s+\S+", text), text
    if device.version == "2.3.0":
        assert re.search(r"\bwatch\s+\S+.*\balerts\s+\d+", text), text


@pytest.mark.case("TC-HL-02")
@pytest.mark.parametrize("interval", [10, 300])
def test_interval(device, interval):
    device.command(f"health interval {interval}")
    assert device.health_settings()["interval"] == interval


@pytest.mark.case("TC-HL-03")
@pytest.mark.parametrize("interval", [9, 301])
def test_invalid_interval(device, interval):
    device.ok("health interval 30")
    assert "E902" in device.command(f"health interval {interval}")


@pytest.mark.case("TC-HL-04")
@pytest.mark.slow
def test_disable_periodic_reports(device):
    device.ok("health interval 10")
    device.ok("health on")
    device.wait_for(r"\[TELEMETRY #\d+\][^\n]*\n", timeout=13)
    device.ok("health off")
    observed = device.read_for(22)
    assert not re.search(r"\[TELEMETRY #\d+\]", observed), observed


@pytest.mark.case("TC-HL-05")
@pytest.mark.slow
def test_interval_survives_reboot(device):
    device.ok("health interval 10")
    device.reboot()
    assert device.health_settings()["interval"] == 10
