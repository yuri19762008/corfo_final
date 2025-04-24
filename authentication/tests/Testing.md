## 🧪 Testing y Coverage

Este proyecto utiliza `coverage.py` para medir qué tanto del código está cubierto por tests.

---

### 🔄 Cómo ejecutar los tests con cobertura

```bash
# Ejecutar todos los tests con coverage
coverage run manage.py test

# Ver resumen en consola
coverage report -m

# Generar reporte HTML visual
coverage html
open htmlcov/index.html  # Solo en macOS
```

---

### 🎯 Ejecutar coverage por app

```bash
# Para authentication
coverage run manage.py test authentication
coverage report -m --include='*/authentication/*'

# Para authorization
coverage run manage.py test authorization
coverage report -m --include='*/authorization/*'

# Para core
coverage run manage.py test core
coverage report -m --include='*/core/*'
```

---

### 📚 Niveles de prueba utilizados

| Nivel           | Enfoque                                  | Herramientas principales        |
|-----------------|-------------------------------------------|----------------------------------|
| API/Integración | Testean endpoints de la API en conjunto  | `APITestCase`, `factory_boy`    |
| Unitario        | Testean funciones o métodos individuales  | `TestCase`, `factory_boy`       |

---

### ▶️ Comandos útiles

| Acción                           | Comando                                                             |
|----------------------------------|----------------------------------------------------------------------|
| Ejecutar todos los tests         | `python manage.py test`                                             |
| Ejecutar tests de una app        | `python manage.py test authentication.tests`                        |
| Ejecutar un archivo específico   | `python manage.py test authentication.tests.test_login`             |
| Ejecutar un método específico    | `python manage.py test authentication.tests.test_login.LoginTestCase.test_login_admin_sma` |

---

### 📌 Notas

- Cada test se ejecuta sobre una base de datos temporal.
- Los objetos se generan con `factory_boy`.
- Se recomienda mantener los tests organizados por funcionalidad o app.

---

### 🧰 ¿Qué es `factory_boy`?

`factory_boy` permite crear datos de prueba sin depender de fixtures.

Se utiliza para:
- Usuarios (`UserFactory`)
- Tipos de Perfil (`ProfileTypeFactory`)

❗ **No usar `python -m unittest` directamente**, ya que no carga `settings.py` de Django.  
Siempre usa `python manage.py test` para evitar errores de entorno.