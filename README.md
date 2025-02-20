# Автоматизированное тестирование формы на сайте only.digital

## Описание

Этот проект предназначен для автоматизированного тестирования формы на сайте only.digital с использованием Selenium и Python. Он включает как позитивные, так и негативные проверки для различных типов полей и чекбоксов, а также для кнопки "Start a project".

В рамках тестирования используются различные техники, такие как:
- Классы эквивалентности
- Граничные значения
- Таблицы принятия решений

### Типы тестов:
1. **Позитивные тесты** – Проверка корректных данных, которые должны проходить тестирование и делать кнопку "Start a project" активной.
2. **Негативные тесты** – Проверка некорректных данных, которые должны оставить кнопку неактивной.

**Общее количество тестов**: 128 (по количеству возможных комбинаций полей).

### Структура тестовых данных:
Тестовые данные для каждого поля вводятся в формате `test 1`, `test 2`, и т. д. и загружаются из файла `test_data.json`.

### Поля, проверяемые в тестах:
1. **Your contact information**:
    - Имя (Name)
    - Телефон (Phone) – обязательное поле
    - E-mail – валидные и невалидные адреса
    - Компания (Company)
2. **About the project** – Чекбоксы с типами проектов: Work package, Website, Service, Design, UX-audit, Branding
3. **Tell us about your project** – обязательное текстовое поле
4. **Attach a file** – загрузка файла (или без файла)
5. **Budget** – выбор из 5 вариантов
6. **How did you find out about us?** – выбор из 5 вариантов
7. **Кнопка "Start a project"** – проверка активации кнопки в зависимости от введённых данных

### Логирование:

В проекте реализовано логирование, которое сохраняет результаты всех тестов:
- Логирование успешных тестов с указанием тестовых данных, которые прошли проверку.
- Логирование неудачных тестов с указанием ошибки и тестовых данных, которые не прошли проверку.

Логи сохраняются в два файла:
1. `positive_tests.log` – для успешных тестов. В этом файле будут записываться данные, которые прошли все проверки.
2. `negative_tests.log` – для неудачных тестов. Этот файл будет содержать ошибки и данные, которые не прошли тесты.

Логирование помогает отслеживать, какие тесты были успешными, а какие — неудачными, с возможностью легко анализировать проблему.

## Структура проекта
```
/your-repository
│
├── test_script.py         # Основной скрипт для тестирования
├── test_data.json         # Тестовые данные
├── requirements.txt       # Файл с зависимостями
└── README.md              # Описание проекта
```

## Установите необходимые зависимости

Выполните команду для установки всех зависимостей:

```bash
pip install -r requirements.txt
```
## В файле requirements.txt должны быть указаны все нужные библиотеки:
selenium
webdriver-manager
pytest

## Запустите тесты. Для запуска тестов выполните команду:
```bash
python test_script.py
```

