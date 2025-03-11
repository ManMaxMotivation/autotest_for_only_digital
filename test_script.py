import json
import random
import time
import logging
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Логирование
success_logger = logging.getLogger('success_logger')
error_logger = logging.getLogger('error_logger')
success_handler = logging.FileHandler('positive_tests.log', mode='w', encoding='utf-8')
error_handler = logging.FileHandler('negative_tests.log', mode='w', encoding='utf-8')
success_logger.addHandler(success_handler)
error_logger.addHandler(error_handler)
success_logger.setLevel(logging.INFO)
error_logger.setLevel(logging.ERROR)

# Загружаем тестовые данные
def load_test_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

test_data = load_test_data("test_data.json")

# Настройка драйвера
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://only.digital/projects#brief")
time.sleep(5)  # Ожидание загрузки страницы

# Закрытие окна с куки (если оно появляется)
try:
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Cookie_rootButton__38Z2N')]"))
    )
    cookie_button.click()
    success_logger.info("Успешно: кнопка 'Окей' нажата")
    time.sleep(1)
except Exception as e:
    error_logger.error(f"Ошибка при попытке нажать кнопку 'Окей'. Ошибка: {e}")

# Ожидание прохождения reCAPTCHA вручную
input("Пройдите reCAPTCHA вручную и нажмите Enter для продолжения...")

# Подсчет успешных и неудачных тестов
successful_tests = 0
failed_tests = 0

# Функция для заполнения полей
def fill_field(field_name, values, is_required=False):
    global successful_tests, failed_tests
    for value in values:
        try:
            field = driver.find_element(By.NAME, field_name)
            field.clear()
            field.send_keys(value)
            time.sleep(1)

            if is_required and not value:
                error_logger.error(f"Ошибка: поле {field_name} не заполнено")
                failed_tests += 1
            else:
                success_logger.info(f"Успешно: поле {field_name} заполнено значением {value}")
                successful_tests += 1
        except Exception as e:
            error_logger.error(f"Ошибка: не удалось заполнить поле {field_name}. Ошибка: {e}")
            failed_tests += 1

# Заполняем поля
fill_field("name", test_data["your_contact_information"]["name"], is_required=True)
fill_field("phone", test_data["your_contact_information"]["phone"], is_required=True)
fill_field("email", test_data["your_contact_information"]["email"])
fill_field("company", test_data["your_contact_information"]["company"])

# Проверяем чекбоксы "About the project"
for xpath in test_data["about_project"]:
    try:
        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)
        success_logger.info(f"Успешно: чекбокс с XPath '{xpath}' выбран")
        successful_tests += 1
    except Exception as e:
        error_logger.error(f"Ошибка при клике по чекбоксу '{xpath}'. Ошибка: {e}")
        failed_tests += 1

# Заполняем поле "Tell us about your project"
for text_value in test_data["tell_about_project"]:
    try:
        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "description"))
        )
        driver.execute_script("arguments[0].value = arguments[1];", textarea, text_value)
        time.sleep(1)
        success_logger.info(f"Успешно: поле 'Tell us about your project' заполнено значением '{text_value}'")
        successful_tests += 1
    except Exception as e:
        error_logger.error(f"Ошибка при заполнении поля 'Tell us about your project'. Ошибка: {e}")
        failed_tests += 1

# Выбираем случайный бюджет
try:
    random_budget_xpath = random.choice(test_data["budget_options"])
    budget_radio = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, random_budget_xpath))
    )
    driver.execute_script("arguments[0].click();", budget_radio)
    time.sleep(1)
    success_logger.info(f"Успешно: выбран бюджет '{random_budget_xpath}'")
    successful_tests += 1
except Exception as e:
    error_logger.error(f"Ошибка при выборе бюджета. Ошибка: {e}")
    failed_tests += 1

# Выбираем случайный источник "How did you find us?"
try:
    random_source_xpath = random.choice(test_data["how_did_you_find_us"])
    source_checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, random_source_xpath))
    )
    driver.execute_script("arguments[0].click();", source_checkbox)
    time.sleep(1)
    success_logger.info(f"Успешно: выбран источник '{random_source_xpath}'")
    successful_tests += 1
except Exception as e:
    error_logger.error(f"Ошибка при выборе источника '{random_source_xpath}': {e}")
    failed_tests += 1

# Проверяем кнопку "Start a project"
try:
    start_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start a project')]"))
    )
    if start_button.is_enabled():
        success_logger.info("Кнопка 'Start a project' активна")
        successful_tests += 1
    else:
        error_logger.error("Ошибка: кнопка 'Start a project' неактивна")
        failed_tests += 1
except Exception as e:
    error_logger.error(f"Ошибка при проверке кнопки 'Start a project'. Ошибка: {e}")
    failed_tests += 1

# Финальный отчет
total_tests = successful_tests + failed_tests
print(f"\n=== Финальный отчет ===\n"
      f"Всего тестов: {total_tests}\n"
      f"✅ Успешных: {successful_tests}\n"
      f"❌ Неудачных: {failed_tests}\n"
      f"🔍 Результат: {'Есть баги' if failed_tests > 0 else 'Багов нет'}\n")

# Закрываем браузер
driver.quit()