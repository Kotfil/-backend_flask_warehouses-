from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

from app.models import db, User
from app.routes.auth import auth_bp
from app.routes.warehouses import bp as warehouse_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'
    app.config['SWAGGER'] = {'title': 'Warehouse API', 'uiversion': 3}

    db.init_app(app)
    JWTManager(app)
    Swagger(app)


    app.register_blueprint(warehouse_bp)
    app.register_blueprint(auth_bp)

    return app


def create_fake_users():
    if not User.query.filter_by(username='admin').first():
        users = [
            User(username='admin', password_hash=generate_password_hash('admin111'), role='admin'),
            User(username='manager', password_hash=generate_password_hash('manager111'), role='manager'),
            User(username='user', password_hash=generate_password_hash('user111'), role='user')
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        create_fake_users()
    app.run(debug=True)
