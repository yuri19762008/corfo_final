# 🛠 Comandos de Administración Personalizados

## 🧹 Comando clean_django_project

Este comando elimina completamente la base de datos SQLite, todas las migraciones generadas (excepto los archivos __init__.py) y archivos temporales como __pycache__ y .pyc en todo el proyecto.


🧪 ¿Qué hace?
	•	Elimina el archivo db.sqlite3 si existe.
	•	Limpia todas las migraciones en apps listadas en settings.LOCAL_APPS.
	•	Borra carpetas __pycache__ y archivos .pyc en todos los subdirectorios del proyecto.

🚀 Uso
    ```python manage.py clean_django_project```
	
Este comando es útil para reiniciar el proyecto y asegurarse de que no haya migraciones cruzadas o inconsistentes. Se recomienda usarlo con precaución, ya que eliminará todos los datos de la base de datos.

## 📦 Comando load_initial_data

Este comando carga una serie de fixtures iniciales en un orden específico, asegurando que la base de datos quede configurada con usuarios, perfiles, datos de dominio (medidas, planes, organismos, etc.) y que los usuarios tengan sus permisos correctamente asignados.


A diferencia de loaddata, este comando:

- ✅ Usa save() al crear cada objeto, activando validaciones, campos auto_now_add, clean() y relaciones reales como ForeignKey y ManyToMany.

- ✅ Resuelve dependencias como objetos relacionados o claves foráneas al vuelo.

- ✅ Llama a la lógica de asignación de permisos centralizada definida en authori zation/utils.py.

- ✅ Asigna fechas de creación/modificación automáticamente si no están presentes.


🧪 ¿Qué hace?
1.	Carga los fixtures definidos en orden:
	•	authorization/fixtures/profiletype.json
	•	authentication/fixtures/users.json
	•	core/fixtures/organismos_sectoriales.json
	•	core/fixtures/tipo_medidas.json
	•	core/fixtures/medidas.json
	•	core/fixtures/planes_descontaminacion.json
2.	Asigna:
	•	Permisos a usuarios según su profile_type.
	•	Timestamps (fecha_creacion, fecha_modificacion) si están vacíos.

🚀 Uso
    ```python manage.py load_initial_data```

Este comando es útil luego de un clean_django_project, ya que deja la base de datos lista para trabajar con todos los roles, usuarios y permisos necesarios.