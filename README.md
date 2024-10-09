# Superheroes API

This project implements a simple API for managing heroes, powers, and their relationships using Flask, SQLAlchemy, and Flask-Migrate.

## Features

- Create and manage **Heroes**.
- Create and manage **Powers**.
- Create **HeroPower** relationships to assign powers with varying strengths to heroes.
- Comprehensive error handling and validation.

## Project Structure

- `app.py`: Main Flask app configuration and routes initialization.
- `models.py`: SQLAlchemy models for Hero, Power, and HeroPower.
- `routes.py`: API routes for creating and managing heroes, powers, and relationships.
- `seed.py`: Script for seeding the database with sample data.
- `debug.py`: Script for debugging database models and relationships.
- `migrations/`: Database migrations managed via Flask-Migrate.

## Endpoints

1. **GET /heroes**: Fetch all heroes.
2. **GET /heroes/:id**: Fetch a hero by their ID.
3. **GET /powers**: Fetch all powers.
4. **GET /powers/:id**: Fetch a power by its ID.
5. **PATCH /powers/:id**: Update a power's description.
6. **POST /hero_powers**: Assign a power to a hero with a specific strength.

### Example API Request

#### Creating a HeroPower

```bash
curl -X POST http://127.0.0.1:5555/hero_powers \
-H "Content-Type: application/json" \
-d '{
    "strength": "Average",
    "power_id": 1,
    "hero_id": 3
}'
```

## Requirements
Below are the main dependencies required for this project. These are included in the `Pipfile` or `requirements.txt`.

### Installed Dependencies
- Flask: Lightweight web framework for Python.
- Flask-SQLAlchemy: Adds SQLAlchemy support for Flask.
- Flask-Migrate: Adds database migrations using Alembic.
- SQLAlchemy-Serializer: Adds easy model serialization support to SQLAlchemy.
- Faker: Can be used for generating fake data (for seeding/testing).

## Installation
To set up this project locally, follow these steps:

1. Clone the repository:

```bash
git clone <your-repo-url>
cd your-project-directory
```

2. Set up a virtual environment:

If you don’t have pipenv installed, first install it:

```bash
pip install pipenv
```

Using pipenv:

```bash
pipenv install
pipenv shell
```
Alternatively, using virtualenv:

```bash
python3 -m venv env
source env/bin/activate
```

3. Install dependencies:

The `pipenv install` installed all packages listen in the `[packages]` section of the `Pipfile`

4. Run database migrations:

Initialize and run migrations:

```bash
flask db init
flask db migrate -m "message"
flask db upgrade head
```

5. Seed the database:

Run the `seed.py` file to populate the database with sample data:

```bash
python seed.py
```

6. Run the application:

Before starting development server, esnure you had run these commands from the `server` directory:

```bash
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
```

Then, start the Flask development server:

```bash
python app.py
```

- The API will be available at http://127.0.0.1:5555/.

## Development Tools
- Postman or curl: To test your API routes.

## Debugging
If you want to debug the models or database relationships, run the `debug.py` script:

```bash
python debug.py
```

This will reset the database, create tables, and seed some initial data for testing.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
