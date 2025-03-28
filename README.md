
# Proyecto FastAPI

Este es un proyecto de FastAPI. Puedes correrlo en tu entorno utilizando Docker con el siguiente comando:

```bash
docker-compose up --build
```

El servidor de desarrollo se iniciará en `http://localhost:8000`.

## Requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

## Instalación

### 1. Clona el repositorio

```bash
git clone [<URL del repositorio>](https://github.com/Mario991012/seek-todo-list-backend.git)
cd seek-todo-list-backend
```

### 2. Instalación de dependencias

No es necesario instalar dependencias manualmente. Docker se encargará de construir la imagen y instalar todas las dependencias necesarias.

## Ejecución

Para iniciar el servidor de FastAPI y su base de datos MongoDB local, usa el siguiente comando:

```bash
docker-compose up --build
```

Esto levantará dos contenedores:

1. **FastAPI** en `http://localhost:8000`
2. **MongoDB** en un contenedor local

### Detener el entorno

Para detener los contenedores, usa el siguiente comando:

```bash
docker-compose down
```

## MongoDB Local

El proyecto está configurado para usar una base de datos **MongoDB local** que se encuentra dentro del contenedor. Los datos de MongoDB se persistirán en el contenedor mientras esté en ejecución.

## Notas

- Si deseas cambiar el puerto, puedes editar la configuración en el archivo `docker-compose.yml`.
- Asegúrate de que Docker y Docker Compose estén instalados correctamente en tu máquina para poder levantar el proyecto.
