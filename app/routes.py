from flask import Flask


def register_routes(app: Flask):
    from app.pet import create_bp as create_pet_bp
    from app.user import create_bp as create_user_bp

    app.register_blueprint(create_pet_bp())
    app.register_blueprint(create_user_bp())
