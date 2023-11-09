import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import timedelta
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv  # levanta las variables de entorno en el .env
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt,
    get_jwt_identity,
)


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

db = SQLAlchemy(app=app)
migrate = Migrate(app, db)
ma = Marshmallow(app=app)
jwt = JWTManager(app)
load_dotenv()
from views import view

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
