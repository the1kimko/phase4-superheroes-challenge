from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db  # Import db from models.py
from routes import routes_bp  # Import the Blueprint from routes.py

# Initialize the Flask app
app = Flask(__name__)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Register the routes blueprint
app.register_blueprint(routes_bp)

# Run the app
if __name__ == '__main__':
    app.run(port=5555, debug=True)
