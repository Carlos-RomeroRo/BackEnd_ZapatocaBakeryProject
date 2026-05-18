# 🥖 Panadería Zapatoca — Backend API

Backend desarrollado con **FastAPI** bajo principios de **Clean Architecture** para gestionar productos, empleados, carrito de compras y automatizaciones del negocio de la panadería.

El sistema se integra con un frontend en **Angular** y con **n8n** para automatizar procesos como notificaciones por WhatsApp, cálculo de domicilios y geolocalización.

---

## 🎯 Objetivo del proyecto

Construir una solución backend **escalable y profesional** que permita:

| Área | Capacidad |
|------|-----------|
| 🥐 Productos | Gestión del catálogo y cargue masivo desde Excel |
| 👨‍🍳 Empleados | Administración de trabajadores y cargue masivo |
| 🛒 Carrito | Selección de productos por nombre y cantidad |
| 📦 Pedidos | Domicilio o compra presencial |
| 🚚 Domicilios | Costo según distancia |
| 📍 Mapas | Ubicación de la panadería y rutas al cliente |
| 📲 n8n | Automatización de WhatsApp y webhooks |
| 🔗 Angular | API REST para el frontend |

---

## 📊 Estado actual

| Módulo | Estado |
|--------|--------|
| Arquitectura por capas (domain, application, infrastructure, presentation) | ✅ |
| Entidades y repositorios (Producto, Trabajador) | ✅ |
| Persistencia SQLAlchemy (SQLite dev / PostgreSQL ready) | ✅ |
| Excel: plantilla, exportar, importar (productos y trabajadores) | ✅ |
| CORS para Angular (`localhost:4200`) | ✅ |
| Carrito, pedidos, domicilios, geolocalización, n8n | 🔜 Planificado |
| Docker y CI | 🔜 En progreso |

---

## 🏗️ Arquitectura

El proyecto separa responsabilidades en capas independientes. Las dependencias apuntan **hacia el dominio**; la infraestructura implementa los contratos definidos en el núcleo.

```
app/
├── domain/                 # Reglas de negocio puras
│   ├── entities/           # Producto, Trabajador, …
│   └── repositories/       # Interfaces (contratos)
├── application/            # Casos de uso y puertos
│   ├── use_cases/
│   ├── ports/
│   └── dtos/
├── infrastructure/         # Detalles técnicos
│   ├── database/           # ORM, sesión, modelos
│   ├── repositories/       # Implementación SQL
│   └── excel/              # Pandas / openpyxl
├── presentation/           # HTTP / FastAPI
│   └── api/                # Routers y schemas
└── main.py                 # Composición y arranque
```

```mermaid
flowchart TB
    subgraph presentation [Presentation]
        API[FastAPI Routers]
    end
    subgraph application [Application]
        UC[Casos de uso]
    end
    subgraph domain [Domain]
        E[Entidades]
        R[Repositorios abstractos]
    end
    subgraph infrastructure [Infrastructure]
        SQL[SQLAlchemy]
        XLS[Excel Pandas]
    end
    API --> UC
    UC --> R
    UC --> E
    SQL -.implementa.-> R
    XLS -.lee/escribe.-> UC
```

### Capas

| Capa | Contenido |
|------|-----------|
| **Domain** | Entidades, validaciones de negocio, interfaces de repositorios |
| **Application** | Casos de uso, orquestación, DTOs de importación |
| **Infrastructure** | Modelos ORM, SQL, lectura/escritura Excel, servicios externos (futuro) |
| **Presentation** | Endpoints REST, schemas Pydantic, respuestas HTTP |

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|------------|-----|
| Python 3.11+ | Lenguaje base |
| FastAPI | API REST y documentación OpenAPI |
| SQLAlchemy 2 | ORM y acceso a datos |
| SQLite | Desarrollo local (`panaderia.db`) |
| PostgreSQL / Supabase | Producción (vía `DATABASE_URL`) |
| Pandas + openpyxl | Cargue y exportación Excel |
| Angular | Frontend consumidor |
| n8n | Automatizaciones y webhooks |
| Google Maps / OpenStreetMap | Geolocalización (planificado) |

---

## 📦 Módulos del sistema

### 🥐 Productos

- CRUD completo — *planificado*
- **Cargue masivo desde Excel** — ✅
- Gestión de imágenes (URL en campo `foto`) — ✅ en modelo

### 👨‍🍳 Empleados (trabajadores)

- CRUD completo — *planificado*
- **Cargue masivo desde Excel** — ✅

### 🛒 Carrito de compras — *planificado*

- Crear carrito
- Agregar productos por nombre y cantidad
- Calcular subtotales y total

### 📦 Pedidos — *planificado*

- Confirmación del carrito
- Dirección de entrega
- Estados del pedido

### 🚚 Domicilios — *planificado*

- Costo según distancia
- Estimación de tiempo de entrega

### 📍 Geolocalización — *planificado*

- Ubicación de la panadería
- Rutas desde el cliente

### 📲 Automatización con n8n — *planificado*

- Confirmación de pedidos por WhatsApp
- Notificaciones al administrador
- Mensajes al cambiar estado del pedido

---

## 📁 Cargue masivo desde Excel

### Productos

| nombre | descripcion | precio | foto |
|--------|-------------|--------|------|
| Pan francés | Pan tradicional | 1200 | https://... |

> `descripcion`: máximo **100** caracteres.

### Trabajadores

| nombre | descripcion | documento | email | rol | foto |
|--------|-------------|-----------|-------|-----|------|
| Juan Pérez | Atención en mostrador | 12345678 | juan@... | Panadero | |

> Debe indicarse **documento** o **email** (al menos uno).

### Comportamiento del import

- Solo **inserta** registros nuevos.
- Si el nombre del producto (o documento/email del trabajador) ya existe, la fila se reporta en `errores` sin detener el resto del archivo.

---

## 📡 Endpoints disponibles

Base URL: `http://127.0.0.1:8000`

### General

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Health / mensaje de bienvenida |

### Productos

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/productos/excel/plantilla` | Descarga plantilla `.xlsx` |
| `GET` | `/productos/excel/exportar` | Exporta productos de la BD |
| `POST` | `/productos/excel/importar` | Importa productos (`multipart/form-data`) |

### Trabajadores

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/trabajadores/excel/plantilla` | Descarga plantilla `.xlsx` |
| `GET` | `/trabajadores/excel/exportar` | Exporta trabajadores de la BD |
| `POST` | `/trabajadores/excel/importar` | Importa trabajadores |

### Respuesta de importación (ejemplo)

```json
{
  "insertados": 5,
  "errores": [
    { "fila": 3, "motivo": "Ya existe un producto con nombre 'Pan integral'." }
  ]
}
```

### Endpoints planificados

<details>
<summary>Ver roadmap de rutas</summary>

| Área | Rutas previstas |
|------|-----------------|
| Productos | `GET/POST /productos`, CRUD |
| Empleados | `GET/POST /trabajadores`, CRUD |
| Carrito | `POST /carritos`, `POST /carritos/{id}/items`, `GET /carritos/{id}` |
| Pedidos | `POST /pedidos`, `GET /pedidos/{id}` |
| Domicilios | `POST /domicilios/calcular` |
| n8n | `POST /webhooks/n8n/pedido-creado` |

</details>

---

## 🔗 Integración con Angular

El frontend consume la API con `HttpClient`. CORS está habilitado para `http://localhost:4200`.

**Flujo de compra (objetivo):**

1. El cliente navega el catálogo.
2. Agrega productos al carrito.
3. Elige entrega a domicilio o compra presencial.
4. Si es domicilio → cálculo automático del costo.
5. Se crea el pedido → webhook a **n8n** → confirmación por **WhatsApp**.

---

## 🤖 Automatización con n8n

n8n actúa como motor de automatización del negocio.

| Caso de uso | Descripción |
|-------------|-------------|
| Pedido confirmado | Mensaje WhatsApp al cliente |
| Nuevo pedido | Notificación al administrador |
| Ubicación | Enlace a mapa / navegación |
| Marketing | Recordatorios de promociones |

**Flujo ejemplo:**

```
FastAPI (pedido creado) → webhook n8n → flujo n8n → WhatsApp API
```

---

## 📍 Geolocalización y domicilios

| Distancia | Tarifa ejemplo (COP) |
|-----------|----------------------|
| 0 – 3 km | $3.000 |
| 3 – 5 km | $5.000 |
| Más de 5 km | Tarifa personalizada |

*Reglas de negocio configurables en capa application/infrastructure.*

---

## 🗄️ Base de datos

### Implementado

| Tabla | Campos principales |
|-------|-------------------|
| `productos` | id, nombre, descripcion, precio, foto |
| `trabajadores` | id, nombre, descripcion, documento, email, rol, foto |

### Modelo objetivo (roadmap)

`Users`, `Carts`, `CartItems`, `Orders`, `OrderItems`, `DeliveryRates`, …

### Configuración

Copia `.env.example` a `.env`:

```env
# Desarrollo (por defecto): SQLite en panaderia.db
# DATABASE_URL=sqlite:///./panaderia.db

# Producción
# DATABASE_URL=postgresql+psycopg2://usuario:password@host:5432/panaderia
```

> `panaderia.db` está en `.gitignore` y no se versiona.

---

## 🚀 Instalación y ejecución

### Requisitos

- Python 3.11 o superior
- Git

### Pasos

```powershell
# Clonar e ingresar al proyecto
cd PanaderíaProjectBackEnd

# Entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Dependencias
python -m pip install -r requirements.txt

# Variables de entorno (opcional)
copy .env.example .env

# Arrancar API (desde la raíz del proyecto, no desde app/)
python -m uvicorn app.main:app --reload
```

### Documentación interactiva

| Herramienta | URL |
|-------------|-----|
| **Swagger UI** | http://127.0.0.1:8000/docs |
| **ReDoc** | http://127.0.0.1:8000/redoc |
| **OpenAPI JSON** | http://127.0.0.1:8000/openapi.json |

---

## 🌟 Competencias que demuestra el proyecto

- Desarrollo backend con **FastAPI**
- **Clean Architecture** y inversión de dependencias
- **SQLAlchemy** y diseño relacional
- Procesamiento de **Excel** con **Pandas**
- Integración con **Angular** y **n8n**
- Diseño de **APIs REST** documentadas con OpenAPI
- Geolocalización y automatización empresarial *(roadmap)*

---

## 📈 Escalabilidad futura

- [ ] Docker y docker-compose
- [ ] Carrito y pedidos
- [ ] Webhooks n8n
- [ ] Cálculo de domicilios y mapas
- [ ] Autenticación JWT
- [ ] Pasarela de pagos
- [ ] Panel administrativo e inventario
- [ ] Facturación electrónica
- [ ] Atención al cliente con IA

---

## 📄 Licencia

Proyecto académico / portafolio — Panadería Zapatoca.

---

<p align="center">
  <strong>🥖 Hecho con FastAPI y arquitectura limpia</strong>
</p>
