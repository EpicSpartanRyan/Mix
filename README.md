# Distributed AI of Things (AIoT) - Production Stack

<div align="center">
  
<img width="1159" height="1603" alt="image" src="https://github.com/user-attachments/assets/9cf920b1-e2fa-4b3d-92fc-a1d0f992edbb" />
<img width="1159" height="1251" alt="image" src="https://github.com/user-attachments/assets/52466eda-5672-4163-8873-d02664a01632" />

</div>

Un stack tecnológico de alto rendimiento diseñado para aplicaciones de inteligencia artificial en tiempo real, distribuidas e infinitamente escalables en la nube, conectadas directamente al mundo físico mediante millones o billones de dispositivos del Internet Industrial de las Cosas (IIoT).

---

## 🏗️ Arquitectura del Sistema

<div align="center">

<img width="811" height="1777" alt="image" src="https://github.com/user-attachments/assets/26810404-8e49-4f75-992f-8301f6855b6a" />


</div>

La arquitectura desacopla la ingesta masiva de dispositivos físicos y la procesa a través de una tubería optimizada de alto rendimiento:

* **Ingesta y Conectividad Edge:** **EMQX** actúa como el broker y sistema de mensajería IoT central, soportando millones de conexiones simultáneas mediante formatos como JSON y Protobuf con baja latencia.
* **Orquestación y Caché:** **Dragonfly** funge como la columna vertebral de caché ultrarrápida y cola de mensajes para la coordinación de múltiples *workers*.
* **Procesamiento Distribuido:** **Celery** desacopla las tareas pesadas ejecutando cargas de trabajo en paralelo con **PyTorch**, **CuPy**, **Polars** y **DuckDB**.
* **Persistencias Especializadas:** 
  * **OceanBase:** Base de datos NewSQL distribuida para almacenamiento transaccional y analítico híbrido (HTAP).
  * **Milvus:** Motor vectorial optimizado para búsqueda híbrida, multimodal y cargas de IA.
* **Capa de Aplicación:** **FastAPI** expone servicios REST, gRPC y WebSockets de altísimo rendimiento con soporte nativo para corrutinas (*asyncio*).

---

## 🛠️ Componentes y Tecnologías Clave

* **Gestión de Dependencias con `uv`**: Migrado completamente al gestor ultrarrápido `uv` para una resolución de dependencias óptima y tiempos de compilación mínimos.
* **Entorno de Desarrollo (Devcontainer)**: Configurado nativamente mediante `docker-compose.yml` para garantizar paridad absoluta entre entornos locales y de producción, integrando una consola **tmux** autoacoplada al iniciar el contenedor.
* **Automatización con Dependabot**: Configurado para gestionar hasta 20 pull requests concurrentes con escaneos programados a las 12:00 UTC (06:00 AM CDMX).
* **Gestión de Base de Datos y Migraciones**: Implementación de **SQLModel** como ORM moderno basado en Pydantic y SQLAlchemy, acompañado de **Alembic** para el control de versiones y migraciones de esquemas.
* **Monitoreo y Visualización de Contenedores**: Incluye **DockGraph** para graficar en tiempo real las relaciones, estado y métricas de todos los servicios del stack.

---
