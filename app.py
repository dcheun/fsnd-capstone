import os
import sys

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from models import setup_db, Movie, Actor, Casting

ITEMS_PER_PAGE = 10


def paginate(_request, selection):
    page = _request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    records = [rec.format() for rec in selection]
    current_records = records[start:end]

    return current_records


def create_app(test_config=None):
    """Create and configures the app."""
    app = Flask(__name__)
    with app.app_context():
        setup_db(app)

    # Allow '*' for origins.
    CORS(app)

    # Use after_request decorator to set the Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/actors', methods=['GET'])
    def get_actors():
        selection = Actor.query.order_by(Actor.id).all()
        actors = paginate(request, selection)

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': actors,
            'total_actors': len(selection)
        })

    @app.route('/movies', methods=['GET'])
    def get_movies():
        selection = Movie.query.order_by(Movie.release_date.desc()).all()
        movies = paginate(request, selection)

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies,
            'total_movies': len(selection)
        })

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    def get_movie_by_id(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    def get_actor_by_id(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)

        return jsonify({
            'success': True,
            'movie': actor.format()
        })

    @app.route('/actors/<int:actor_id>/movies', methods=['GET'])
    def get_movies_by_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)

        selection = [x.movie for x in actor.casting]
        selection = sorted(selection, key=lambda x: x.release_date, reverse=True)
        movies = paginate(request, selection)

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format(),
            'movies': movies,
            'total_movies': len(selection)
        })

    @app.route('/movies/<int:movie_id>/actors', methods=['GET'])
    def get_actors_by_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404)

        selection = [x.actor for x in movie.casting]
        selection = sorted(selection, key=lambda x: x.id)
        actors = paginate(request, selection)

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format(),
            'actors': actors,
            'total_actors': len(actors)
        })

    @app.route('/actors', methods=['POST'])
    def create_actor():
        body = request.get_json()

        # Check for required fields.
        required_fields = {'name', 'age', 'gender'}
        missing_fields = required_fields.difference(body)
        if missing_fields:
            abort(400, f'Missing required actor fields(s): {", ".join(missing_fields)}')
        # Check for empty fields.
        empty_fields = set(x for x in body if not body.get(x))
        empty_required_fields = required_fields.intersection(empty_fields)
        if empty_required_fields:
            abort(400, f'Movie field(s) cannot be empty: {", ".join(empty_required_fields)}')

        try:
            actor = Actor(
                name=body.get('name'),
                age=body.get('age'),
                gender=body.get('gender')
            )
            actor.insert()
            return jsonify({
                'success': True,
                'created_id': actor.id
            })
        except Exception:
            abort(422)

    @app.route('/movies', methods=['POST'])
    def create_movie():
        body = request.get_json()

        # Check for required fields.
        required_fields = {'title', 'release_date'}
        missing_fields = required_fields.difference(body)
        if missing_fields:
            abort(400, f'Missing required movie field(s): {", ".join(missing_fields)}')
        # Check for empty fields.
        empty_fields = set(x for x in body if not body.get(x))
        empty_required_fields = required_fields.intersection(empty_fields)
        if empty_required_fields:
            abort(400, f'Movie field(s) cannot be empty: {", ".join(empty_required_fields)}')

        try:
            movie = Movie(
                title=body.get('title'),
                release_date=body.get('release_date')
            )
            movie.insert()
            return jsonify({
                'success': True,
                'created_id': movie.id
            })
        except Exception:
            abort(422)

    @app.route('/castings', methods=['POST'])
    def create_casting():
        body = request.get_json()

        # Check for required fields.
        required_fields = {'movie_id', 'actor_id'}
        missing_fields = required_fields.difference(body)
        if missing_fields:
            abort(400, f'Missing required cast field(s): {", ".join(missing_fields)}')
        # Check for empty fields.
        empty_fields = set(x for x in body if not body.get(x))
        empty_required_fields = required_fields.intersection(empty_fields)
        if empty_required_fields:
            abort(400, f'Cast field(s) cannot be empty: {", ".join(empty_required_fields)}')

        try:
            cast = Casting(
                movie_id=body.get('movie_id'),
                actor_id=body.get('actor_id')
            )
            cast.insert()
            return jsonify({
                'success': True,
                'created_id': cast.id
            })
        except IntegrityError:
            abort(400, f'Casting already exist')
        except Exception:
            print(sys.exc_info())
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def update_actor(actor_id):
        body = request.get_json()

        # Check for valid inputs.
        for field in ['name', 'age', 'gender']:
            if field in body and not body.get(field):
                abort(400, f'A value is required for field: {field}')

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            if 'name' in body:
                actor.name = body['name']
            if 'age' in body:
                actor.age = body['age']
            if 'gender' in body:
                actor.gender = body['gender']
            actor.update()

            return jsonify({
                'success': True,
                'actors': [actor.format()]
            })
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def update_movie(movie_id):
        body = request.get_json()

        # Check for valid inputs.
        for field in ['title', 'release_date']:
            if field in body and not body.get(field):
                abort(400, f'A value is required for field: {field}')

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        try:
            if 'title' in body:
                movie.title = body['title']
            if 'release_date' in body:
                movie.release_date = body['release_date']
            movie.update()

            return jsonify({
                'success': True,
                'movies': [movie.format()]
            })
        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actors(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()
            return jsonify({
                'success': True,
                'delete': actor_id
            })
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movies(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()
            return jsonify({
                'success': True,
                'delete': movie_id
            })
        except Exception:
            abort(422)

    @app.route('/castings/<int:casting_id>', methods=['DELETE'])
    def delete_casting(casting_id):
        casting = Casting.query.filter(Casting.id == casting_id).one_or_none()

        if casting is None:
            abort(404)

        try:
            casting.delete()
            return jsonify({
                'success': True,
                'delete': casting_id
            })
        except Exception:
            abort(422)

    #############################################################################
    # Error handlers
    #############################################################################
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': error.description or 'bad request'
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    #app.run()
