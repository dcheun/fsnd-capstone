"""App Unit Tests

IMPORTANT: Tests require test database to be seeded with the supplied casting_agency.psql.
IMPORTANT: Set the following environment variables:
    - DATABASE_URL
        E.g.: postgresql://postgres:postgres@192.168.20.154:5432/casting_agency_test
    - TOKEN
        This must be a JWT token with permissions to everything such as that of
        an "Executive Producer".

E.g.:
    createdb -h <host> -U <username> casting_agency_test
    psql -h <host> -U <username> casting_agency_test < casting_agency.psql

"""
import os
import unittest
import json

from app import create_app
from models import Actor, Movie, Casting


class CastingAgencyTestCase(unittest.TestCase):

    """This class represents the casting_agency test case."""

    def setUp(self) -> None:
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        token = os.environ.get('TOKEN')
        self.headers = {'Content-Type': 'application/json'}
        if token:
            self.headers.update({
                'Authorization': f'Bearer {token}'
            })
        # This should match what is set on app.py
        self.ITEMS_PER_PAGE = 10

        self.new_movie = {
            'title': 'Spider-Man: Homecoming',
            'release_date': '2017-07-07'
        }

        self.new_actor = {
            'name': 'Tom Holland',
            'age': 26,
            'gender': 'M'
        }

    def tearDown(self) -> None:
        """Executed after each test"""
        pass

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'])

        # Clean up
        with self.app.app_context():
            Movie.query.filter(Movie.id == data['created_id']).one().delete()

    def test_400_create_movie_missing_fields(self):
        res = self.client().post('/movies', json={
            'title': 'Spider-Man: Homecoming'
        }, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertIn('Missing required', data.get('message'))

    def test_405_movie_creation_not_allowed(self):
        res = self.client().post('/movies/45', json=self.new_movie, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_get_paginated_movies(self):
        """
        NOTE: Seeded data contains records.
        NOTE: Assume ITEMS_PER_PAGE = 10
        """
        res = self.client().get('/movies', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'] > self.ITEMS_PER_PAGE)
        self.assertTrue(len(data['movies']) == self.ITEMS_PER_PAGE)

    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get('/movies?page=999', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        with self.app.app_context():
            # Create a test movie to delete.
            test_movie = Movie(**self.new_movie)
            test_movie.insert()
            test_id = test_movie.id

            res = self.client().delete(f'/movies/{test_id}', headers=self.headers)
            data = json.loads(res.data)

            movie = Movie.query.filter(Movie.id == test_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], test_id)
        self.assertEqual(movie, None)

    def test_422_if_deleting_non_existing_movies(self):
        res = self.client().delete('/movies/1000', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_movie_by_id(self):
        res = self.client().get('/movies/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 1)

    def test_get_movie_by_actor(self):
        """Tests both movie_by_actor and actor_by_movie."""
        actor_id = 1
        movie_res = self.client().get(f'/actors/{actor_id}/movies', headers=self.headers)
        movie_data = json.loads(movie_res.data)

        self.assertEqual(movie_res.status_code, 200)
        self.assertEqual(movie_data['success'], True)
        self.assertTrue(movie_data['movies'])

        movie_id = movie_data['movies'][0]['id']
        actor_res = self.client().get(f'/movies/{movie_id}/actors', headers=self.headers)
        actor_data = json.loads(actor_res.data)
        found_actor = [x for x in actor_data['actors'] if x['id'] == actor_id]

        self.assertEqual(actor_res.status_code, 200)
        self.assertEqual(actor_data['success'], True)
        self.assertTrue(actor_data['actors'])
        self.assertTrue(found_actor)

    def test_create_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'])

        # Clean up
        with self.app.app_context():
            Actor.query.filter(Actor.id == data['created_id']).one().delete()

    def test_400_create_actor_empty_fields(self):
        res = self.client().post('/actors', json={
            'name': 'Tom Cruise',
            'age': '',
            'gender': 'M'
        }, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertIn('cannot be empty', data.get('message'))

    def test_405_actor_creation_not_allowed(self):
        res = self.client().post('/actors/45', json=self.new_actor, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_get_paginated_actors(self):
        """
        NOTE: Seeded data contains records.
        NOTE: Assume ITEMS_PER_PAGE = 10
        """
        res = self.client().get('/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'] > self.ITEMS_PER_PAGE)
        self.assertTrue(len(data['actors']) == self.ITEMS_PER_PAGE)

    def test_delete_actor(self):
        with self.app.app_context():
            # Create a test actor to delete.
            test_actor = Actor(**self.new_actor)
            test_actor.insert()
            test_id = test_actor.id

            res = self.client().delete(f'/actors/{test_id}', headers=self.headers)
            data = json.loads(res.data)

            actor = Actor.query.filter(Actor.id == test_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], test_id)
        self.assertEqual(actor, None)

    def test_422_if_deleting_non_existing_actors(self):
        res = self.client().delete('/actors/1000', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_actor_by_id(self):
        res = self.client().get('/actors/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 1)

    def test_create_casting(self):
        movie_res = self.client().post('/movies', json=self.new_movie, headers=self.headers)
        movie_data = json.loads(movie_res.data)
        actor_res = self.client().post('/actors', json=self.new_actor, headers=self.headers)
        actor_data = json.loads(actor_res.data)
        casting_res = self.client().post('/castings', json={
            'movie_id': movie_data['created_id'],
            'actor_id': actor_data['created_id']
        }, headers=self.headers)
        casting_data = json.loads(casting_res.data)

        self.assertEqual(casting_res.status_code, 200)
        self.assertEqual(casting_data['success'], True)
        self.assertTrue(casting_data['created_id'])

        # Clean up
        with self.app.app_context():
            Casting.query.filter(Casting.id == casting_data['created_id']).one().delete()
            Actor.query.filter(Actor.id == actor_data['created_id']).one().delete()
            Movie.query.filter(Movie.id == movie_data['created_id']).one().delete()

    def test_integrity_error_casting(self):
        """Test create casting that already exists"""
        movie_res = self.client().post('/movies', json=self.new_movie, headers=self.headers)
        movie_data = json.loads(movie_res.data)
        actor_res = self.client().post('/actors', json=self.new_actor, headers=self.headers)
        actor_data = json.loads(actor_res.data)
        casting_res = self.client().post('/castings', json={
            'movie_id': movie_data['created_id'],
            'actor_id': actor_data['created_id']
        }, headers=self.headers)
        casting_data = json.loads(casting_res.data)
        casting_created_id = casting_data['created_id']
        casting_res = self.client().post('/castings', json={
            'movie_id': movie_data['created_id'],
            'actor_id': actor_data['created_id']
        }, headers=self.headers)
        casting_data = json.loads(casting_res.data)

        self.assertEqual(casting_res.status_code, 400)
        self.assertEqual(casting_data['success'], False)
        self.assertIn('already exists', casting_data['message'])

        # Clean up
        with self.app.app_context():
            Casting.query.filter(Casting.id == casting_created_id).one().delete()
            Actor.query.filter(Actor.id == actor_data['created_id']).one().delete()
            Movie.query.filter(Movie.id == movie_data['created_id']).one().delete()

    def test_delete_casting(self):
        with self.app.app_context():
            # Create a test casting to delete.
            test_movie = Movie(**self.new_movie)
            test_movie.insert()
            test_movie_id = test_movie.id
            test_actor = Actor(**self.new_actor)
            test_actor.insert()
            test_actor_id = test_actor.id
            test_casting = Casting(movie_id=test_movie_id, actor_id=test_actor_id)
            test_casting.insert()
            test_casting_id = test_casting.id
            res = self.client().delete(f'/castings/{test_casting_id}', headers=self.headers)
            data = json.loads(res.data)

            casting = Casting.query.filter(Casting.id == test_casting_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], test_casting_id)
        self.assertEqual(casting, None)

        # Clean up
        with self.app.app_context():
            Movie.query.filter(Movie.id == test_movie_id).one().delete()
            Actor.query.filter(Actor.id == test_actor_id).one().delete()

    # TODO: Add RBAC Testing with different tokens


if __name__ == '__main__':
    unittest.main()
