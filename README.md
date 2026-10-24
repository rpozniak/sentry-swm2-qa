# SENTRY SWM-2 QA

Курсовий проєкт Embedded QA Engineer: перевірки прошивок 2.1.0 stable та 2.3.0 beta на ESP32-S3.

Обрані фічі: лампа, реле, телеметрія, акаунт і Alert center. Обсяг: 36 кейсів із параметризованими варіантами та окремими фізичними перевірками.

## Матеріали

- [Тест-план](docs/TEST_PLAN.md)
- [Тест-кейси](docs/TEST_CASES.md)
- [Матриця трасування і результатів](docs/TRACEABILITY.md)
- [Вимоги прошивки](reference/PRD.md)
- [Підключення стенда](reference/WIRING.md)

## Структура

```text
reference/     вимоги, схема підключення та OTA-інструмент
firmware/      локальний стартовий образ і SHA256
framework/     код керування пристроєм
tests/         автотести pytest
docs/          тестова документація
logs/          очищені докази
logs/raw/      локальні сирі логи, виключені з Git
```

## Середовище Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Команда запуску pytest із кореня репозиторію: `python -m pytest`.

## Докази

Результати записуються для фактично виконаних перевірок. Очищені UART-логи, фото та вимірювання пов'язуються з ID кейсів у матриці. Паролі й інші секрети замінюються на `***` перед додаванням у Git.

## Репозиторій

[rpozniak/sentry-swm2-qa](https://github.com/rpozniak/sentry-swm2-qa), основна гілка `main`.
