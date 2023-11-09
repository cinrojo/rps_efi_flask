from sqlalchemy import ForeignKey
from app import db


class Usuario(db.Model):
    _tablename_ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo_electronico = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)


class Post(db.Model):
    _tablename_ = "post"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    posteo = db.Column(db.String(300), nullable=False)
    usuario_posteado = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    id_categoria = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    # Definir las relaciones con Usuario y Categoria
    usuario = db.relationship(
        "Usuario", foreign_keys=[usuario_posteado], backref="posts"
    )
    categoria = db.relationship(
        "Categoria", foreign_keys=[id_categoria], backref="posts"
    )

    # Definir la relación con Comentario con cascade para eliminar comentarios relacionados
    comentarios_relacionados = db.relationship(
        "Comentario", backref="post_relacionado", cascade="all, delete-orphan"
    )


class Comentario(db.Model):
    _tablename_ = "comentario"
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(300), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    autor = db.Column(
        db.Integer,  # tipo integer
        ForeignKey("usuario.id"),  # es la clave de la db
        nullable=False,  # no acpeptar falso
    )
    id_post = db.Column(
        db.Integer,  # tipo integer
        ForeignKey("post.id"),  # es la clave de la db
        nullable=False,  # no acpeptar falso
    )


class Categoria(db.Model):
    _tablename_ = "categoria"
    id = db.Column(db.Integer(), primary_key=True)
    nombreCategoria = db.Column(db.String(100), nullable=False)
