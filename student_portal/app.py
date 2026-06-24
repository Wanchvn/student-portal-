import os

from flask import Flask

from config import Config
from models import db
from routes.api import api_bp
from routes.web import web_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(Config.DATABASE_DIR, exist_ok=True)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

    db.init_app(app)
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
