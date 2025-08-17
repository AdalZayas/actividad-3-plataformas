# Pruebas automatizadas para Spring PetClinic

Este paquete contiene ejemplos de scripts de automatización de pruebas diseñados
para la aplicación **Spring PetClinic**. Los scripts se han organizado
según el tipo de prueba descrita en el documento de la actividad:

- **Pruebas de aceptación (validación)**: se ofrecen en el directorio
  `acceptance` empleando la sintaxis de Behaviour‑Driven Development (BDD).
  Contienen escenarios escritos en castellano que describen el comportamiento
  esperado de la aplicación y un esqueleto de implementación con Selenium.
  
- **Pruebas funcionales (interfaz de usuario)**: el directorio
  `functional_tests` contiene un ejemplo de script con Selenium que
  navega por la aplicación web, rellena un formulario y verifica que
  los datos se muestran correctamente.

- **Pruebas de carga**: en `load_tests` se incluye un fichero de
  configuración para Locust. Define una carga concurrente sobre
  un punto de consulta de la API para medir el tiempo de respuesta
  cuando múltiples usuarios simultáneos acceden al sistema.

## Ejecución de las pruebas

1. **Requisitos previos**: instale las dependencias indicadas en
   `requirements.txt` utilizando `pip`. Además necesitará
   `Java` y `Maven` para ejecutar el back‑end y `Node.js` para el
   front‑end de PetClinic.

   ```sh
   pip install -r requirements.txt
   ```

2. **Arranque de la aplicación**: desde los proyectos `spring‑petclinic‑rest`
   y `spring‑petclinic‑angular` arranque el back‑end y el front‑end:

   ```sh
   cd spring‑petclinic‑rest
   ./mvnw spring-boot:run
   # en otra terminal
   cd spring‑petclinic‑angular
   npm install
   ng serve
   ```

   De forma predeterminada, el back‑end escuchará en
   `http://localhost:9966/petclinic` y el front‑end en
   `http://localhost:4200`.

3. **Pruebas de aceptación**:

   Desde la raíz del proyecto ejecute Behave para procesar los
   escenarios Gherkin del directorio `acceptance`:

   ```sh
   behave tests/acceptance
   ```

4. **Pruebas funcionales (UI)**:

   Ejecute el script Selenium (asegurándose de disponer del
   `chromedriver` adecuado y de que la aplicación esté corriendo):

   ```sh
   python tests/functional_tests/test_add_owner_ui.py
   ```

5. **Pruebas de carga**:

   Con Locust instalado, lance el intérprete de Locust en
   `load_tests/locustfile.py` e indique el número de usuarios y la
   tasa de generación de nuevos usuarios:

   ```sh
   locust -f tests/load_tests/locustfile.py --headless -u 1000 -r 50 \
     --host=http://localhost:9966/petclinic --run-time 1m
   ```

Estas pruebas sirven como punto de partida y deberán adaptarse a las
concretas rutas y datos de su despliegue de PetClinic. Cada script
incluye comentarios para orientar la personalización.
