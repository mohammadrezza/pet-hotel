from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from app.third_party.service import Mailer

mongo = PyMongo()
jwt = JWTManager()
bcrypt = Bcrypt()
mailer = Mailer()


def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "dev"])
    register_routes(app)
    mongo.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mailer.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
