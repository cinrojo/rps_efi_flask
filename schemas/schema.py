from marshmallow import fields
from flask import jsonify
from app import app, ma, db
from models.models import Usuario, Post, Comentario, Categoria


class UsuarioSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String()
    correo_electronico = fields.String()
    password_hash = fields.String()


class ComentarioSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    texto = fields.String()
    fecha = fields.Date()
    autor = fields.Integer()
    id_post = fields.Integer()


class CategoriaSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    nombreCategoria = fields.String()


class PostSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    titulo = fields.String()
    posteo = fields.String()
    usuario_posteado = fields.Integer()
    id_categoria = fields.Integer()
    autor = fields.Nested(UsuarioSchema)  # Anidamos UsuarioSchema
    comentarios = fields.Nested(
        ComentarioSchema, many=True
    )  # Anidamos ComentarioSchema
    categoria = fields.Nested(CategoriaSchema)  # Anidamos CategoriaSchema
