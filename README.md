![Inove banner](inove.jpg)
Inove Escuela de Código\
info@inove.com.ar\
Web: [Inove](http://inove.com.ar)

---

# Django - REST FRAMEWORK Autenticación
En este repositorio encontrarán los siguientes archivos:

__Ejemplos que el profesor mostrará en clase__\

* **dockerfile** (Para generar la imagen de Docker)
* **docker-compose.yml** (Para configurar el contenedor de Docker)
* **requirements.txt** (Que contiene las librerías que vamos a estar usando)
* **/marvel** (Directorio raíz de nuestra aplicación)
* **/database** (Directorio de nuestra base de datos)

---

# Comandos útiles 🐋

### 1. Correr el proyecto
Siempre en el mismo directorio del archivo *docker-compose.yml*
**$** `docker-compose up`

### 2. Correr la línea de comandos dentro del contenedor

**$** `docker exec -i -t modulo_4b bash`

Nos va a devolver a nuestra consola, una consola dentro del contenedor de software.


Una vez dentro ejecutamos el comando:

**$** `cd /opt/back_end/marvel` 

### 3. Iniciar el servidor
(Siempre dentro de nuestro contenedor de software - Comando N°2)  
Tenemos que ir a la carpeta donde se encuentra el archivo *manage.py*  

**$** `python manage.py runserver 0.0.0.0:8000`  

### 4. Ejecutar los siguientes comandos para realizar la primera migración:  

**$** `python manage.py makemigrations`

**$** `python manage.py migrate`

#### NOTA: Si se quiere sólo realizar las migracions correspondiente a una determinada aplicación del proyecto, podemos ejecutar los siguientes comandos:  

**$** `python manage.py makemigrations nombre_aplicación`

  - Ejemplo: **$** `python manage.py makemigrations e_commerce`

**$** `python manage.py migrate nombre_aplicación` 

  - Ejemplo: **$** `python manage.py migrate e_commerce`

### 5. Creamos un super usuario:  

**$** `python manage.py createsuperuser`

### 6. Detener la ejecución de nuestro contenedor y nuestro servidor
Tenemos que estar en la terminal que nos muestra los mensajes del servidor, tomada por el contenedor.
Tan solo con el comando `ctrl + c`  se detiene la ejecución de nuestro contenedor.  

Una forma alternativa es con el siguiente comando en la terminal del host:

**$** `docker stop modulo_4b`  

O también puede ser con docker-compose:
Tenemos que estar en la carpeta que contiene el archivo *docker-compose.yml* y hacer:


**$** `docker-compose down`  

---
# Consultas
alumnos@inove.com.ar
