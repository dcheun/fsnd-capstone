# API Reference

## Getting Started
- Base URL: This app can be run and hosted locally. By default, it will be listening on `http://127.0.0.1:5000`.
- Authentication:
  - The API is protected using JWT and RBAC via Auth0.
  - Valid JWT bearer tokens are required with the correct permissions set.
  - At this time, you can only request a valid JWT from the author.

## Role-Based Access Control
There are `3` roles supported by the API with respective permissions, including:
- Casting Assistant
  - Can view actors and movies
- Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database

## Error Handling
Errors are returned as JSON objects in the following format:
```json
{
  "success": false,
  "error": 400,
  "message": "bad request"
}
```
There are `7` error types that can be returned from the API, including:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error
- 401: Unauthorized
- 403: Forbidden

## Endpoints
### GET /movies
- General:
  - Retrieves a list of movies.
  - Query Parameters:
    - `page` (int) - Results are paginated in groups of 10. Specify the page number, starting at 1.
  - Returns:
    - `success` - The success value.
    - `movies` - List of movie objects, paginated.
    - `total_movies` - The number of total movies.
- Required Permission: `get:movies`
- Sample: `curl http://127.0.0.1:5000/movies?page=1 --header "Authorization: Bearer <TOKEN>"`
```json
{
  "movies": [
    {
      "id": 23,
      "release_date": "Thu, 08 Sep 2022 00:00:00 GMT",
      "title": "Pinocchio"
    },
    {
      "id": 13,
      "release_date": "Fri, 17 Dec 2021 00:00:00 GMT",
      "title": "Spider-Man: No Way Home"
    },
    {
      "id": 19,
      "release_date": "Fri, 10 Jul 2020 00:00:00 GMT",
      "title": "Greyhound"
    },
    {
      "id": 29,
      "release_date": "Thu, 14 Dec 2017 00:00:00 GMT",
      "title": "The Post"
    },
    {
      "id": 32,
      "release_date": "Fri, 07 Jul 2017 00:00:00 GMT",
      "title": "Spider-Man: Homecoming"
    },
    {
      "id": 33,
      "release_date": "Fri, 07 Jul 2017 00:00:00 GMT",
      "title": "Spider-Man: Homecoming"
    },
    {
      "id": 20,
      "release_date": "Sat, 08 Oct 2016 00:00:00 GMT",
      "title": "Inferno"
    }
  ],
  "success": true,
  "total_movies": 34
}
```

### GET /actors
- General:
  - Retrieves a list of actors.
  - Query Parameters:
    - `page` (int) - Results are paginated in groups of 10. Specify the page number, starting at 1.
  - Returns:
    - `success` - The success value.
    - `actors` - List of actor objects, paginated.
    - `total_actors` - The number of total actors.
- Required Permission: `get:actors`
- Sample: `curl http://127.0.0.1:5000/actors?page=1 --header "Authorization: Bearer <TOKEN>"`
```json
{
    "actors": [
        {
            "age": 85,
            "gender": "M",
            "id": 1,
            "name": "Morgan Freeman"
        },
        {
            "age": 64,
            "gender": "M",
            "id": 2,
            "name": "Tim Robbins"
        },
        {
            "age": 80,
            "gender": "M",
            "id": 3,
            "name": "Marlon Brando"
        },
        {
            "age": 82,
            "gender": "M",
            "id": 4,
            "name": "Al Pacino"
        },
        {
            "age": 48,
            "gender": "M",
            "id": 5,
            "name": "Christian Bale"
        },
        {
            "age": 39,
            "gender": "M",
            "id": 6,
            "name": "Chris Hemsworth"
        },
        {
            "age": 68,
            "gender": "M",
            "id": 7,
            "name": "John Travolta"
        },
        {
            "age": 52,
            "gender": "F",
            "id": 8,
            "name": "Uma Thurman"
        },
        {
            "age": 70,
            "gender": "M",
            "id": 9,
            "name": "Liam Neeson"
        },
        {
            "age": 48,
            "gender": "M",
            "id": 10,
            "name": "Leonardo Dicaprio"
        }
    ],
    "success": true,
    "total_actors": 27
}
```

### GET /movies/<movie_id>
- General:
  - Retrieves a movie by id.
  - Returns:
    - `success` - The success value.
    - `movie` - Data of the movie object.
- Required Permission: `get:movies`
- Sample: `curl http://127.0.0.1:5000/movies/1 --header "Authorization: Bearer <TOKEN>"`
```json
{
    "movie": {
        "id": 1,
        "release_date": "Tue, 04 Oct 1994 00:00:00 GMT",
        "title": "The Shawshank Redemption"
    },
    "success": true
}
```

### GET /actors/<actor_id>
- General:
  - Retrieves an actor by id.
  - Returns:
    - `success` - The success value.
    - `actor` - Data of the actor object.
- Required Permission: `get:actors`
- Sample: `curl http://127.0.0.1:5000/actors/1 --header "Authorization: Bearer <TOKEN>"`
```json
{
    "actor": {
        "age": 85,
        "gender": "M",
        "id": 1,
        "name": "Morgan Freeman"
    },
    "success": true
}
```

### GET /actors/<actor_id>/movies
- General:
  - Retrieves a list of movies by actor casting.
  - Query Parameters:
    - `page` (int) - Results are paginated in groups of 10. Specify the page number, starting at 1.
  - Returns:
    - `success` - The success value.
    - `actor` - Data of the actor object.
    - `movies` - List of movie objects where actor was cast, paginated.
    - `total_movies` - The number of total movies where this actor was cast.
- Required Permission: `get:movies`
- Sample: `curl http://127.0.0.1:5000/actors/1/movies --header "Authorization: Bearer <TOKEN>"`
```json
{
    "actor": {
        "age": 85,
        "gender": "M",
        "id": 1,
        "name": "Morgan Freeman"
    },
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 04 Oct 1994 00:00:00 GMT",
            "title": "The Shawshank Redemption"
        }
    ],
    "success": true,
    "total_movies": 1
}
```

### GET /movies/<movie_id>/actors
- General:
  - Retrieves a list of actors who were cast to this movie id.
  - Query Parameters:
    - `page` (int) - Results are paginated in groups of 10. Specify the page number, starting at 1.
  - Returns:
    - `success` - The success value.
    - `movie` - Data of the movie object.
    - `actors` - List of actors who were cast to this movie id, paginated.
    - `total_actors` - The number of total actors on record casted to this movie.
- Required Permission: `get:actors`
- Sample: `curl http://127.0.0.1:5000/movies/1/actors --header "Authorization: Bearer <TOKEN>"`
```json
{
    "actors": [
        {
            "age": 85,
            "gender": "M",
            "id": 1,
            "name": "Morgan Freeman"
        },
        {
            "age": 64,
            "gender": "M",
            "id": 2,
            "name": "Tim Robbins"
        }
    ],
    "movie": {
        "id": 1,
        "release_date": "Tue, 04 Oct 1994 00:00:00 GMT",
        "title": "The Shawshank Redemption"
    },
    "success": true,
    "total_actors": 2
}
```

### POST /movies (Create)
- General:
  - Creates a new movie using the supplied fields.
  - Request Body:
    - `title` (str) - The title of the movie.
    - `release_date` (str) - The release date of the movie (E.g.: 1994-10-04).
  - Returns:
    - `success` - The success value.
    - `created_id` - id of the created resource.
- Required Permission: `post:movies`
- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json"
      --header "Authorization: Bearer <TOKEN>"
      --data '{"title": "Spider-Man: Homecoming", "release_date": "2017-06-28"}'`
```json
{
    "created_id": 46,
    "success": true
}
```

### POST /actors (Create)
- General:
  - Creates a new actor using the supplied fields.
  - Request Body:
    - `name` (str) - The name of the actor.
    - `age` (int) - The age of the actor.
    - `gender` (str) - The gender of the actor (M/F).
  - Returns:
    - `success` - The success value.
    - `created_id` - id of the created resource.
- Required Permission: `post:actors`
- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json"
      --header "Authorization: Bearer <TOKEN>"
      --data '{"name": "Tom Holland", "age": 28, "gender": "M"}'`
```json
{
    "created_id": 42,
    "success": true
}
```

### POST /castings (Create)
- General:
  - Casts an actor by id to movie by id.
  - Request Body:
    - `movie_id` (str) - The id of the movie to cast the actor to.
    - `actor_id` (int) - The id of the actor to cast.
  - Returns:
    - `success` - The success value.
    - `created_id` - id of the created resource.
- Required Permission: `post:castings`
- Sample: `curl http://127.0.0.1:5000/castings -X POST -H "Content-Type: application/json"
      --header "Authorization: Bearer <TOKEN>"
      --data '{"movie_id": 30, "actor_id": 22}'`
```json
{
    "created_id": 49,
    "success": true
}
```

### PATCH /movies/<movie_id> (Update)
- General:
  - Update a movie by id.
  - Request Body (supply at least one):
    - `title` (str) - The new title of the movie.
    - `release_date` (int) - The new release date of the movie.
  - Returns:
    - `success` - The success value.
    - `movie` - Data of the updated movie object.
- Required Permission: `patch:movies`
- Sample: `curl http://127.0.0.1:5000/movies/1 -X PATCH -H "Content-Type: application/json"
      --header "Authorization: Bearer <TOKEN>"
      --data '{"release_date": "1994-10-04"}'`
```json
{
    "movie": {
        "id": 1,
        "release_date": "Tue, 04 Oct 1994 00:00:00 GMT",
        "title": "The Shawshank Redemption"
    },
    "success": true
}
```

### PATCH /actors/<actor_id> (Update)
- General:
  - Update an actor by id.
  - Request Body (supply at least one):
    - `name` (str) - The new name of the actor.
    - `age` (int) - The new age of the actor.
    - `gender` (str) - The new gender of the actor.
  - Returns:
    - `success` - The success value.
    - `movie` - Data of the updated actor object.
- Required Permission: `patch:actors`
- Sample: `curl http://127.0.0.1:5000/movies/1 -X PATCH -H "Content-Type: application/json"
      --header "Authorization: Bearer <TOKEN>"
      --data '{"gender": "F"}'`
```json
{
    "actor": {
        "age": 52,
        "gender": "F",
        "id": 8,
        "name": "Uma Thurman"
    },
    "success": true
}
```

### DELETE /movies/<movie_id>
- General:
  - Deletes the movie of the given ID if it exists.
  - Returns:
    - `success` - The success value.
    - `deleted_id` - id of the deleted resource.
- Required Permission: `delete:movies`
- Sample: `curl -X DELETE http://127.0.0.1:5000/movies/47`
```json
{
    "deleted_id": 47,
    "success": true
}
```

### DELETE /actors/<actor_id>
- General:
  - Deletes the actor of the given ID if it exists.
  - Returns:
    - `success` - The success value.
    - `deleted_id` - id of the deleted resource.
- Required Permission: `delete:actors`
- Sample: `curl -X DELETE http://127.0.0.1:5000/actors/43`
```json
{
    "deleted_id": 43,
    "success": true
}
```

### DELETE /castings/<casting_id>
- General:
  - Deletes the casting of the given ID if it exists.
  - Returns:
    - `success` - The success value.
    - `deleted_id` - id of the deleted resource.
- Required Permission: `delete:castings`
- Sample: `curl -X DELETE http://127.0.0.1:5000/castings/49`
```json
{
    "deleted_id": 49,
    "success": true
}
```
