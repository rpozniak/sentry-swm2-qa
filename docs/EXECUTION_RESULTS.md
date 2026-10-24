# Результати окремих виконань

Основні прогони: stable-01 і beta-01. Кожен параметр має власний результат та повний очищений UART-лог. N/A означає незастосовність до версії. Окремий ручний прогін 2.3.0: TC-RL-02 і TC-RL-03 — Pass за [підтвердженням виконавця](../logs/manual-2.3.0-01/OPERATOR_REPORT.md). TC-LM-09 і TC-LM-10 на обох версіях та TC-RL-02/03 на 2.1.0 — Not Run. Автоматизовані підсумки залишаються без змін. Журнал їхніх параметрів — у [MANUAL_RUN.md](MANUAL_RUN.md). Для TC-AL-04 наведено контроль beta-recheck-01: перед повторним ack запис підтверджений через ack all.

## TC-LM-01

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | off-on | Pass | [UART](../logs/stable-01/TC-LM-01_off-on.log) |
| 2.1.0 | on-off | Pass | [UART](../logs/stable-01/TC-LM-01_on-off.log) |
| 2.1.0 | off-toggle | Pass | [UART](../logs/stable-01/TC-LM-01_off-toggle.log) |
| 2.1.0 | on-toggle | Pass | [UART](../logs/stable-01/TC-LM-01_on-toggle.log) |
| 2.3.0 | off-on | Pass | [UART](../logs/beta-01/TC-LM-01_off-on.log) |
| 2.3.0 | on-off | Pass | [UART](../logs/beta-01/TC-LM-01_on-off.log) |
| 2.3.0 | off-toggle | Pass | [UART](../logs/beta-01/TC-LM-01_off-toggle.log) |
| 2.3.0 | on-toggle | Pass | [UART](../logs/beta-01/TC-LM-01_on-toggle.log) |

## TC-LM-02

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | on | Pass | [UART](../logs/stable-01/TC-LM-02_on.log) |
| 2.1.0 | off | Pass | [UART](../logs/stable-01/TC-LM-02_off.log) |
| 2.3.0 | on | Pass | [UART](../logs/beta-01/TC-LM-02_on.log) |
| 2.3.0 | off | Pass | [UART](../logs/beta-01/TC-LM-02_off.log) |

## TC-LM-03

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | black | Pass | [UART](../logs/stable-01/TC-LM-03_black.log) |
| 2.1.0 | white | Pass | [UART](../logs/stable-01/TC-LM-03_white.log) |
| 2.1.0 | mixed | Pass | [UART](../logs/stable-01/TC-LM-03_mixed.log) |
| 2.3.0 | black | Pass | [UART](../logs/beta-01/TC-LM-03_black.log) |
| 2.3.0 | white | Pass | [UART](../logs/beta-01/TC-LM-03_white.log) |
| 2.3.0 | mixed | Pass | [UART](../logs/beta-01/TC-LM-03_mixed.log) |

## TC-LM-04

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | red-low | Pass | [UART](../logs/stable-01/TC-LM-04_red-low.log) |
| 2.1.0 | red-high | Pass | [UART](../logs/stable-01/TC-LM-04_red-high.log) |
| 2.1.0 | green-low | Pass | [UART](../logs/stable-01/TC-LM-04_green-low.log) |
| 2.1.0 | green-high | Pass | [UART](../logs/stable-01/TC-LM-04_green-high.log) |
| 2.1.0 | blue-low | Pass | [UART](../logs/stable-01/TC-LM-04_blue-low.log) |
| 2.1.0 | blue-high | Pass | [UART](../logs/stable-01/TC-LM-04_blue-high.log) |
| 2.1.0 | unknown-name | Pass | [UART](../logs/stable-01/TC-LM-04_unknown-name.log) |
| 2.3.0 | red-low | Pass | [UART](../logs/beta-01/TC-LM-04_red-low.log) |
| 2.3.0 | red-high | Pass | [UART](../logs/beta-01/TC-LM-04_red-high.log) |
| 2.3.0 | green-low | Pass | [UART](../logs/beta-01/TC-LM-04_green-low.log) |
| 2.3.0 | green-high | Pass | [UART](../logs/beta-01/TC-LM-04_green-high.log) |
| 2.3.0 | blue-low | Pass | [UART](../logs/beta-01/TC-LM-04_blue-low.log) |
| 2.3.0 | blue-high | Pass | [UART](../logs/beta-01/TC-LM-04_blue-high.log) |
| 2.3.0 | unknown-name | Pass | [UART](../logs/beta-01/TC-LM-04_unknown-name.log) |

## TC-LM-05

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | 0 | Pass | [UART](../logs/stable-01/TC-LM-05_0.log) |
| 2.1.0 | 1 | Pass | [UART](../logs/stable-01/TC-LM-05_1.log) |
| 2.1.0 | 50 | Pass | [UART](../logs/stable-01/TC-LM-05_50.log) |
| 2.1.0 | 100 | Pass | [UART](../logs/stable-01/TC-LM-05_100.log) |
| 2.3.0 | 0 | Pass | [UART](../logs/beta-01/TC-LM-05_0.log) |
| 2.3.0 | 1 | Pass | [UART](../logs/beta-01/TC-LM-05_1.log) |
| 2.3.0 | 50 | Pass | [UART](../logs/beta-01/TC-LM-05_50.log) |
| 2.3.0 | 100 | Pass | [UART](../logs/beta-01/TC-LM-05_100.log) |

## TC-LM-06

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | -1 | Pass | [UART](../logs/stable-01/TC-LM-06_-1.log) |
| 2.1.0 | 101 | Pass | [UART](../logs/stable-01/TC-LM-06_101.log) |
| 2.3.0 | -1 | Pass | [UART](../logs/beta-01/TC-LM-06_-1.log) |
| 2.3.0 | 101 | Pass | [UART](../logs/beta-01/TC-LM-06_101.log) |

## TC-LM-07

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | Pass | [UART](../logs/stable-01/TC-LM-07_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-LM-07_base.log) |

[BUG-LM-01](../bugs/BUG-LM-01.md) — Повідомлення lamp timer вказує мілісекунди замість секунд.

Основний критерій TC-LM-07 — стан лампи під час і після відліку — пройшов. Неправильна одиниця підтвердження є окремою знахідкою з UART-логу.

## TC-LM-08

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | Pass | [UART](../logs/stable-01/TC-LM-08_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-LM-08_base.log) |

## TC-LM-09

Метод Manual; статус Not Run для обох версій.

## TC-LM-10

Метод Manual; статус Not Run для обох версій.

## TC-RL-01

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | off-on | Pass | [UART](../logs/stable-01/TC-RL-01_off-on.log) |
| 2.1.0 | on-off | Pass | [UART](../logs/stable-01/TC-RL-01_on-off.log) |
| 2.1.0 | off-toggle | Pass | [UART](../logs/stable-01/TC-RL-01_off-toggle.log) |
| 2.1.0 | on-toggle | Pass | [UART](../logs/stable-01/TC-RL-01_on-toggle.log) |
| 2.3.0 | off-on | Pass | [UART](../logs/beta-01/TC-RL-01_off-on.log) |
| 2.3.0 | on-off | Pass | [UART](../logs/beta-01/TC-RL-01_on-off.log) |
| 2.3.0 | off-toggle | Pass | [UART](../logs/beta-01/TC-RL-01_off-toggle.log) |
| 2.3.0 | on-toggle | Pass | [UART](../logs/beta-01/TC-RL-01_on-toggle.log) |

## TC-RL-02

Метод Manual. 2.3.0 — **Pass** за [підтвердженням виконавця](../logs/manual-2.3.0-01/OPERATOR_REPORT.md). Параметри — у [журналі](MANUAL_RUN.md#tc-rl-02). 2.1.0 — Not Run.

## TC-RL-03

Метод Manual. 2.3.0 — **Pass** за [підтвердженням виконавця](../logs/manual-2.3.0-01/OPERATOR_REPORT.md). Параметри — у [журналі](MANUAL_RUN.md#tc-rl-03). 2.1.0 — Not Run.

## TC-RL-04

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | -1 | Pass | [UART](../logs/stable-01/TC-RL-04_-1.log) |
| 2.1.0 | 0 | Pass | [UART](../logs/stable-01/TC-RL-04_0.log) |
| 2.1.0 | 99 | Fail | [UART](../logs/stable-01/TC-RL-04_99.log) |
| 2.1.0 | 10001 | Pass | [UART](../logs/stable-01/TC-RL-04_10001.log) |
| 2.3.0 | -1 | Pass | [UART](../logs/beta-01/TC-RL-04_-1.log) |
| 2.3.0 | 0 | Pass | [UART](../logs/beta-01/TC-RL-04_0.log) |
| 2.3.0 | 99 | Fail | [UART](../logs/beta-01/TC-RL-04_99.log) |
| 2.3.0 | 10001 | Pass | [UART](../logs/beta-01/TC-RL-04_10001.log) |

[BUG-RL-01](../bugs/BUG-RL-01.md) — relay pulse 99 запускає імпульс замість E603.

## TC-RL-05

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | 100 | Pass | [UART](../logs/stable-01/TC-RL-05_100.log) |
| 2.1.0 | 1000 | Pass | [UART](../logs/stable-01/TC-RL-05_1000.log) |
| 2.1.0 | 10000 | Pass | [UART](../logs/stable-01/TC-RL-05_10000.log) |
| 2.3.0 | 100 | Pass | [UART](../logs/beta-01/TC-RL-05_100.log) |
| 2.3.0 | 1000 | Pass | [UART](../logs/beta-01/TC-RL-05_1000.log) |
| 2.3.0 | 10000 | Pass | [UART](../logs/beta-01/TC-RL-05_10000.log) |

## TC-RL-06

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | off-on | Fail | [UART](../logs/stable-01/TC-RL-06_off-on.log) |
| 2.1.0 | on-off | Fail | [UART](../logs/stable-01/TC-RL-06_on-off.log) |
| 2.3.0 | off-on | Pass | [UART](../logs/beta-01/TC-RL-06_off-on.log) |
| 2.3.0 | on-off | Pass | [UART](../logs/beta-01/TC-RL-06_on-off.log) |

[BUG-RL-02](../bugs/BUG-RL-02.md) — Одне перемикання реле збільшує cycles на 2.

## TC-RL-07

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | Pass | [UART](../logs/stable-01/TC-RL-07_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-RL-07_base.log) |

## TC-RL-08

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | Pass | [UART](../logs/stable-01/TC-RL-08_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-RL-08_base.log) |

## TC-RL-09

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | on-low | Pass | [UART](../logs/stable-01/TC-RL-09_on-low.log) |
| 2.1.0 | off-low | Pass | [UART](../logs/stable-01/TC-RL-09_off-low.log) |
| 2.1.0 | on-high | Pass | [UART](../logs/stable-01/TC-RL-09_on-high.log) |
| 2.1.0 | off-high | Pass | [UART](../logs/stable-01/TC-RL-09_off-high.log) |
| 2.3.0 | on-low | Pass | [UART](../logs/beta-01/TC-RL-09_on-low.log) |
| 2.3.0 | off-low | Pass | [UART](../logs/beta-01/TC-RL-09_off-low.log) |
| 2.3.0 | on-high | Pass | [UART](../logs/beta-01/TC-RL-09_on-high.log) |
| 2.3.0 | off-high | Pass | [UART](../logs/beta-01/TC-RL-09_off-high.log) |

## TC-HL-01

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | Pass | [UART](../logs/stable-01/TC-HL-01_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-HL-01_base.log) |

## TC-HL-02

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | 10 | Pass | [UART](../logs/stable-01/TC-HL-02_10.log) |
| 2.1.0 | 300 | Fail | [UART](../logs/stable-01/TC-HL-02_300.log) |
| 2.3.0 | 10 | Pass | [UART](../logs/beta-01/TC-HL-02_10.log) |
| 2.3.0 | 300 | Pass | [UART](../logs/beta-01/TC-HL-02_300.log) |

[BUG-HL-01](../bugs/BUG-HL-01.md) — health interval 300 відхиляється на допустимій верхній межі.

## TC-HL-03

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | 9 | Pass | [UART](../logs/stable-01/TC-HL-03_9.log) |
| 2.1.0 | 301 | Pass | [UART](../logs/stable-01/TC-HL-03_301.log) |
| 2.3.0 | 9 | Pass | [UART](../logs/beta-01/TC-HL-03_9.log) |
| 2.3.0 | 301 | Pass | [UART](../logs/beta-01/TC-HL-03_301.log) |

## TC-HL-04

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | Pass | [UART](../logs/stable-01/TC-HL-04_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-HL-04_base.log) |

## TC-HL-05

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | Pass | [UART](../logs/stable-01/TC-HL-05_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-HL-05_base.log) |

## TC-AU-01

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | Pass | [UART](../logs/stable-01/TC-AU-01_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-AU-01_base.log) |

## TC-AU-02

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | same-user | Pass | [UART](../logs/stable-01/TC-AU-02_same-user.log) |
| 2.1.0 | mixed-users | Pass | [UART](../logs/stable-01/TC-AU-02_mixed-users.log) |
| 2.3.0 | same-user | Pass | [UART](../logs/beta-01/TC-AU-02_same-user.log) |
| 2.3.0 | mixed-users | Pass | [UART](../logs/beta-01/TC-AU-02_mixed-users.log) |

## TC-AU-03

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | Pass | [UART](../logs/stable-01/TC-AU-03_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-AU-03_base.log) |

## TC-AU-04

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | 5 | Pass | [UART](../logs/stable-01/TC-AU-04_5.log) |
| 2.1.0 | 33 | Pass | [UART](../logs/stable-01/TC-AU-04_33.log) |
| 2.3.0 | 5 | Pass | [UART](../logs/beta-01/TC-AU-04_5.log) |
| 2.3.0 | 33 | Pass | [UART](../logs/beta-01/TC-AU-04_33.log) |

## TC-AU-05

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | 6 | Fail | [UART](../logs/stable-01/TC-AU-05_6.log) |
| 2.1.0 | 32 | Fail | [UART](../logs/stable-01/TC-AU-05_32.log) |
| 2.3.0 | 6 | Pass | [UART](../logs/beta-01/TC-AU-05_6.log) |
| 2.3.0 | 32 | Pass | [UART](../logs/beta-01/TC-AU-05_32.log) |

[BUG-AU-01](../bugs/BUG-AU-01.md) — Зміна пароля не зберігається після reboot.

## TC-AU-06

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | Pass | [UART](../logs/stable-01/TC-AU-06_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-AU-06_base.log) |

## TC-AL-01

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | list | Pass | [UART](../logs/stable-01/TC-AL-01_list.log) |
| 2.1.0 | test | Pass | [UART](../logs/stable-01/TC-AL-01_test.log) |
| 2.1.0 | ack | Pass | [UART](../logs/stable-01/TC-AL-01_ack.log) |
| 2.1.0 | clear | Pass | [UART](../logs/stable-01/TC-AL-01_clear.log) |
| 2.3.0 | list | N/A | [UART](../logs/beta-01/TC-AL-01_list.log) |
| 2.3.0 | test | N/A | [UART](../logs/beta-01/TC-AL-01_test.log) |
| 2.3.0 | ack | N/A | [UART](../logs/beta-01/TC-AL-01_ack.log) |
| 2.3.0 | clear | N/A | [UART](../logs/beta-01/TC-AL-01_clear.log) |

## TC-AL-02

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | info | N/A | [UART](../logs/stable-01/TC-AL-02_info.log) |
| 2.1.0 | warning | N/A | [UART](../logs/stable-01/TC-AL-02_warning.log) |
| 2.1.0 | critical | N/A | [UART](../logs/stable-01/TC-AL-02_critical.log) |
| 2.3.0 | info | Pass | [UART](../logs/beta-01/TC-AL-02_info.log) |
| 2.3.0 | warning | Pass | [UART](../logs/beta-01/TC-AL-02_warning.log) |
| 2.3.0 | critical | Pass | [UART](../logs/beta-01/TC-AL-02_critical.log) |

## TC-AL-03

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | N/A | [UART](../logs/stable-01/TC-AL-03_base.log) |
| 2.3.0 | base | Fail | [UART](../logs/beta-01/TC-AL-03_base.log) |

[BUG-AL-01](../bugs/BUG-AL-01.md) — alert ack за ID повертає E851 для наявного сповіщення.

## TC-AL-04

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | N/A | [UART](../logs/stable-01/TC-AL-04_base.log) |
| 2.3.0 | base | Fail | [UART](../logs/beta-recheck-01/TC-AL-04_base.log) |

[BUG-AL-01](../bugs/BUG-AL-01.md) — alert ack за ID повертає E851 для наявного сповіщення.

## TC-AL-05

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | N/A | [UART](../logs/stable-01/TC-AL-05_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-AL-05_base.log) |

## TC-AL-06

| Версія | Варіант | Результат | Доказ |
|---|---|---|---|
| 2.1.0 | base | N/A | [UART](../logs/stable-01/TC-AL-06_base.log) |
| 2.3.0 | base | Pass | [UART](../logs/beta-01/TC-AL-06_base.log) |
