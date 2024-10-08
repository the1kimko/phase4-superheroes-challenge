from flask import Blueprint, jsonify, request, make_response
from models import db, Hero, Power, HeroPower

import traceback

# Create a blueprint
routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the Superheroes API!"}), 200

@routes_bp.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    response = make_response(jsonify([hero.to_dict(only=("id", "name", "super_name")) for hero in heroes]), 200)
    return response

@routes_bp.route('/heroes/<int:id>', methods=['GET'])
def get_heroes_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'hero_powers': [
                {
                    'id': hp.id,
                    'hero_id': hp.hero_id,
                    'power_id': hp.power_id,
                    'strength': hp.strength,
                    'power': {
                        'id': hp.power.id,
                        'name': hp.power.name,
                        'description': hp.power.description
                    }
                } for hp in hero.hero_powers
            ]
        }
        response = make_response(jsonify(hero_data), 200)
    else:
        response = make_response(jsonify({'error': 'Hero not found'}), 404)
    return response

@routes_bp.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    response = make_response(jsonify([{
        "description": power.description,
        "id": power.id,
        "name": power.name
    } for power in powers]), 200)
    return response

@routes_bp.route('/powers/<int:id>', methods=['GET'])
def get_powers_by_id(id):
    power = Power.query.get(id)
    if power:
        # Serialize the power using to_dict()
        response = make_response(jsonify(power.to_dict(only=("id", "name", "description"))), 200)
    else:
        response = make_response(jsonify({'error': 'Power not found'}), 404)
    return response
    

@routes_bp.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return make_response(jsonify({'error': 'Power not found'}), 404)

    data = request.json
    description = data.get('description', '')

    # Validation: ensure description is at least 20 characters
    if len(description) < 20:
        return make_response(jsonify({'errors': ['Description must be at least 20 characters']}), 400)

    # Update the power's description
    power.description = description
    db.session.commit()

    # Return the updated power
    response = make_response(jsonify(power.to_dict(only=("id", "name", "description"))), 200)
    return response


@routes_bp.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.json
        strength = data.get('strength')
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')

        # Validation for strength
        if strength not in ['Strong', 'Weak', 'Average']:
            return make_response(jsonify({'errors': ['Strength must be Strong, Weak, or Average']}), 400)

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        # Validate that both the hero and power exist
        if not hero or not power:
            return make_response(jsonify({'errors': ['Hero or Power not found']}), 404)

        # Create the HeroPower association
        hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
        db.session.add(hero_power)
        db.session.commit()

        # Return the created HeroPower with nested hero and power information
        response = make_response(jsonify({
            "id": hero_power.id,
            "hero_id": hero.id,
            "power_id": power.id,
            "strength": hero_power.strength,
            "hero": {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            },
            "power": {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
        }), 201)
        
        return response
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error: {e}")
        traceback.print_exc()
        return make_response(jsonify({"error": "An unexpected error occurred."}), 500)
