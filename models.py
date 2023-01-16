import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey

# Database path. Eg: postgresql://postgres:postgres@192.168.20.154:5432/casting_agency
database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()
migrate = Migrate()


def setup_db(app, db_path=database_path):
    """Binds a Flask application and a SQLAlchemy service."""
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path or database_path
    db.app = app
    db.init_app(app)
    # NOTE: render doesn't support shell access on free tier.
    # To get around not being able to run flask db init, migrate, upgrade.
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
    casting = db.relationship('Casting', backref='movie')

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
    casting = db.relationship('Casting', backref='actor')

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


class Casting(db.Model):

    __tablename__ = 'casting'
    __table_args__ = (
        db.UniqueConstraint('movie_id', 'actor_id', name='unique_casting'),
    )

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    actor_id = Column(Integer, ForeignKey('actor.id', ondelete='CASCADE'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id})'

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id
        }
