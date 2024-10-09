from models import db
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    serialize_rules = ("-hero.hero_powers", "-power.hero_powers")

    __table_args__ = (
        CheckConstraint("strength IN ('Strong', 'Weak', 'Average')", name='strength_check'),
    )

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of: 'Strong', 'Weak', 'Average'")
        return strength

    def __repr__(self):
        return f"<HeroPower ({self.id}) of {self.hero.name}: {self.strength}>"
