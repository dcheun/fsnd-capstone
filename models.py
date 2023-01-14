import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, create_engine

# Database path. Eg: postgresql://postgres:postgres@192.168.20.154:5432/casting_agency
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()
migrate = Migrate()


def setup_db(app, db_path=database_path):
    """Binds a Flask application and a SQLAlchemy service."""
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate.init_app(app, db)


#################################################################################
# Models
#################################################################################

class Movie(db.Model):

    __tablename__ = 'movie'

    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Actor(db.Model):

    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String(1))

    def __int__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
