# Proyecto PPDA - Grupo 8


## Descripción General

El Proyecto PPDA (Plan de Prevención y Descontaminación Atmosférica) es una aplicación web desarrollada con Django Rest Framework
que tiene como objetivo gestionar medidas ambientales destinadas a la descontaminación atmosférica en diversas regiones.

La plataforma permite la administración de planes, medidas, tipos de medidas, organismos sectoriales y reportes relacionados con el cumplimiento de objetivos ambientales declarados por la SMA.

## Instalacion del Proyecto


    1.-  Clonar el proyecto desde el repositorio de GitHub: 
                https://github.com/angelo-lion/PPDA_2

    2 .- Instalar las dependencias del proyecto: 
                pip install pipenv
                pipenv install
    
    3.-  Activar el entorno virtual de pipenv:
                pipenv shell

    4.1 - Limpiar projecto Django (Opcional si el proyecto ya fué descargado y se necesita volver a cero):
                python manage.py clean_django_project
            
            *se recomienda no utilizarlo si no está consciente que se elmina la base de datos, paso 5 obligatorio luego de esto.

    4.2 - Aplicar las migraciones de la base de datos:
                python manage.py makemigrations
                python manage.py migrate
    
    5 .- Cargar datos iniciales (fixture):
                python manage.py load_initial_data
    
    6 .- Iniciar servidor Backend;:
                python manage.py runserver



### Links de Utilidad
    - https://github.com/angelo-lion/PPDA_2
    - https://tree.taiga.io/project/mfaundes-gis-proyecto-final-solucion-sma/backlog

## Características Principales

    1. Gestión de Planes de Descontaminación:

        -   Registro y administración de planes ambientales.
        -   Asociación de medidas específicas a cada plan.
        -   Trazabilidad mediante registros históricos.

    2. Gestión de Medidas Ambientales:

        -   Registro y seguimiento de medidas implementadas por organismos sectoriales.
        -   Monitoreo del estado de las medidas (pendiente, en progreso, completado).
        -   Trazabilidad mediante registros históricos.

    3. Reportes:

        -   Registro y seguimiento de reportes técnicos sobre las medidas que componen el PPDA.
        -   Trazabilidad mediante registros históricos.

    4. Organismos Sectoriales:
        -   Registro y administración de organismos sectoriales involucrados.
        -   Trazabilidad mediante registros históricos.

    5. Autenticación, Roles y Permisos:

        -   Sistema de autenticación basado en JWT (JSON Web Tokens).
        -   Roles definidos para usuarios: Administrador del sistema, funcionario sectorial, analista SMA y administrador SMA.
            - Administrador del sistema: Contiene todos los permisos de superusuario
            - Funcionario Sectorial: Visualizacion de: Organismos, Tipo de Medida, Medida, Plan de Descontaminacion y Reporte; Añadir Rporte y Editar Reporte.
            - Analista SMA: Visualizacion de: Organismos, Tipo de Medida, Medida, Plan de Descontaminacion y Reporte; Añadir, Editar y Eliminar una Medida.
            - Administrador SMA: CRUD de Organismo, CRUD de Tipo de Medida, CRUD de Medida, CRUD de Plan de Descontaminación y Visualización de Reporte

    6. Generación centralizada de datos iniciales (incluyendo usuarios y permisos):
        -   Se ponen a disposición 4 usuarios con sus perfiles para probar endpoints (todos con clave admin por ahora)
        -   Se incuye usuario admin@gmail.com como superusuario

    7. Documentación API:
        -   Documentación interactiva Swagger disponible en /api/docs/.
        -   Schemma descargable desde /api/schemma/

## Estructura del Proyecto

El proyecto está dividido en cuatro aplicaciones principales:
- Authentication: Gestión de usuarios y sistema de autenticación.
- [Authorization](authorization/README.md) : Gestión de roles y permisos.
- [Core](core/README.md): Gestión de lógica de negocio.
- PPDA: Configuración central del proyecto.

Tecnologías Utilizadas
-    Backend: Django, Django REST Framework.
-    Base de Datos: SQLite3.

Dependencias Adicionales:
-    DRF Spectacular para documentación API.
-    SimpleJWT para autenticación.
-    Whitenoise para uso de certificado ssl.
-    Factory Boy
-    Coverage
-    
  





## Endpoints Principales
    Autenticación:
        POST /api/authentication/login/: Iniciar sesión (obtener tokens JWT).
        POST /api/authentication/refresh/: Refrescar Token de Acceso (Vía Refresh Token)
        POST /api/authentication/logout/: Cerrar sesión.
        POST /api/authentication/register/: Registrar nuevo usuario (Usuario Administrador requerido)

    Organismo:
        GET /api/organismo/: Listar organismos.
        POST /api/organismo/: Crear un nuevo organismo.

    Planes de Descontaminacion:
        GET /api/plan_descontaminacion/: Listar planes.
        POST /api/plan_descontaminacion/: Crear un nuevo plan.

    Tipo de Medidas:
        GET /api/tipo_medida/: Listar tipos de medida.
        POST /api/tipo_medida/: Crear un tipo de medida.

    Medidas:
        GET /api/medida/: Listar medidas.
        POST /api/medida/: Crear una nueva medida.

    Reportes:
        GET /api/reporte/: Listar reporte asociados a las medidas.
        POST /api/reporte/: Crear un nuevo reporte

    La documentación completa está disponible en /api/docs/.


# Testing
Importante para revisar covertura y testing!
- [Testing - Link](authentication/tests/Testing.md).


# PIPENV - Comandos

1) Revisar paquetes con vulnerabilidades de seguridad:

pipenv check

2) Para resolver vulnerabilidades, primero identifica los paquetes afectados usando pipenv check. Luego actualízalos individualmente o todos:

    Generar archivo requirements.txt desde Pipfile (útil para despliegue o CI/CD):
        pipenv requirements > requirements.txt

    Actualizar un paquete específico:
        pipenv update django

    Actualizar todos los paquetes dentro del Pipfile (con precaución):
        pipenv update

    Ver paquetes instalados:
        pipenv graph

    Mostrar ubicación del entorno virtual actual:
        pipenv --venv

    Eliminar entorno virtual completo
        pipenv --rm