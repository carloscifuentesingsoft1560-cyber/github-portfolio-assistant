# Arquitectura del Proyecto

## Objetivo

GitHub Portfolio Assistant es una aplicación desarrollada en Python cuyo propósito es automatizar el flujo de publicación y mantenimiento de proyectos en GitHub.

---

# Arquitectura

```
github-portfolio-assistant
│
├── app.py
│
├── src
│
├── config
│
├── docs
│
├── templates
│
├── assets
│
└── tests
```

---

## Responsabilidad de cada carpeta

### app.py

Punto de entrada de la aplicación.

No contiene lógica de negocio.

---

### src/

Contiene toda la lógica principal del sistema.

Aquí se implementan los módulos funcionales.

---

### config/

Configuraciones globales del proyecto.

---

### templates/

Plantillas reutilizables.

---

### assets/

Recursos gráficos e imágenes.

---

### docs/

Documentación técnica.

---

### tests/

Pruebas del sistema.

---

## Principios del proyecto

- Separación de responsabilidades.
- Código reutilizable.
- Arquitectura modular.
- Escalabilidad.
- Documentación desde el inicio.