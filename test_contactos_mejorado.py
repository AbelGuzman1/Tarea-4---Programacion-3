import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Config
BASE_URL = "http://localhost:8000/contactos.html"
TARGET_URL_FRAGMENT = "contactos.html"

NAME_FIELD = (By.ID, "nombre")
EMAIL_FIELD = (By.ID, "email")
CONTACT_FIELD = (By.ID, "contacto")
CREATE_BUTTON = (By.ID, "btnCrear")


@pytest.fixture(scope="module")
def driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,1024")
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def tomar_captura(driver, nombre):
    ruta = os.path.join(os.getcwd(), 'screenshots', f"{nombre}.png")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    driver.save_screenshot(ruta)


def esperar_carga(driver):
    try:
        WebDriverWait(driver, 8).until(EC.url_contains(TARGET_URL_FRAGMENT))
    except TimeoutException:
        pass


def contar_filas(driver):
    esperar_carga(driver)
    try:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tablaContactos tbody')))
        filas = driver.find_elements(By.CSS_SELECTOR, '#tablaContactos tbody tr')
        return len(filas)
    except Exception:
        return 0


def test_crear_y_eliminar(driver):
    driver.get(BASE_URL)
    esperar_carga(driver)
    inicial = contar_filas(driver)
    driver.find_element(*NAME_FIELD).send_keys('Prueba Uno')
    driver.find_element(*EMAIL_FIELD).send_keys('prueba@example.com')
    driver.find_element(*CONTACT_FIELD).send_keys('8091234567')
    driver.find_element(*CREATE_BUTTON).click()
    WebDriverWait(driver, 12).until(lambda d: contar_filas(d) == inicial + 1)
    tomar_captura(driver, 'crear_ok')
    # eliminar
    eliminar_btn = driver.find_elements(By.CSS_SELECTOR, '#tablaContactos tbody tr .btnEliminar')[-1]
    eliminar_btn.click()
    WebDriverWait(driver, 8).until(lambda d: contar_filas(d) == inicial)
    tomar_captura(driver, 'eliminar_ok')
