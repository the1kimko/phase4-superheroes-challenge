
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, CheckConstraint
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    serialize_rules = ("-hero_powers.hero",)

    def __repr__(self):
        return f"<Hero {self.name}, {self.super_name}>"

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    serialize_rules = ("-hero_powers.power",)

    # Validation for description length (must be at least 20 characters)
    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description

    def __repr__(self):
        return f"<Power {self.name}, {self.description}>"


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    serialize_rules = ("-hero.hero_powers", "-power.hero_powers")

    # Add a CheckConstraint to enforce strength values
    __table_args__ = (
        CheckConstraint("strength IN ('Strong', 'Weak', 'Average')", name='strength_check'),
    )

    # Validation for strength
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of: 'Strong', 'Weak', 'Average'")
        return strength

    def __repr__(self):
        return f"<HeroPower ({self.id}) of {self.hero}: {self.strength}>"
