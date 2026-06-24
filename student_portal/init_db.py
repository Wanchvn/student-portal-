"""Initialize the Student Portal database."""

from app import create_app
from models import db


def init_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        print('Database initialized successfully.')
        print(f'Database location: {app.config["SQLALCHEMY_DATABASE_URI"]}')


if __name__ == '__main__':
    init_database()
