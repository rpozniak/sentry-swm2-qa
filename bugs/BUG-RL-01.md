# BUG-RL-01 — relay pulse 99 запускає імпульс замість E603

**Severity:** Major. **Priority:** High.

**Середовище:** ESP32-S3 N16R8, UART 115200 8N1, macOS; тестовий профіль із доступом user.

| Версія | Результат |
|---|---|
| 2.1.0 | Відтворюється |
| 2.3.0 | Відтворюється для варіантів: 99. |

**Передумови:** Wi-Fi та сесія активні, NORMAL; relay off, auto off, без pulse/schedule; пауза від останнього перемикання щонайменше 1 с.

**Кроки:**

1. Виконати `relay pulse 99`.
2. Записати відповідь і логічні переходи реле.

**Очікуваний результат:** За RL-3 допустимі 100–10000 мс включно. Значення 99 має відхилятися з E603. [PRD, RL-3](../reference/PRD.md).

**Фактичний результат:** У 2.1.0 та 2.3.0 E603 відсутня: UART фіксує OPEN (pulse), потім CLOSED (pulse end). Команда поза допустимим діапазоном виконується.

```text
TX relay pulse 99
[VALVE] OPEN (pulse)
[VALVE] CLOSED (pulse end)
```

**Відтворюваність:** 2.1.0: 3/3 для 99 мс. Контроль 2.3.0: 3 Fail, 0 Pass для наведених варіантів.

**Докази:**

- [stable-01](../logs/stable-01/TC-RL-04_99.log).
- [stable-recheck-01](../logs/stable-recheck-01/TC-RL-04_99.log).
- [stable-recheck-02](../logs/stable-recheck-02/TC-RL-04_99.log).
- [Контроль 2.3.0](../logs/beta-01/TC-RL-04_99.log).

**Пов’язані кейси:** TC-RL-04.

**Регресія:** не підтверджена; дефект наявний уже у 2.1.0.

[Повтор 2.3.0: beta-recheck-01](../logs/beta-recheck-01/TC-RL-04_99.log).

[Повтор 2.3.0: beta-recheck-02](../logs/beta-recheck-02/TC-RL-04_99.log).
