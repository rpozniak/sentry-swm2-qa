import codecs
import re
import time
from pathlib import Path

import serial
from serial.tools import list_ports


class DeviceError(Exception):
    pass


class DeviceTimeout(DeviceError):
    pass


class DeviceDriver:
    """UART commands, bounded waits and a sanitized transcript."""

    def __init__(self, port=None, username="qa_user", password=""):
        self.port = port
        self.username = username
        self.password = password
        self.version = None
        self.connection = None
        self.log = None
        self.secrets = set()
        self.secret(password)
        self.decoder = codecs.getincrementaldecoder("utf-8")("replace")
        self.rx = ""
        self.pending_line = ""
        self.events = []
        self.started = time.monotonic()
        self.last_relay = 0

    def secret(self, value):
        if value:
            self.secrets.add(value)
        return value

    def clean(self, text):
        text = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)
        text = text.replace("\r", "")
        text = re.sub(r"(?m)^(login|register)\s+(\S+)\s+\S+", r"\1 \2 ***", text)
        text = re.sub(r"(?m)^passwd\s+\S+\s+\S+", "passwd *** ***", text)
        text = re.sub(r"(?m)^sudo\s+\S+", "sudo ***", text)
        text = re.sub(r"(build tag:\s*)\S+", r"\1***", text)
        for value in sorted(self.secrets, key=len, reverse=True):
            text = text.replace(value, "***")
        return text

    def set_log(self, path):
        self.flush_partial()
        if self.log:
            self.log.close()
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.log = Path(path).open("x", encoding="utf-8")
        self.note(f"PORT {self.port}; FW {self.version or 'detecting'}; UART 115200 8N1")

    def note(self, text, direction="NOTE"):
        if self.log:
            self.log.write(f"[{time.monotonic()-self.started:09.3f}] {direction} {self.clean(text)}\n")
            self.log.flush()

    def open(self):
        if not self.port:
            candidates = [p.device for p in list_ports.comports() if p.vid == 0x1A86]
            if len(candidates) != 1:
                raise DeviceError(f"Specify UART port; detected candidates: {candidates}")
            self.port = candidates[0]
        self.connection = serial.Serial(
            port=None, baudrate=115200, timeout=0.05, write_timeout=2, exclusive=True
        )
        self.connection.dtr = False
        self.connection.rts = False
        self.connection.port = self.port
        self.connection.open()
        self.read_for(0.3)
        if "ESP-ROM:" in self.rx and "ready. state" not in self.rx:
            self.wait_for(r"ready\. state", timeout=10)

    def close(self):
        self.flush_partial()
        if self.connection:
            self.connection.close()
        if self.log:
            self.log.close()
            self.log = None

    def flush_partial(self):
        if self.pending_line:
            self.note(self.pending_line, "RX")
            self.pending_line = ""

    def _read(self):
        data = self.connection.read(self.connection.in_waiting or 1)
        if not data:
            return False
        chunk = self.decoder.decode(data)
        self.rx += chunk
        self.pending_line += chunk
        while "\n" in self.pending_line:
            line, self.pending_line = self.pending_line.split("\n", 1)
            line = self.clean(line)
            self.events.append((time.monotonic(), line))
            self.note(line, "RX")
        return True

    def read_for(self, seconds):
        start = len(self.rx)
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            self._read()
        return self.clean(self.rx[start:])

    def wait_for(self, pattern, timeout=5):
        start = len(self.rx)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            self._read()
            text = self.clean(self.rx[start:])
            if re.search(pattern, text, re.I):
                return text
        raise DeviceTimeout(f"No {pattern!r} within {timeout}s; received: {text}")

    def command(self, command, timeout=3, wait=None):
        if re.match(r"relay (on|off|toggle|pulse|schedule)\b", command):
            self.read_for(max(0, 1.05 - (time.monotonic() - self.last_relay)))
            self.last_relay = time.monotonic()
        self.read_for(0.03)
        start = len(self.rx)
        self.note(command, "TX")
        self.last_tx = time.monotonic()
        self.connection.write((command + "\n").encode("utf-8"))
        self.connection.flush()
        deadline = time.monotonic() + timeout
        last_rx = self.last_tx
        while time.monotonic() < deadline:
            if self._read():
                last_rx = time.monotonic()
            text = self.clean(self.rx[start:])
            if wait:
                if re.search(wait, text, re.I):
                    return text
            elif re.search(r"\bsentry:", text) and time.monotonic() - last_rx >= 0.15:
                return text
        raise DeviceTimeout(f"No complete response to {self.clean(command)!r}: {text}")

    def ok(self, command, **kwargs):
        response = self.command(command, **kwargs)
        if re.search(r"\bE\d{3}\b", response):
            raise DeviceError(f"Preparation command {self.clean(command)!r}: {response}")
        return response

    def get_version(self):
        response = self.command("version")
        match = re.search(r"\bfw v(\d+\.\d+\.\d+)", response)
        if not match:
            raise DeviceError(f"Version format: {response}")
        self.version = match.group(1)
        return self.version

    def try_login(self, password=None):
        password = self.password if password is None else password
        self.secret(password)
        response = self.command(f"login {self.username} {password}")
        who = self.command("whoami")
        success = re.search(rf"user:\s*{re.escape(self.username)},\s*access:\s*user\b", who)
        return bool(success), response + who

    def ensure_login(self):
        who = self.command("whoami")
        if re.search(rf"user:\s*{re.escape(self.username)},\s*access:\s*user\b", who):
            return
        self.command(
            "reconnect", wait=r"(?:\[LINK\] time:|W114|E\d{3})[^\n]*\n", timeout=45
        )
        success, response = self.try_login()
        if not success:
            raise DeviceError(f"Cannot establish the known test session: {response}")

    def reboot(self):
        version = self.version
        self.command("reboot", wait=r"ready\. state[^\n]*\n", timeout=20)
        self.ensure_login()
        if self.get_version() != version:
            raise DeviceError("Firmware version changed during reboot")

    def lamp_status(self):
        response = self.command("lamp status")
        match = re.search(
            r"\[BEACON\]\s*(ON|off), color\s*\((\d+),(\d+),(\d+)\), "
            r"brightness\s*(\d+)%, mode\s*(\w+), timer\s*([^\r\n]+)", response, re.I
        )
        if not match:
            raise DeviceError(f"Lamp status format: {response}")
        state, red, green, blue, brightness, mode, timer = match.groups()
        return dict(on=state.lower() == "on", rgb=tuple(map(int, (red, green, blue))),
                    brightness=int(brightness), mode=mode, timer=timer)

    def relay_status(self):
        response = self.command("relay status")
        match = re.search(r"\[VALVE\]\s*(OPEN|closed|ON|off), auto\s*(on|off), cycles\s*(\d+)", response, re.I)
        if not match:
            raise DeviceError(f"Relay status format: {response}")
        state, auto, cycles = match.groups()
        return dict(on=state.lower() in ("open", "on"), auto=auto.lower() == "on", cycles=int(cycles))

    def set_relay(self, enabled):
        if self.relay_status()["on"] != enabled:
            self.ok("relay on" if enabled else "relay off")

    def health_settings(self):
        response = self.command("health")
        match = re.search(r"auto\s*(on|off), interval\s*(\d+) s", response, re.I)
        if not match:
            raise DeviceError(f"Health settings format: {response}")
        return dict(on=match[1].lower() == "on", interval=int(match[2]))

    def valve_events(self, start):
        events = []
        for _, line in self.events[start:]:
            match = re.search(r"\((\d+)\).*\[VALVE\]\s*(OPEN|closed|ON|off)\s*\(", line, re.I)
            if match:
                events.append((int(match[1]) / 1000, match[2].lower() in ("open", "on")))
        return events

    def restore_password(self, original, candidate):
        self.secret(candidate)
        self.command("logout")
        for password in dict.fromkeys((candidate, original)):
            self.note("RECOVERY: try changed password" if password == candidate else "RECOVERY: try original password")
            success, _ = self.try_login(password)
            if success:
                self.password = password
                if password != original:
                    self.ok(f"passwd {password} {original}")
                self.password = original
                self.command("logout")
                self.ensure_login()
                return
        raise DeviceError("Password recovery failed; stop tests and restore access manually")
