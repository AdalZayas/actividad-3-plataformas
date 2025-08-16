"""
Prueba funcional de la interfaz de usuario de Spring PetClinic (Python 3).

- Navega: Owners (hover) -> Add New
- Llena formulario y envía
- Verifica que el nuevo propietario aparece en la lista

Requisitos:
  pip install selenium
Asegúrate de tener chromedriver compatible en PATH o ChromeDriver Manager.
"""

import os
import uuid
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_add_owner_ui():
    """Automatiza la adición de un nuevo propietario mediante la UI (Owners -> Add New)."""
    front = os.getenv("FRONT_URL", "http://localhost:4200/petclinic")

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)
    actions = ActionChains(driver)

    try:
        # 1) Ir al front-end (welcome)
        driver.get(f"{front}/welcome")

        # 2) Hover sobre el menú "Owners"
        owners_toggle = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//li[contains(@class,'dropdown')]/a[contains(., 'Owners')]")
            )
        )
        actions.move_to_element(owners_toggle).perform()
        actions.click(owners_toggle).perform()

        # 3) Click en submenú "Add New"
        add_new = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//ul[contains(@class,'dropdown-menu')]//a[normalize-space()='Add New']")
            )
        )
        add_new.click()

        # 4) Rellenar formulario
        wait.until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys("John")
        driver.find_element(By.ID, "lastName").send_keys("doe")
        driver.find_element(By.ID, "address").send_keys("Av. Siempre Viva 742")
        driver.find_element(By.ID, "city").send_keys("Springfield")
        driver.find_element(By.ID, "telephone").send_keys("1231231234")

        add_owner_btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[@type='submit' and contains(@class,'btn-default') and normalize-space()='Add Owner' and not(@disabled)]"
            ))
        )
        add_owner_btn.click()

        time.sleep(2)
        # 3) Buscar por apellido y enviar
        last_name_input = wait.until(EC.presence_of_element_located((By.ID, "lastName")))
        last_name_input.clear()
        last_name_input.send_keys("doe")
        last_name_input.send_keys(Keys.ENTER)

        table_names = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.table-striped tbody tr td.ownerFullName a")))
        if table_names:
            assert table_names[0].text.strip() == "John doe", "El nuevo propietario no aparece en la lista."

    finally:
        driver.quit()

# Probar si el nuevo propietario aparece en la lista 

if __name__ == "__main__":
    test_add_owner_ui()
    print("Prueba funcional de UI completada correctamente.")
