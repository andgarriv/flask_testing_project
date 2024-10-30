from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Configurar Selenium para usar Chromium
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Usar webdriver-manager para gestionar el driver de Chromium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Abre la aplicación web
    driver.get("http://localhost:5000")

    # Verifica que el título de la página es correcto
    assert "Gestor de Tareas" in driver.title

    # Buscar el campo de entrada de nueva tarea
    input_field = driver.find_element(By.NAME, "title")

    # Escribir en el campo de entrada
    input_field.send_keys("Tarea de Selenium")
    input_field.send_keys(Keys.RETURN)

    # Verificar que la tarea aparece en la lista
    assert "Tarea de Selenium" in driver.page_source

finally:
    driver.quit()
