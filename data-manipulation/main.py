import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from models import Alliance, Country, Tank

if __name__ == "__main__":
    engine = db.create_engine("sqlite:///foo.db")

    Session = sessionmaker(bind=engine)

    session = Session()

    # Example how to add data to database.

    # Create tank
    # tank_example = Tank(name="f-18", quantity=100, country_id=1, origin_id=2)

    # Create country
    # country_1 = Country(name="Poland")
    # country_2 = Country(name="Germany")

    # Create Alliance
    # alliance_1 = Alliance(
    #     country1_id="1", country2_id="2", start_year=1900, end_year=2100
    # )

    # Add data to session and commit changes.
    # session.add(tank_example)
    # session.add(country_1)
    # session.add(country_2)
    # session.add(alliance_1)
    # session.commit()


    # Printing data.
    for instance in session.query(Tank).order_by(Tank.id):
        print(
            instance.name,
            instance.quantity,
            instance.country_id,
            instance.country,
            instance.origin,
        )

    print()
    for instance in session.query(Country).order_by(Country.id):
        print(f"{instance.name} - tanks in posession: {instance.country}")
        print(f"{instance.name} - tanks produced: {instance.origin}")
    print()
    # alliance = session.query(Alliance).one()
    # print(alliance.country1)
    for instance in session.query(Alliance).all():
        print(f"[{instance.country1.name}, {instance.country2.name}]")
