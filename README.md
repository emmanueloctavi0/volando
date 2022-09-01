## Introduction

La meta de este proyecto es crear un microservicio para administrar las ordenes de los usuarios para una empresa de logística

Hecho con Django 4.1, Django REST Framework y GEODjango

![Admin view](./doc_imgs/admin.png)

### Main features

* Se crea una orden por un usuario normal o un superusuario
* Consulta de ordenes
* Actualización del estatus de la orden
* Autenticación de usuarios

# Usage

Para user este proyecto

### Docker compose

Se asume que se tiene instalado Docker junto con Docker compose, esto facilitará el poder empezar a modificar el proyecto.

Si usas una Mac con procesador Apple Silicon para evitar problemas usa la siguiente variable

    $ export DOCKER_DEFAULT_PLATFORM=linux/amd64

# Getting Started

Primero clona el repositorio:

    $ https://github.com/emmanueloctavi0/volando.git
    $ cd volando
    
Compila las imágenes de docker

    $ docker compose build
    
Ejecuta el proyecto

    $ docker compose up

Con esto ya puedes interactuar con la API en http://localhost:8000/v1/orders/

### Documentación de la API REST
La documentación está en:
```
app
│
└───docs
│---│---openapi.yml
```
Este archivo se puede importar a una colección de [Postman](https://learning.postman.com/docs/integrations/available-integrations/working-with-openAPI/) o bien visualizarse en https://editor.swagger.io/

### Crear un super usuario

    $ docker compose exec app bash -c "python3 manage.py createsuperuser"

Con este usuario se puede entrar al administrador de Django http://localhost:8000/admin/
Un super usuario puede hacer cualquier operación en cualquier orden, pero un usuario normal sólo puede hacer las operaciones en las ordenes que a él le pertenecen

### Método de autenticación de la API
Usa [token authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication), para hacer un request a la API con la herramienta curl es de la siguiente manera:

	$ curl -X GET http://localhost:8000/v1/orders/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'

### Ejecutar los tests

	$ docker compose exec app bash -c "python3 manage.py test"
