# ✅ Módulo `authentication`

### 🔐 Descripción general

Este módulo gestiona la autenticación de usuarios mediante JWT y contempla:

- Registro de usuarios (`/register/`)
- Login con token JWT (`/login/`)
- Logout con invalidación de refresh token (`/logout/`)
- Serializador de usuario con lógica de permisos (`UserSerializer`)
- Uso de `ProfileType` para controlar roles
- Panel de administración personalizado

---

### 🧪 Cobertura de tests (vía `coverage.py`)

Cobertura global del proyecto: **84%**  
Cobertura específica del módulo `authentication`:

| Componente               | Cobertura  | Estado        |
|--------------------------|------------|----------------|
| `views.py`               | 100%       | ✅ Completo     |
| `serializers.py`         | 87%        | ✅ Completo     |
| `test_login.py`          | 100%       | ✅ Implementado |
| `test_register.py`       | 100%       | ✅ Implementado |
| `test_logout.py`         | 100%       | ✅ Implementado |
| `factories.py`           | 100%       | ✅ Implementado |
| `models.py`              | 59%        | ⚠️ Solo funciones usadas |
| `forms.py`               | 61%        | ⚠️ No se priorizó por ahora |
| `admin.py`               | 69%        | ⚠️ No cubierto por tests aún |

---

### 📌 Estado del módulo

✅ Todos los flujos de API críticos cubiertos  
✅ Contraseñas hasheadas correctamente  
✅ Flags `is_staff` y `is_superuser` asignados según perfil  
✅ Validación por roles controlada en serializers y admin  
⚠️ No se permite modificación de usuarios vía API (por decisión de negocio actual)

---

### 🔜 Próximo paso

> Migración de ProfileType a app Authorization para separar responsabilidades.

---


# 🛡️ Lógicas de Negocio – App `authentication`

Este módulo gestiona la autenticación de usuarios mediante un modelo personalizado, control de perfiles y lógica de permisos alineada con buenas prácticas de Django y DRF.

---

## 1. 👤 Modelo de Usuario Personalizado (`User`)

- Basado en `AbstractBaseUser` + `PermissionsMixin`.
- Campo de autenticación: `email` (único).
- Campos adicionales: `first_name`, `last_name`, `profile_type`.
- Relación con modelo `ProfileType` para definir el rol o tipo de usuario.
- Campo `password` protegido en `save()` para asegurar hasheo en todos los casos.

---

## 2. 🧩 Tipos de Perfil (`ProfileType`)

Definidos en `ProfileTypes` (`TextChoices`):

- `administrador_sistema`: acceso completo (superusuario).
- `administrador_sma`: acceso al panel de administración (staff).
- `analista_sma`: sin privilegios administrativos.
- `funcionario_sectorial`: sin privilegios administrativos.

---

## 3. 🔐 Lógica de Permisos Automática

- Los flags `is_staff` y `is_superuser` **se asignan automáticamente** según el `profile_type`.
- La lógica está implementada en:
  - `UserAdmin.save_model()` (panel de administración de Django).
  - `UserSerializer.create()` (API REST).
- Se **evita manipulación manual** de estos flags en ambos entornos.

| Perfil                  | `is_staff` | `is_superuser` |
|-------------------------|------------|----------------|
| administrador_sistema   | ✅         | ✅             |
| administrador_sma       | ✅         | ❌             |
| otros                   | ❌         | ❌             |

---

## 4. 🔒 Seguridad en el Admin

- `is_staff` y `is_superuser` están definidos como `readonly_fields` en el panel de administración.
- Solo modificables mediante la lógica de negocio en `save_model()`.

---

## 5. 🔐 Seguridad en la API

- `is_staff` y `is_superuser` **no están expuestos** en la API.
- Solo se permite definir `profile_type`, y los permisos se asignan internamente.
- Contraseña (`password`) siempre protegida con `write_only`.

---

## 6. 🛑 Restricciones de edición desde la API

- **No se permite modificar usuarios existentes desde la API.**
- Toda la gestión de usuarios se realiza exclusivamente desde el panel de administración.

---

## 7. 🧪 Cobertura de pruebas (en progreso)

Se desarrollarán tests para:

- Creación de usuarios según perfil y validación de permisos.
- Seguridad del flujo de autenticación.
- Protección contra contraseñas en texto plano.
- Comportamiento de la API en diferentes escenarios.

---
