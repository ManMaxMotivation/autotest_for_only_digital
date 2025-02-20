import json
import random
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Логирование
success_logger = logging.getLogger('success_logger')
error_logger = logging.getLogger('error_logger')
success_handler = logging.FileHandler('positive_tests.log', mode='w')
error_handler = logging.FileHandler('negative_tests.log', mode='w')
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

# Подсчет успешных и неудачных тестов
successful_tests = 0
failed_tests = 0


# Функция для заполнения полей с тестовыми данными
def fill_field(field_name, values, is_required=False):
    global successful_tests, failed_tests
    for value in values:
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


# Заполняем поля
fill_field("name", test_data["your_contact_information"]["name"], is_required=True)
fill_field("phone", test_data["your_contact_information"]["phone"], is_required=True)
fill_field("email", test_data["your_contact_information"]["email"])
fill_field("company", test_data["your_contact_information"]["company"])

# Проверяем чекбоксы "About the project"
for option in test_data["about_project"]:
    checkbox = driver.find_element(By.XPATH, f"//label[contains(text(), '{option}')]")
    checkbox.click()
    time.sleep(1)
    success_logger.info(f"Успешно: чекбокс '{option}' выбран")
    successful_tests += 1

# Проверяем поле "Tell us about your project"
fill_field("project", test_data["tell_about_project"])

# Выбираем случайный бюджет
random_budget = random.choice(test_data["budget"])
driver.find_element(By.XPATH, f"//label[contains(text(), '{random_budget}')]").click()

# Выбираем источники "How did you find us?"
for source in test_data["how_did_you_find_us"]:
    driver.find_element(By.XPATH, f"//label[contains(text(), '{source}')]").click()
    time.sleep(1)
    success_logger.info(f"Успешно: чекбокс '{source}' выбран")
    successful_tests += 1

# Проверяем кнопку "Start a project"
start_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Start a project')]")
if start_button.is_enabled():
    success_logger.info("Кнопка 'Start a project' активна и может быть нажата")
    successful_tests += 1
else:
    error_logger.error("Ошибка: кнопка 'Start a project' неактивна")
    failed_tests += 1

# Финальный отчет
total_tests = successful_tests + failed_tests
bugs = "Есть баги" if failed_tests > 0 else "Багов нет"

# Выводим отчет
print(f"Всего тестов: {total_tests}")
print(f"Успешных тестов: {successful_tests}")
print(f"Неудачных тестов: {failed_tests}")
print(f"{bugs}")

# Закрываем браузер
driver.quit()