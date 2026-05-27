import os
from flask import Flask
from .extensions import db
from .routes import bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)

    db_path = os.path.join(app.instance_path, 'library.db').replace('\\', '/')
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///' + db_path,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY='dev-secret-key',
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app