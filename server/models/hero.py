
from models import db
from sqlalchemy_serializer import SerializerMixin

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')

    serialize_rules = ("-hero_powers.hero",)

    def __repr__(self):
        return f"<Hero {self.name}, {self.super_name}>"
