from datetime import datetime, timedelta

from flask import (
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    session,
)

from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_jwt,
)

from werkzeug.security import generate_password_hash, check_password_hash


from flask import render_template, request, jsonify
from app import app, db, jwt
from models.models import Usuario, Post, Comentario, Categoria
from schemas.schema import UsuarioSchema, PostSchema, ComentarioSchema, CategoriaSchema
from flask.views import MethodView


# Crear instancias de los esquemas de Marshmallow
def allData():
    data = {
        "posts": Post.query.all(),
        "users": Usuario.query.all(),
        "comments": Comentario.query.all(),
        "categories": Categoria.query.all(),
    }
    return data


@app.context_processor
def categorias_disponibles():
    categorias = Categoria.query.all()
    return dict(categorias=categorias)


@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route("/inicio_sesion")
def inicio_sesion():
    return render_template(("login.html"))


@app.route("/login", methods=["POST"])
def login():
    nombre_ususario = request.form["usuario"]
    contraseña_ususario = request.form["contraseña"]

    usuario = Usuario.query.filter_by(nombre=nombre_ususario).first()

    if usuario and check_password_hash(usuario.password_hash, contraseña_ususario):
        access_token = create_access_token(
            identity=usuario.nombre,
            expires_delta=timedelta(seconds=30),
            additional_claims={"id_user": usuario.id},
        )

        session["userID"] = usuario.id

        return redirect(url_for("/"))

    return render_template("/agregar_usuario.html")


@app.route("/registro")
def registro():
    return render_template(("registro.html"))


@app.route("/agregar_usuario", methods=["POST"])
def agregar_usuario():
    # Recibo desde el front lo que viene en el input name="nombre"
    nombre_usuario = request.form["usuario"]
    correo_ususario = request.form["correo"]
    contraseña_ususario = request.form["contraseña"]

    passwordHash = generate_password_hash(
        contraseña_ususario, method="pbkdf2", salt_length=16
    )

    newUser = Usuario(
        nombre=nombre_usuario,
        password_hash=passwordHash,
        correo_electronico=correo_ususario,
    )

    db.session.add(newUser)
    db.session.commit()

    return render_template(
        "index.html",
    )


@app.route("/crear_post")
def crear_post():
    usuarios = Usuario.query.all()
    return render_template("crear_posteo.html", usuarios=usuarios)


@app.route("/agregar_post", methods=["POST"])
def agregar_post():
    # Recibo desde el front lo que viene en el input name="nombre"
    data = allData()
    titulo_post = request.form["titulo"]
    posteo_post = request.form["posteo"]
    categoria_id = request.form["categoria"]
    usuario_posteado = session["userID"]

    # Instanciar el modelo Post
    post = Post(
        titulo=titulo_post,
        posteo=posteo_post,
        id_categoria=categoria_id,
        usuario_posteado=usuario_posteado,
    )
    # # Preparo el objeto para enviarlo a DB
    db.session.add(post)
    # Almaceno el objeto
    db.session.commit()

    return redirect(
        "createPost.html",
    )


@app.route("/comentario/<int:id_post>")
def mostrar_comentarios(id_post):
    data = Comentario.query.all()
    comentarios = [comentario for comentario in data if comentario.id_post == id_post]
    return render_template("comentarios.html", comentarios=comentarios, id_post=id_post)


@app.route("/form_comentario/<int:id_post>")
def form_comentario(id_post):
    usuarios = Usuario.query.all()
    id_post = id_post
    return render_template(
        "agregar_comentario.html", usuarios=usuarios, id_post=id_post
    )


@app.route("/agregar_comentario", methods=["POST"])
def agregar_comentario():
    # Recibo desde el front lo que viene en el input name="nombre"
    texto_comen = request.form["comentario"]
    fecha_coment = request.form["fecha"]
    usuario_id = request.form["usuario"]
    id_post = request.form["post_id"]

    # Instanciar el modelo Post
    comentario = Comentario(
        texto=texto_comen, fecha=fecha_coment, autor=usuario_id, id_post=id_post
    )

    # # Preparo el objeto para enviarlo a DB
    db.session.add(comentario)
    # Almaceno el objeto
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/ver_posteo/<int:id_post>")
def ver_posteo(id_post):
    post = Post.query.get(id_post)  # traer un posteo por su id
    return render_template("ver_posteo.html", post=post)


# Crea una instancia del esquema de Marshmallow
usuario_schema = UsuarioSchema()


class UserView(MethodView):
    def get(self, id_user):
        if id_user is None:
            users = Usuario.query.all()
            users_data = [usuario_schema.dump(user) for user in users]
            return jsonify(users_data)
        else:
            user = Usuario.query.get(id_user)
            if not user:
                return jsonify(error="Usuario no encontrado"), 404
            user_data = usuario_schema.dump(user)
            return jsonify(user_data)

    def post(self):
        data = request.get_json()
        username = data.get("nombre")
        email = data.get("correo_electronico")
        password = data.get("password_hash")

        new_user = Usuario(
            nombre=username, correo_electronico=email, password_hash=password
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify(MENSAJE=f"Se creó el usuario {username}"), 201

    def put(self, id_user):
        user = Usuario.query.get(id_user)
        if not user:
            return jsonify(error="Usuario no encontrado"), 404

        data = request.get_json()
        nuevo_nombre_de_usuario = data.get("nombre")

        user.nombre = nuevo_nombre_de_usuario
        db.session.commit()
        user_data = usuario_schema.dump(user)
        return jsonify(user_data)

    def delete(self, id_user):
        user = Usuario.query.get(id_user)
        if not user:
            return jsonify(error="Usuario no encontrado"), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify(Mensaje=f"Usuario {id_user} eliminado")


# Agrega la vista a la aplicación con la ruta correspondiente
app.add_url_rule("/user", view_func=UserView.as_view("user"))
app.add_url_rule("/user/<id_user>", view_func=UserView.as_view("userById"))



class PostView(MethodView):
    def post(self):
        data = request.get_json()
        title = data.get("title")
        content = data.get("content")
        user_id = data.get("user_id")

        new_post = Post(title=title, content=content, user=user_id)
        db.session.add(new_post)
        db.session.commit()

        return jsonify(Mensaje="Nuevo post creado")

    def get(self):
        posts = Post.query.all()
        posts_schema = PostSchema.dump(posts, many=True)
        return jsonify(posts_schema)


# Agrega la vista a la aplicación con la ruta correspondiente
app.add_url_rule("/post", view_func=PostView.as_view("post"))


class ComentarioView(MethodView):
    def get(self, comentario_id):
        if comentario_id is None:
            # Devuelve una lista de todos los comentarios
            comentarios = Comentario.query.all()
            comentarios_schema = ComentarioSchema(many=True)
            return jsonify(comentarios_schema.dump(comentarios))
        else:
            # Devuelve un comentario específico por su ID
            comentario = Comentario.query.get(comentario_id)
            if comentario:
                comentario_schema = ComentarioSchema()
                return jsonify(comentario_schema.dump(comentario))
            return jsonify({"message": "Comentario no encontrado"}), 404

    def post(self):
        data = request.get_json()
        nuevo_comentario = Comentario(
            texto=data["texto"],
            fecha=data["fecha"],
            autor=data["autor"],
            id_post=data["id_post"],
        )
        db.session.add(nuevo_comentario)
        db.session.commit()
        return jsonify({"message": "Comentario creado con éxito"}), 201

    def put(self, comentario_id):
        comentario = Comentario.query.get(comentario_id)
        if comentario:
            data = request.get_json()
            comentario.texto = data.get("texto", comentario.texto)
            comentario.fecha = data.get("fecha", comentario.fecha)
            comentario.autor = data.get("autor", comentario.autor)
            comentario.id_post = data.get("id_post", comentario.id_post)
            db.session.commit()
            return jsonify({"message": "Comentario actualizado con éxito"})
        return jsonify({"message": "Comentario no encontrado"}), 404

    def delete(self, comentario_id):
        comentario = Comentario.query.get(comentario_id)
        if comentario:
            db.session.delete(comentario)
            db.session.commit()
            return jsonify({"message": "Comentario eliminado con éxito"})
        return jsonify({"message": "Comentario no encontrado"}), 404
    

app.add_url_rule("/comentario", view_func=ComentarioView.as_view("comentario"))
app.add_url_rule("/user/<id_post>", view_func=ComentarioView.as_view("postById"))


class CategoriaView(MethodView):
    def get(self, categoria_id):
        if categoria_id is None:
            # Devuelve una lista de todas las categorías
            categorias = Categoria.query.all()
            categorias_schema = CategoriaSchema(many=True)
            return jsonify(categorias_schema.dump(categorias))
        else:
            # Devuelve una categoría específica por su ID
            categoria = Categoria.query.get(categoria_id)
            if categoria:
                categoria_schema = CategoriaSchema()
                return jsonify(categoria_schema.dump(categoria))
            return jsonify({"message": "Categoría no encontrada"}), 404

    def post(self):
        data = request.get_json()
        nueva_categoria = Categoria(nombreCategoria=data["nombreCategoria"])
        db.session.add(nueva_categoria)
        db.session.commit()
        return jsonify({"message": "Categoría creada con éxito"}), 201

    def put(self, categoria_id):
        categoria = Categoria.query.get(categoria_id)
        if categoria:
            data = request.get_json()
            categoria.nombreCategoria = data.get(
                "nombreCategoria", categoria.nombreCategoria
            )
            db.session.commit()
            return jsonify({"message": "Categoría actualizada con éxito"})
        return jsonify({"message": "Categoría no encontrada"}), 301

    def delete(self, categoria_id):
        categoria = Categoria.query.get(categoria_id)
        if categoria:
            db.session.delete(categoria)
            db.session.commit()
            return jsonify({"message": "Categoría eliminada con éxito"})
        return jsonify({"message": "Categoría no encontrada"}), 301

app.add_url_rule("/categoria", view_func=CategoriaView.as_view("categorias"))
