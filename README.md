# Casting Agency API

## Introduction

This project models a Casting Agency company that is responsible for creating movies and managing and assigning actors to those movies.

The API provides a secure RESTful service for interfacing with the backend resources.

## Overview

The following models are provided:

- `Movie` with attributes title and release date
- `Actor` with attributes name, age and gender
- `Casting` links an actor to a movie, and establishes a many-to-many relationship

The following roles are provided for access control:

- `Casting Assistant`
  - Can view actors and movies
- `Casting Director`
  - All permissions of a Casting Assistant and...
  - Add or delete an actor from the database
  - Modify actors or movies
- `Executive Producer`
  - All permissions of a Casting Director and...
  - Add or delete a movie from the database

For more information, please see the [API reference](docs/API.md) documentation.

### Deployed Cloud Environment

The API is currently hosted live on `render` at the following URL: `https://casting-agency.onrender.com/`

### Authentication & Authorization

Currently, there is no front-end for this project.

For testing the live hosted instance, a valid JWT can be provided by the author.

The Auth0 parameters are configurable via environment variables if you wish to use your own.

## Tech Stack (Dependencies)

- [Python 3](https://www.python.org/) - a high-level, general-purpose programming language.
- [Flask](http://flask.pocoo.org/) - a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) - the Python SQL toolkit and ORM used to handle the lightweight SQL database.
- [PostgreSQL](https://www.postgresql.org/) - a popular open source object-relational database system.

## Setting up the API and running development server locally

### Install Dependencies

- **Python 3** - Install the latest version of python for your platform. See [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
- **Virtual Environment** - Installing a virtual environment is recommended. This keeps your dependencies for each project separate and organized.
Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
E.g.:

```bash
python -m venv venv
source venv/bin/activate
```

- **PIP Dependencies** - Once the virtual environment is set up and running, install the required dependencies by running:

```bash
pip install -r requirements.txt
```


### Set up the Database

With PostgreSQL running, create a `casting_agency` database:

```bash
createdb casting_agency
```

Included is a PostgreSQL database dump with sample data that can be seeded to the database.
To use this file, run:

```bash
psql casting_agency < casting_agency.psql
```

### Environment Variables

Edit the `setup.sh` file and update the `DATABASE_URL` to your running database connection string.

Source the file:
```bash
source setup.sh
```

NOTE: If you are on a Windows system, you can set environment variables like so:

```bash
set DATABASE_URL=<DB_CONNECTION_STRING>
```

### Run the Server

To run the server, execute:

```bash
python app.py
```

## Testing

It is recommended to use a test database and seed the data for it.

E.g.:
```bash
createdb casting_agency_test
psql casting_agency_test < casting_agency.psql
```

Edit the `setup.sh` file and supply tokens for the 3 different role based JWT.

```bash
source setup.sh
```

To run test:

```bash
python test_app.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
