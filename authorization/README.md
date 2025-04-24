## 🛡️ App `authorization`

✅ Recuerda: si agregas un nuevo perfil, actualiza `ProfileTypes`, `PERMISSIONS_BY_PROFILE_TYPE`, y `setup_groups()`.

Gestión de **roles, perfiles y permisos** del sistema. Esta app define los distintos tipos de usuarios, sus permisos y sus accesos a funcionalidades.

---

### 📌 ¿Qué hace esta app?

- Define tipos de perfil (`ProfileTypes`)
- Asocia cada perfil a un `Group` y permisos específicos
- Aplica automáticamente permisos con `apply_permissions_based_on_profile()`
- Expone la vista protegida `ProfileTypeModelViewSet` con permisos personalizados

---

### 📁 Estructura clave

- `models.py`: modelo `ProfileType` y enum `ProfileTypes`
- `utils.py`: lógica de permisos (asignación, validación, setup)
- `permissions.py`: clases DRF que usan `utils.py` para validar acceso
- `signals.py`: crea grupos y permisos tras migraciones
- `tests/`: pruebas unitarias de roles y permisos

---

### 👥 Tipos de perfil

```python
- ADMINISTRADOR_SISTEMA
- ADMINISTRADOR_SMA
- ANALISTA_SMA
- FUNCIONARIO_SECTORIAL
```

---

### 🔐 Permisos por perfil

La lógica vive en `authorization/utils.py`, en el diccionario:

```python
PERMISSIONS_BY_PROFILE_TYPE = { ... }
```

Cada clave representa un tipo de perfil y su lista de permisos (`codenames`) asociados.

---

### 🧪 Ejecutar tests

```bash
python manage.py test authorization
```

---

### 📦 Fixture disponible

```
authorization/fixtures/profiletype.json
```

---

