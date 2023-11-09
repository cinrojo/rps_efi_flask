# rps_efi_flask
## Docker y docker-compose

Con este comando van a borrar los volúmenes asociados al docker-compose del proyecto:

`docker-compose down -v `

Les dejo otro comando, por las dudas que no sea suficiente el anterior, que va a borrar **todas** las imágenes, contenedores y volúmenes que tengan, usenló con cuidado:

`docker system prune -a --volumes`


Una vez hecho eso, les recomiendo borrar los contenedores y reconstruir las imágenes.

Pueden correr:

`docker-compose build && docker-compose up`


Les recomiendo correrlo sin el `-d` al principio así pueden ver los logs más fácil en caso de que algo salga mal.

Luego de eso lo cancelan con `CTRL+C` y lo vuelven a levantar con `docker-compose up -d` o `docker-compose restart`. Luego para frenarlo, usan `docker-compose stop`

Presten **muchísima** atención a las variables de entorno y los valores que ponen. Yo les actualicé el .env.sample para que tengan de referencia. Ojo que les coincida con el `/init/create_schema.sql`, no llegué a configurar las variables de entorno.

   ##  Practico Segundo Semestre 

Descripción: Es aplicación web en Flask que incluye rutas para el inicio de sesión, registro, creación y visualización de publicaciones, comentarios y categorías. También se maneja la autenticación de usuarios y la interacción con la base de datos.


Tabla de Contenidos

-	Requisitos Previos
-	Instalación
-	Estructura del proyecto
-	Uso
-	Características
-	Autores

Requisitos Previos:

-	Python 3.x instalado.
-	MySQL instalado y configurado en 'mysql+pymysql://root@localhost/practico_python'.
-	Las bibliotecas Flask, Flask-Migrate y Flask-SQLAlchemy instaladas. Puedes instalarlas con 		
	pip install Flask Flask-Migrate Flask-SQLAlchemy.


* Instalación
Clona este repositorio en tu máquina local
git clone <git@github.com:cinrojo/efi_flask_docker.git>

Navega hasta el directorio del proyecto:
cd <efi_flask_docker>

Crea un entorno virtual e instala las dependencias:
python -m venv venv
source venv/bin/activate      # Para Linux / macOS
venv\Scripts\activate         # Para Windows
pip install -r requirements.txt

Configura la base de datos MySQL en app.config['SQLALCHEMY_DATABASE_URI'] para que coincida con tu configuración.

Ejecuta las migraciones para crear las tablas de la base de datos:

flask db init
flask db migrate
flask db upgrade

* Estructura del Proyecto
- app.py: El archivo principal de la aplicación Flask.
- templates/: Directorio que contiene las plantillas HTML (Jinja2).
- models.py: Define los modelos de la base de datos.
- schemas.py: Define los esquemas de Marshmallow para serialización de datos.
- Dockerfile: Configuración del contenedor de la aplicación.
- docker-compose.yml: Define la configuración de Docker Compose.


* Uso
Ejecuta la aplicación web:
docker run -d --name mi_contenedor NOMBRE_DE_LA_IMAGEN
flask run

Abre tu navegador web y ve a http://localhost:5000 para acceder a la aplicación.

Características

-	Registro de usuarios con nombre, correo electrónico y contraseña.
-	Publicación de posts con títulos, contenido y categorías.
-	Comentarios en los posts.
-	Clasificación de posts por categorías.
-	Visualización de detalles de un post específico.

Autor
	Nombres de los Autores: Cintia Rojo,Palacios Lautaro,Milton Storm.
	Contactos: correo electrónico de los autores:
    * c.rojo@itecriocuarto.org.ar 	 
	* l.palacios@itecriocuarto.org.ar
    * m.storm@itecriocuarto.org.ar
