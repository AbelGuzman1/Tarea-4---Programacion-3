import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==========================================================
# CONFIGURACIÓN INICIAL Y DRIVER
# ==========================================================

@pytest.fixture(scope="module")
def driver():
    # Iniciar el driver (Selenium gestiona el navegador automáticamente)
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Función para tomar captura de pantalla automática
def tomar_captura(driver, nombre_escenario):
    # Esto asegura que la captura se guarde en la carpeta 'screenshots'
    ruta_captura = os.path.join(os.getcwd(), 'screenshots', f"{nombre_escenario}.png")
    driver.save_screenshot(ruta_captura)

# ==========================================================
# CASOS DE PRUEBA OBLIGATORIOS (Estructura Base)
# ==========================================================

# HU 1: LOGIN - CAMINO FELIZ
def test_login_camino_feliz(driver):
    # ! IMPORTANTE: REEMPLAZAR POR LA URL DE TU APLICACIÓN
    driver.get("http://URL_DE_TU_APLICACION/login") 
    
    # Rellenar credenciales (REEMPLAZAR LOS IDs DE TU APLICACIÓN)
    driver.find_element(By.ID, "ID_USUARIO").send_keys("usuario_valido")
    driver.find_element(By.ID, "ID_PASSWORD").send_keys("password_valida")
    
    # Clic en el botón (REEMPLAZAR ID_BOTON)
    driver.find_element(By.ID, "ID_BOTON_LOGIN").click() 

    # Asersión de éxito (REEMPLAZAR POR LA PÁGINA DE DESTINO)
    WebDriverWait(driver, 15).until(
        EC.url_contains("/dashboard") 
    )
    tomar_captura(driver, "Login_1_Camino_Feliz")
    assert "dashboard" in driver.current_url.lower()