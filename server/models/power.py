from models import db
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')

    serialize_rules = ("-hero_powers.power",)

    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description

    def __repr__(self):
        return f"<Power {self.name}, {self.description}>"
