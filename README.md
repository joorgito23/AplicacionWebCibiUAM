# CibiUAM - Manual del Desarrollador

Aplicación web desarrollada con Django, PostgreSQL y frontend basado en Node.js.

> Entorno de referencia: **Ubuntu 24.04.4 LTS**

---

## Índice

- [Instalación y Configuración Previa](#instalación-y-configuración-previa)
  - [Git](#git)
  - [PostgreSQL](#postgresql)
  - [Python y paquetes necesarios](#python-y-paquetes-necesarios)
  - [Migraciones y poblado de la base de datos](#migraciones-y-poblado-de-la-base-de-datos)
  - [Frontend](#frontend)
- [Ejecución de la aplicación](#ejecución-de-la-aplicación)
  - [Backend](#backend)
  - [Frontend](#frontend-1)
- [Comandos útiles](#comandos-útiles)
- [Métodos de pago](#métodos-de-pago)

---

## Instalación y Configuración Previa

Este manual describe el procedimiento necesario para la correcta instalación y ejecución de la aplicación **CibiUAM**.

Todas las instrucciones están orientadas al sistema operativo **Ubuntu 24.04.4 LTS**.

---

## Git

Para obtener el código fuente de la aplicación es necesario instalar Git.

### Instalación

```bash
sudo apt install git
```

### Clonar el repositorio

```bash
git clone https://github.com/joorgito23/AplicacionWebCibiUAM.git
cd AplicacionWebCibiUAM
```

---

## PostgreSQL

El sistema gestor de bases de datos utilizado por la aplicación es PostgreSQL.

---

### Instalación

Instalar PostgreSQL e iniciar su servicio:

```bash
sudo apt install postgresql
sudo systemctl enable postgresql
```

---

### Creación del superusuario

Acceder al usuario postgres:

```bash
sudo -i -u postgres psql
```

Crear usuario administrador:

```sql
CREATE USER alumnodb WITH SUPERUSER PASSWORD 'alumnodb';
```

Salir de PostgreSQL:

```sql
\q
```

Salir del usuario postgres:

```bash
exit
```

---

### Creación de la base de datos

Crear la base de datos asociada al usuario creado previamente:

```bash
createdb cibiuam -U alumnodb -h localhost
```

Configuración:

- Base de datos: `cibiuam`
- Host: `localhost`
- Puerto: `5432`

---

### Comandos útiles PostgreSQL

#### Acceder a la consola de la base de datos

```bash
psql cibiuam -U alumnodb -h localhost
```

#### Eliminar la base de datos

```bash
dropdb -U alumnodb -h localhost cibiuam
```

---

## Python y paquetes necesarios

La aplicación ha sido desarrollada utilizando:

- Python 3.11
- Django

Es necesario instalar Python, pip y configurar un entorno virtual.

---

### Instalación de Python

```bash
sudo apt update
sudo apt install python3
```

---

### Instalación de pip

```bash
sudo apt-get install python3-pip
```

---

### Entorno virtual

#### Instalar herramienta venv

```bash
sudo apt install python3.11-venv
```

#### Crear entorno virtual

```bash
python3 -m venv env
```

#### Activar entorno virtual

```bash
source env/bin/activate
```

#### Desactivar entorno virtual

```bash
deactivate
```

---

### Dependencias del proyecto

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

---

## Migraciones y poblado de la base de datos

> ⚠️ Todos estos comandos deben ejecutarse desde el directorio donde se encuentra `manage.py`

Crear migraciones:

```bash
python3 manage.py makemigrations
```

Aplicar migraciones:

```bash
python3 manage.py migrate
```

Poblar base de datos:

```bash
python3 populate.py
```

---

## Frontend

Para la correcta ejecución del cliente de la aplicación es necesario instalar sus dependencias mediante npm.

Se recomienda utilizar **Node.js 18 o superior**.

---

### Instalación de npm

```bash
sudo apt install npm
```

---

### Instalación de dependencias

Acceder al directorio del frontend:

```bash
cd frontend
```

Instalar dependencias:

```bash
npm install
```

---

# Ejecución de la aplicación

## Backend

El backend está desarrollado con Django y se ejecuta como API independiente.

---

### Activar entorno virtual

```bash
source env/bin/activate
```

---

### Iniciar servidor backend

```bash
python3 manage.py runserver
```

La API quedará disponible en:

```text
http://127.0.0.1:8000/
```

---

### Detener servidor backend

```text
Ctrl + C
```

Desactivar entorno virtual:

```bash
deactivate
```

---

## Frontend

### Iniciar servidor de desarrollo

Desde la carpeta frontend:

```bash
npm run dev
```

Este comando compila la aplicación y levanta el servidor local.

---

### Acceder a la aplicación

```text
http://localhost:5173/
```

---

### Detener servidor frontend

```text
Ctrl + C
```

---

## Comandos útiles

### Backend

Ejecutar servidor:

```bash
python3 manage.py runserver
```

Crear migraciones:

```bash
python3 manage.py makemigrations
```

Aplicar migraciones:

```bash
python3 manage.py migrate
```

Poblar base de datos:

```bash
python3 populate.py
```

---

### Frontend

Ejecutar app:

```bash
npm run dev
```

---

### PostgreSQL

Abrir consola:

```bash
psql cibiuam -U alumnodb -h localhost
```

Eliminar base de datos:

```bash
dropdb -U alumnodb -h localhost cibiuam
```

---

## Métodos de pago

La aplicación integra pagos mediante PayPal.

Se soportan dos métodos de pago:

- Pago mediante una cuenta de PayPal
- Pago mediante tarjeta bancaria a través de PayPal

---

### Pago con una cuenta de PayPal

Para realizar pagos utilizando una cuenta de PayPal, utilice la siguiente configuración:

**Cuenta PayPal:**

- Correo electrónico: sb-qmghw47958772@personal.example.com
- Contraseña: Xg;%-Tb3
- Teléfono móvil: 625580327

---

### Pago con tarjeta bancaria

PayPal permite realizar pagos con tarjeta.

#### Tarjeta 1

- Tipo: Mastercard
- Número: 5232105769361565
- Fecha de expiración: 04/2031
- CVC: 012

#### Tarjeta 2

- Tipo: Visa
- Número: 4020025763299562
- Fecha de expiración: 01/2031
- CVC: 123

---

## Configuración de PayPal en desarrollo

Para configurar PayPal en entorno de desarrollo:

Indicar en el archivo `settings.py` la siguiente información:

```bash
PAYPAL_CLIENT_ID=TU_CLIENT_ID
PAYPAL_SECRET=TU_CLIENT_SECRET
PAYPAL_MAIL=TU_MAIL
PAYPAL_BASE="https://api-m.sandbox.paypal.com"
```

Las credenciales sandbox se pueden configurar desde el panel de PayPal Developer.

---

## Stack tecnológico

- Backend: Django
- Base de datos: PostgreSQL
- Frontend: Node.js + npm
- Lenguaje: Python 3.11
- Pasarela de pago: PayPal

---

## Notas

- Ejecuta los comandos de backend desde la raíz del proyecto.
- Ejecuta los comandos de frontend desde la carpeta `frontend`.
- Mantén el entorno virtual activado durante el desarrollo.
- Asegúrate de tener PostgreSQL en ejecución antes de iniciar el backend.
- Configura correctamente las credenciales de PayPal antes de probar los pagos.
