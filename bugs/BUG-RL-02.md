# BUG-RL-02 — Одне перемикання реле збільшує cycles на 2

**Severity:** Major. **Priority:** Medium.

**Середовище:** ESP32-S3 N16R8, UART 115200 8N1, macOS; тестовий профіль із доступом user.

| Версія | Результат |
|---|---|
| 2.1.0 | Відтворюється |
| 2.3.0 | Не відтворено; контрольні варіанти пройшли. |

**Передумови:** Wi-Fi та сесія активні, NORMAL; auto off, без pulse/schedule, сторонніх натискань немає; початковий стан протилежний цільовому.

**Кроки:**

1. Виконати `relay status` і записати C0.
2. Після паузи щонайменше 1 с виконати одне `relay on` або `relay off`.
3. Повторити `relay status` і порівняти cycles із C0.

**Очікуваний результат:** За RL-2 одне фактичне on або off додає одиницю: cycles = C0 + 1. [PRD, RL-2](../reference/PRD.md).

**Фактичний результат:** У 2.1.0 одне перемикання додає 2. У stable-01 для off → ON отримано 48 → 50; для ON → off — 54 → 56. У логах кожного варіанта є лише одне цільове перемикання між вимірюваннями.

```text
[VALVE] closed, auto off, cycles 48
TX relay on
[VALVE] OPEN (command)
[VALVE] OPEN, auto off, cycles 50
```

**Відтворюваність:** 2.1.0: 3/3 для off → ON та 3/3 для ON → off. Контроль 2.3.0: 0 Fail, 2 Pass для наведених варіантів.

**Докази:**

- [stable-01](../logs/stable-01/TC-RL-06_off-on.log).
- [stable-recheck-01](../logs/stable-recheck-01/TC-RL-06_off-on.log).
- [stable-recheck-02](../logs/stable-recheck-02/TC-RL-06_off-on.log).
- [2.1.0, варіант on-off](../logs/stable-01/TC-RL-06_on-off.log).
- [2.3.0, варіант on-off](../logs/beta-01/TC-RL-06_on-off.log).
- [Контроль 2.3.0](../logs/beta-01/TC-RL-06_off-on.log).

**Пов’язані кейси:** TC-RL-06.

**Регресія:** не підтверджена; дефект наявний уже у 2.1.0.
