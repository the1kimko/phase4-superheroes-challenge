from app import app, db
from models import Hero, Power, HeroPower

# This file allows you to run tests or interact with the models manually

if __name__ == '__main__':
    with app.app_context():
        # Drop all existing tables (for resetting the database during debugging)
        db.drop_all()
        print("Dropped all tables.")

        # Create all tables (reinitialize the database schema)
        db.create_all()
        print("Created all tables.")

        # Seed some initial data for testing/debugging
        hero1 = Hero(name="Kamala Khan", super_name="Ms. Marvel")
        hero2 = Hero(name="Gwen Stacy", super_name="Spider-Gwen")

        power1 = Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed")
        power2 = Power(name="super strength", description="gives the wielder super-human strengths")

        db.session.add_all([hero1, hero2, power1, power2])
        db.session.commit()
        print("Added initial heroes and powers.")

        # Associate heroes and powers with HeroPower
        hero_power1 = HeroPower(strength="Strong", hero_id=hero1.id, power_id=power1.id)
        hero_power2 = HeroPower(strength="Average", hero_id=hero2.id, power_id=power2.id)

        db.session.add_all([hero_power1, hero_power2])
        db.session.commit()
        print("Added hero powers.")

        # Fetch all heroes and print them for verification
        heroes = Hero.query.all()
        for hero in heroes:
            print(f"Hero: {hero.name}, Super Name: {hero.super_name}")
            for hp in hero.hero_powers:
                print(f" - Power: {hp.power.name}, Strength: {hp.strength}")
