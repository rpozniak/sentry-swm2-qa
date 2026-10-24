import json
import os
import re
from pathlib import Path

import pytest

from framework.device_driver import DeviceDriver, DeviceError

ROOT = Path(__file__).parent


def pytest_addoption(parser):
    parser.addoption("--port", help="ESP32 UART port; otherwise detect one CH34x device")
    parser.addoption("--fw", help="Expected firmware version")
    parser.addoption("--run-id", help="Unique log directory, for example stable-01")


@pytest.fixture(scope="session")
def dut(request):
    local = ROOT / "config.local.json"
    settings = json.loads(local.read_text()) if local.exists() else {}
    password = os.environ.get("SENTRY_PASSWORD", settings.get("password", ""))
    if not password:
        pytest.fail("Set the test profile in config.local.json or SENTRY_PASSWORD")
    driver = DeviceDriver(
        request.config.getoption("--port") or settings.get("port"),
        os.environ.get("SENTRY_USER", settings.get("username", "qa_user")),
        password,
    )
    run_id = request.config.getoption("--run-id")
    if not run_id:
        number = 1
        while (ROOT / "logs" / f"auto-{number:03}").exists():
            number += 1
        run_id = f"auto-{number:03}"
    if not re.fullmatch(r"[A-Za-z0-9_-]+", run_id):
        pytest.fail("run-id may contain letters, digits, underscore and hyphen")
    log_dir = ROOT / "logs" / run_id
    log_dir.mkdir(parents=True, exist_ok=False)
    request.config._sentry_run = dict(run_id=run_id, results=[])
    driver.set_log(log_dir / "00_session.log")
    request.config._sentry_driver = driver
    try:
        driver.open()
        driver.get_version()
        request.config._sentry_run.update(version=driver.version, port=driver.port)
        expected = request.config.getoption("--fw")
        if expected and driver.version != expected:
            pytest.fail(f"Expected firmware {expected}; device reports {driver.version}")
        driver.ensure_login()
        driver.ok("state 1")
        if driver.version == "2.3.0":
            guard = driver.command("guard status")
            if not re.search(r"DISARMED", guard, re.I):
                pytest.fail("Disarm Guard before this test suite")
        yield driver
    finally:
        driver.close()


def prepare(device):
    device.ensure_login()
    for command in ("state 1", "distance stop", "relay auto off", "relay schedule off"):
        device.ok(command)
    device.set_relay(False)
    for command in ("lamp timer 0", "lamp off", "health off"):
        device.ok(command)


def cleanup(device):
    device.ensure_login()
    for command in ("state 1", "distance stop", "relay schedule off", "relay auto off"):
        device.ok(command)
    device.set_relay(False)
    for command in ("lamp timer 0", "lamp off", "lamp mode solid", "lamp color white",
                    "lamp brightness 50", "health interval 30", "health on"):
        device.ok(command)


@pytest.fixture
def device(dut, request):
    case = request.node.get_closest_marker("case").args[0]
    variant = request.node.callspec.id if hasattr(request.node, "callspec") else "base"
    run = request.config._sentry_run
    log_path = Path("logs") / run["run_id"] / f"{case}_{variant}.log"
    dut.set_log(ROOT / log_path)
    dut.note(f"CASE {case}; VARIANT {variant}; FW {dut.version}")
    request.node._sentry_result = dict(
        case=case, variant=variant, nodeid=request.node.nodeid,
        version=dut.version, status="Not Run", log=log_path.as_posix(), details="",
    )
    versions = request.node.get_closest_marker("versions")
    if versions and dut.version not in versions.args:
        pytest.skip(f"N/A: firmware {dut.version}; applicable to {versions.args}")
    prepare(dut)
    dut.note("PRECONDITIONS READY")
    try:
        yield dut
    finally:
        dut.note("CLEANUP")
        cleanup(dut)
        dut.note("CLEANUP COMPLETE")


@pytest.fixture
def lamp(device):
    for command in ("lamp mode solid", "lamp brightness 50", "lamp color white", "lamp on"):
        device.ok(command)
    return device


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    result = getattr(item, "_sentry_result", None)
    if result is None:
        return
    driver = item.config._sentry_driver
    if report.failed:
        result["status"] = "Fail" if report.when == "call" else (
            "Fail" if result["status"] == "Fail" else "Blocked"
        )
        result["details"] += driver.clean(str(report.longrepr)) + "\n"
    elif report.skipped:
        reason = str(report.longrepr)
        result["status"] = "N/A" if "N/A:" in reason else "Blocked"
        result["details"] = driver.clean(reason)
    elif report.when == "call":
        result["status"] = "Pass"
    driver.note(f"PYTEST {report.when}: {report.outcome}")
    if report.when == "teardown":
        item.config._sentry_run["results"].append(result.copy())


def pytest_sessionfinish(session, exitstatus):
    run = getattr(session.config, "_sentry_run", None)
    if not run:
        return
    directory = ROOT / "reports" / run["run_id"]
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "results.json").write_text(
        json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    rows = ["# Результати автоматичного прогону", "",
            f"Прогін: {run['run_id']}; FW: {run.get('version', 'unknown')}.", "",
            "| Кейс | Варіант | Результат | Лог |", "|---|---|---|---|"]
    for result in run["results"]:
        rows.append(f"| {result['case']} | {result['variant']} | {result['status']} | "
                    f"[{Path(result['log']).name}](../../{result['log']}) |")
    (directory / "SUMMARY.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
