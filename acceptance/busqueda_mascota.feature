# language: es
#
# Pruebas de aceptación para Spring PetClinic
# Este escenario describe la búsqueda de un propietario existente.

Característica: Búsqueda de propietario
  Como usuario de la aplicación
  Quiero poder buscar un propietario por su apellido
  Para consultar su información y sus mascotas

  Escenario: Buscar un propietario por su apellido
    Dado que la aplicación PetClinic está abierta
    Y existe un propietario registrado con el apellido "Franklin"
    Cuando busco el propietario por su apellido
    Entonces debería ver la información del propietario y sus mascotas
