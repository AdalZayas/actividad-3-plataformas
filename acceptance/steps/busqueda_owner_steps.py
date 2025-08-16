"""
Definiciones de pasos para el escenario de búsqueda de propietario.

Este archivo utiliza Behave y Selenium para automatizar la
interacción con la aplicación web Spring PetClinic. Ajusta rutas
y selectores según tu despliegue. Requiere:
  - Frontend Angular corriendo (por defecto http://localhost:4200/petclinic)
  - Backend REST corriendo (por defecto http://localhost:9966/petclinic)
  - Chromedriver disponible en PATH
"""

import os
import requests

from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


FRONT_URL = os.getenv("FRONT_URL", "http://localhost:4200/petclinic")
API_URL = os.getenv("API_URL", "http://localhost:9966/petclinic")


@given('que la aplicación PetClinic está abierta')
def step_open_application(context):
    """Abre el navegador y carga la página principal de la aplicación."""
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()
    context.wait = WebDriverWait(context.driver, 25)
    context.actions = ActionChains(context.driver)
    context.driver.get(f"{FRONT_URL}/welcome")


@given('existe un propietario registrado con el apellido "{apellido}"')
def step_owner_exists(context, apellido):
    """
    Verifica (vía API) que existe al menos un owner con ese apellido.
    Guarda datos útiles en el contexto para los siguientes pasos.
    """
    url = f"{API_URL}/api/owners"
    resp = requests.get(url, params={"lastName": apellido}, timeout=5)
    resp.raise_for_status()
    data = resp.json()

    assert isinstance(data, list) and len(data) > 0, (
        f"No existe propietario con apellido '{apellido}' en {url}"
    )

    # Primer owner coincidente (ajusta si quieres uno específico)
    owner = data[0]
    context.owner_last_name = apellido
    context.expected_owner_fullname = f"{owner.get('firstName','').strip()} {owner.get('lastName','').strip()}".strip()
    # Nombre de mascota esperado (opcional). Si no hay, usaremos 'Leo' por dataset default.
    pets = owner.get("pets") or []
    context.pet_name = pets[0]["name"] if pets else "Leo"


@when('busco el propietario por su apellido')
def step_search_owner(context):
    """Hover en Owners -> clic en Search -> buscar por apellido -> abrir primer resultado."""
    driver = context.driver
    wait = WebDriverWait(driver, 15)
    actions = context.actions

    # 1) Hover en "Owners"
    owners_toggle = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//li[contains(@class,'dropdown')]/a[contains(., 'Owners')]")
        )
    )
    actions.move_to_element(owners_toggle).perform()
    actions.click(owners_toggle).perform()

    # 2) Clic en "Search"
    search_link = wait.until(EC.element_to_be_clickable( (By.XPATH, "//ul[contains(@class,'dropdown-menu')]//a[normalize-space()='Search']") ) )
    actions.click(search_link).perform()

    # 3) Buscar por apellido y enviar
    last_name_input = wait.until(EC.presence_of_element_located((By.ID, "lastName")))
    last_name_input.clear()
    last_name_input.send_keys(context.owner_last_name)
    last_name_input.send_keys(Keys.ENTER)

    table_names = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.table-striped tbody tr td.ownerFullName a")))

    # Hacer clic en el primer resultado
    if table_names:
        actions.move_to_element(table_names[0]).perform()
        actions.click(table_names[0]).perform()


@then('debería ver la información del propietario y sus mascotas')
def step_verify_owner_and_pets(context):
    """Verifica que se muestra la información del propietario y al menos una mascota."""
    driver = context.driver
    wait = context.wait
    pet_name = getattr(context, "pet_name", "Leo")

    # Presencia de secciones clave en la vista de detalle
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//h2[normalize-space()='Owner Information']")
    ))
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//h2[normalize-space()='Pets and Visits']")
    ))

    # Verifica al menos un 'Name' de mascota en la tabla de pets
    name_dd = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//table[contains(@class,'table-striped')]"
            "//dl[contains(@class,'dl-horizontal')]"
            "/dt[normalize-space()='Name']/following-sibling::dd[1]"
        ))
    )

    # Si quieres verificar un nombre específico (del contexto o por defecto)
    assert pet_name.lower() in name_dd.text.lower(), (
        f"No se encontró la mascota esperada. "
        f"Esperado contiene: '{pet_name}', encontrado: '{name_dd.text}'"
    )
