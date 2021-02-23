from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from . import models
from .views import main_views, auth_views
from .filter import format_datetime
from . import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)


    # 블루프린트
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터
    app.jinja_env.filters['datetime'] = format_datetime

    return app