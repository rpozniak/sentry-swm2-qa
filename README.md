# SENTRY SWM-2 QA

Курсовий проєкт Embedded QA Engineer: приймальні випробування прошивок **2.1.0 stable** та **2.3.0 beta** на ESP32-S3.

Обрано п'ять фіч для технічної здачі: лампа, реле, телеметрія, акаунт і Alert center. Обсяг відповідає [уточненню куратора](reference/COURSEWORK_SCOPE.png); початкова умова — [COURSEWORK.pdf](reference/COURSEWORK.pdf).

## Результат

- 36 тест-кейсів; 32 автоматизовано. Ручні перевірки на 2.3.0: контакти реле, зовнішній LED і кольори RGB — **Pass**; яскравість у чотирьох режимах — **Not Run**. На 2.1.0 усі 4 ручні кейси — **Not Run**.
- 70 параметризованих варіантів на кожну версію: 2.1.0 — 57 Pass / 6 Fail / 7 N/A; 2.3.0 — 63 Pass / 3 Fail / 4 N/A.
- 6 баг-репортів із повторним відтворенням і UART-доказами; 179 очищених логів.
- **NO-GO для 2.3.0:** недопустимий pulse 99 виконується; підтвердження наявного alert за ID повертає E851.

Числа автоматизованих варіантів не включають ручні кейси. [Ручний прогін 2.3.0](logs/manual-2.3.0-01/OPERATOR_REPORT.md) записано за підтвердженням виконавця. Покриття обраних фіч описане в матриці; повне покриття всього PRD не заявляється.

## Матеріали для перевірки

| Матеріал | Файл |
|---|---|
| Підсумки, матриця багів і висновок | [REPORT.md](REPORT.md) |
| Тест-план | [TEST_PLAN.md](docs/TEST_PLAN.md) |
| Кейси з передумовами, даними, кроками й очікуваннями | [TEST_CASES.md](docs/TEST_CASES.md) |
| Вимога → кейс → результат → баг | [TRACEABILITY.md](docs/TRACEABILITY.md) |
| Результати кожного параметра та посилання на логи | [EXECUTION_RESULTS.md](docs/EXECUTION_RESULTS.md) |
| Реальний стенд і фото | [Опис обладнання](docs/REAL_STAND.md), [фото](docs/assets/REAL_STAND_2026-10-24.jpg) |
| HIL для SENTRY: сонар, макет клапана, індикація та CI | [Опис](docs/HIL_STAND.md), [схема PNG](docs/assets/HIL_STAND.png) |
| Презентація | [PDF](docs/presentation/SENTRY_SWM2_QA.pdf), [PowerPoint](docs/presentation/SENTRY_SWM2_QA.pptx) |
| Фреймворк і запуск | [tests/README.md](tests/README.md) |
| Ручний прогін і запис результатів | [MANUAL_RUN.md](docs/MANUAL_RUN.md) |
| Вимоги й підключення | [PRD.md](reference/PRD.md), [WIRING.md](reference/WIRING.md) |

## Запуск автотестів

Перевірене середовище: Python 3.14.7, pytest 9.1.1, pyserial 3.5; macOS, UART 115200 8N1. Для виконання потрібна ESP32-S3 із відповідною прошивкою, збереженим Wi-Fi та створеним тестовим профілем.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp config.example.json config.local.json
```

У `config.local.json` указати логін і пароль тестового профілю. `"port": null` вмикає автопошук єдиного USB-пристрою з VID 1A86; `--port` дозволяє задати порт вручну. Закрити інші UART-термінали. Для beta Guard має бути disarmed.

```bash
python -m pytest --collect-only -q
python -m pytest -m smoke --fw=2.3.0
python -m pytest --fw=2.3.0
```

Без `--run-id` новий каталог доказів обирається автоматично: `auto-001`, `auto-002` тощо. Для stable указати `--fw=2.1.0`. Збирання тестів через `--collect-only` не потребує підключеної плати. Підготовка прошивки — у [firmware/README.md](firmware/README.md); докладні параметри — у [tests/README.md](tests/README.md).

## Структура

```text
reference/     умова, уточнення обсягу, PRD і схема підключення
firmware/      інструкція отримання образу та SHA256
framework/     UART-драйвер
conftest.py    фікстури, підготовка, очищення та звіти
tests/         автотести pytest
docs/          тестова документація, HIL і презентація
bugs/          шість баг-репортів
logs/          очищені докази прогонів і повторного відтворення
```

`.venv/`, `config.local.json`, `reports/`, сирі `logs/raw/` та образ прошивки залишаються локальними. Згенеровані звіти створюються під час запуску; результати виконаних перевірок і очищені докази доступні в репозиторії.
