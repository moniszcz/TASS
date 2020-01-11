import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tank(Base):
    __tablename__ = "tanks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    quantity = db.Column(db.Integer)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    origin_id = db.Column(db.Integer, db.ForeignKey("countries.id"))

    country = db.orm.relationship(
        "Country", foreign_keys=[country_id], backref="country"
    )
    origin = db.orm.relationship(
        "Country", foreign_keys=[origin_id], backref="origin"
    )

    def __repr__(self):
        return f"<Tank(name={self.name}, quantity={self.quantity})>"


class Country(Base):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __repr__(self):
        return f"<Country(name={self.name})>"


class Alliance(Base):
    __tablename__ = "alliances"
    id = db.Column(db.Integer, primary_key=True)
    country1_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    country2_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)

    country1 = db.orm.relationship(
        "Country", foreign_keys=[country1_id], backref="country1"
    )
    country2 = db.orm.relationship(
        "Country", foreign_keys=[country2_id], backref="country2"
    )

    def __repr__(self):
        return f"<Alliance(country1={self.country1_id}, country2={self.country2_id})>"


if __name__ == "__main__":
    # Create database.
    engine = db.create_engine("sqlite:///foo.db")
    Base.metadata.create_all(engine)
