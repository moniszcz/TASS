import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from flask import Flask, request, jsonify
from flask_cors import CORS

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

app = Flask(__name__.split('.')[0])
CORS(app)

engine = db.create_engine("sqlite:///main.db")
Session = sessionmaker(bind=engine)

@app.route("/tankTypes")
def return_tanktypes():
    # Connect to the database.

    # Query the tank types.

    # Return
    return jsonify({ 'tankTypes': ['Foo', 'Bar', 'Baz'] })

@app.route("/countries")
def return_countries():
    session = Session()
    response = [ instance.name for instance in session.query(Country).all()]
    session.close()
    return jsonify({ 'countries': response })
  


@app.route("/chart1")
def chart1_get():
    """Wykreślenie krajów, które posiadają dany typ czołgu

    W zbiorze danych na Wikipedii, możemy zauważyć że niektóre kraje posiadają
    ten sam typ czołgu, dlatego interesującym scenariuszem użycia aplikacji
    byłaby możliwość stworzenia wykresu porównawczego. Użytkownik będzie mógł
    wybrać z dropdownu interesujący go model wozu bojowego, a następnie
    wykreślić wykres dla wszystkich krajów, które posiadają ten typ czołgu.
    Ewentualnie użytkownik będzie miał możliwość wpisania
    maksymalnego progu ilości czołgów.

    :param tank_name:
    :type tank_name: str
    :param threshold:
    :type threshold: int

    :rtype: Chart
    """
    tank_name = request.args.get("tank_name")
    threshold = request.args.get("threshold")

    print(f"tank_name: {tank_name}, threshold: {threshold}")

    return jsonify(chart1)


@app.route("/chart2")
def chart2_get():
    """?????? Wykres wielkości produkcji ??????
    TODO: Make country names a list.

    Kolejnym interesującym scenariuszem użycia aplikacji byłby wykres prezentujący ilości wyprodukowanych czołgów oraz ich eksport przez kraje wybrane przez użytkownika

    :param country_names:
    :type country_names: List[str]

    :rtype: Chart
    """
    country_names = request.args.getlist("country_names[]")
    print(f"country_names: {country_names}")

    return jsonify(chart2)


@app.route("/chart3")
def chart3_get():
    """?????? Wykres posiadanych czołgów ??????
    TODO: Make country names a list.

    Użytkownik będzie miał możliwość wyboru z dropdownu kilku krajów dla których chce przeprowadzić porównanie, a następnie wykreślić na wykresie informacje o ilości i typach posiadanych czołgów

    :param country_name:
    :type country_name: List[str]

    :rtype: Chart
    """
    country_names = request.args.getlist("country_names[]")

    return jsonify(chart3)



@app.route("/sellersGraph")
def sellers_graph_get():
    """Graf powiązań producentów z krajami kupującymi

    Graf przedstawiający powiązania producentów z krajami do których eksportowane są ich czołgi. Dodatkowo przewidziana opcja ograniczenia do krajów będących w sojuszu

    :param country_name:
    :type country_name: str
    :param k_core:
    :type k_core: int
    :param alliance_only: tylko kraje będące w sojuszu
    :type alliance_only: bool

    :rtype: Graph
    """
    print(request.args)
    country_names = request.args.getlist("country_names[]")
    k_core = request.args.get("k_core")
    alliance_only = request.args.get("alliance_only")

    print(f"country_names: {country_names}, k_core: {k_core}, alliance_only: {alliance_only}")
    return jsonify(dataset1)


@app.route("/tankGraph")
def tank_graph_get():
    """Graf powiązań

    Graf prezentujący powiązania między krajami posiadającymi ten sam typ czołgu, wybrany przez użytkownika. Ewentualna dodatkowa opcja zawężająca cały graf do państw będących ze sobą w sojuszu. Możliwość wyboru konkretnego k-rdzenia przez użytkownika

    :param tank_name:
    :type tank_name: str
    :param k_core:
    :type k_core: int
    :param alliance_only: tylko kraje będące w sojuszu
    :type alliance_only: bool

    :rtype: Graph
    """
    tank_name = request.args.get("tank_name")
    k_core = request.args.get("k_core")
    alliance_only = request.args.get("alliance_only")

    print(f"tank_name: {tank_name}, k_core: {k_core}, alliance_only: {alliance_only}")
    return jsonify(dataset2)


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




chart1 =  {
  'labels': ['Poland', 'Germany', 'Russia'],
  'datasets': [
    {
      'label': 'Number of tanks',
      'backgroundColor': 'rgba(255,99,132,0.2)',
      'borderColor': 'rgba(255,99,132,1)',
      'borderWidth': 2,
      'hoverBackgroundColor': 'rgba(255,99,132,0.4)',
      'hoverBorderColor': 'rgba(255,99,132,1)',
      'data': [65, 59, 80]
    }
  ]
}

chart2 =  {
  'labels': ['Poland', 'Germany', 'Russia'],
  'datasets': [
    {
      'label': 'Number of tanks',
      'backgroundColor': 'rgba(255,99,132,0.2)',
      'borderColor': 'rgba(255,99,132,1)',
      'borderWidth': 2,
      'hoverBackgroundColor': 'rgba(255,99,132,0.4)',
      'hoverBorderColor': 'rgba(255,99,132,1)',
      'data': [65, 59, 80]
    },
    {
      'label': 'Number of exported tanks',
      'backgroundColor': 'rgba(155,99,132,0.2)',
      'borderColor': 'rgba(155,99,132,1)',
      'borderWidth': 2,
      'hoverBackgroundColor': 'rgba(155,99,132,0.4)',
      'hoverBorderColor': 'rgba(155,99,132,1)',
      'data': [20, 30, 40]
    }
  ]
}

chart3 =  {
  'labels': ['Poland', 'Germany', 'Russia'],
  'datasets': [
    {
      'label': 'T45',
      'backgroundColor': 'rgba(255,99,132,0.2)',
      'borderColor': 'rgba(255,99,132,1)',
      'borderWidth': 2,
      'hoverBackgroundColor': 'rgba(255,99,132,0.4)',
      'hoverBorderColor': 'rgba(255,99,132,1)',
      'data': [65, 59, 80]
    },
    {
      'label': 'T55',
      'backgroundColor': 'rgba(155,99,132,0.2)',
      'borderColor': 'rgba(155,99,132,1)',
      'borderWidth': 2,
      'hoverBackgroundColor': 'rgba(155,99,132,0.4)',
      'hoverBorderColor': 'rgba(155,99,132,1)',
      'data': [20, 0, 40]
    }
  ]
}

dataset1 = {
    "nodes": [
        {"id": 1, "name": "A"},
        {"id": 2, "name": "B"},
        {"id": 3, "name": "C"},
        {"id": 4, "name": "D"},
        {"id": 5, "name": "E"},
        {"id": 6, "name": "F"},
        {"id": 7, "name": "G"},
        {"id": 8, "name": "H"},
        {"id": 9, "name": "I"},
        {"id": 10, "name": "J"},
    ],
    "links": [
        {"source": 1, "target": 2},
        {"source": 1, "target": 5},
        {"source": 1, "target": 6},
        {"source": 2, "target": 3},
        {"source": 2, "target": 7},
        {"source": 3, "target": 4},
        {"source": 8, "target": 3},
        {"source": 4, "target": 5},
        {"source": 4, "target": 9},
        {"source": 5, "target": 10},
    ],
}

dataset2 = {
  'nodes': [
    { 'id': 'Myriel', 'name': 'Myriel', 'group': 1 },
    { 'id': 'Napoleon', 'name': 'Napoleon', 'group': 1 },
    { 'id': 'Mlle.Baptistine', 'name': 'Mlle.Baptistine', 'group': 1 },
    { 'id': 'Mme.Magloire', 'name': 'Mme.Magloire', 'group': 1 },
    { 'id': 'CountessdeLo', 'name': 'CountessdeLo', 'group': 1 },
    { 'id': 'Geborand', 'name': 'Geborand', 'group': 1 },
    { 'id': 'Champtercier', 'name': 'Champtercier', 'group': 1 },
    { 'id': 'Cravatte', 'name': 'Cravatte', 'group': 1 },
    { 'id': 'Count', 'name': 'Count', 'group': 1 },
    { 'id': 'OldMan', 'name': 'OldMan', 'group': 1 },
    { 'id': 'Labarre', 'name': 'Labarre', 'group': 2 },
    { 'id': 'Valjean', 'name': 'Valjean', 'group': 2 },
    { 'id': 'Marguerite', 'name': 'Marguerite', 'group': 3 },
    { 'id': 'Mme.deR', 'name': 'Mme.deR', 'group': 2 },
    { 'id': 'Isabeau', 'name': 'Isabeau', 'group': 2 },
    { 'id': 'Gervais', 'name': 'Gervais', 'group': 2 },
    { 'id': 'Tholomyes', 'name': 'Tholomyes', 'group': 3 },
    { 'id': 'Listolier', 'name': 'Listolier', 'group': 3 },
    { 'id': 'Fameuil', 'name': 'Fameuil', 'group': 3 },
    { 'id': 'Blacheville', 'name': 'Blacheville', 'group': 3 },
    { 'id': 'Favourite', 'name': 'Favourite', 'group': 3 },
    { 'id': 'Dahlia', 'name': 'Dahlia', 'group': 3 },
    { 'id': 'Zephine', 'name': 'Zephine', 'group': 3 },
    { 'id': 'Fantine', 'name': 'Fantine', 'group': 3 },
    { 'id': 'Mme.Thenardier', 'name': 'Mme.Thenardier', 'group': 4 },
    { 'id': 'Thenardier', 'name': 'Thenardier', 'group': 4 },
    { 'id': 'Cosette', 'name': 'Cosette', 'group': 5 },
    { 'id': 'Javert', 'name': 'Javert', 'group': 4 },
    { 'id': 'Fauchelevent', 'name': 'Fauchelevent', 'group': 0 },
    { 'id': 'Bamatabois', 'name': 'Bamatabois', 'group': 2 },
    { 'id': 'Perpetue', 'name': 'Perpetue', 'group': 3 },
    { 'id': 'Simplice', 'name': 'Simplice', 'group': 2 },
    { 'id': 'Scaufflaire', 'name': 'Scaufflaire', 'group': 2 },
    { 'id': 'Woman1', 'name': 'Woman1', 'group': 2 },
    { 'id': 'Judge', 'name': 'Judge', 'group': 2 },
    { 'id': 'Champmathieu', 'name': 'Champmathieu', 'group': 2 },
    { 'id': 'Brevet', 'name': 'Brevet', 'group': 2 },
    { 'id': 'Chenildieu', 'name': 'Chenildieu', 'group': 2 },
    { 'id': 'Cochepaille', 'name': 'Cochepaille', 'group': 2 },
    { 'id': 'Pontmercy', 'name': 'Pontmercy', 'group': 4 },
    { 'id': 'Boulatruelle', 'name': 'Boulatruelle', 'group': 6 },
    { 'id': 'Eponine', 'name': 'Eponine', 'group': 4 },
    { 'id': 'Anzelma', 'name': 'Anzelma', 'group': 4 },
    { 'id': 'Woman2', 'name': 'Woman2', 'group': 5 },
    { 'id': 'MotherInnocent', 'name': 'MotherInnocent', 'group': 0 },
    { 'id': 'Gribier', 'name': 'Gribier', 'group': 0 },
    { 'id': 'Jondrette', 'name': 'Jondrette', 'group': 7 },
    { 'id': 'Mme.Burgon', 'name': 'Mme.Burgon', 'group': 7 },
    { 'id': 'Gavroche', 'name': 'Gavroche', 'group': 8 },
    { 'id': 'Gillenormand', 'name': 'Gillenormand', 'group': 5 },
    { 'id': 'Magnon', 'name': 'Magnon', 'group': 5 },
    { 'id': 'Mlle.Gillenormand', 'name': 'Mlle.Gillenormand', 'group': 5 },
    { 'id': 'Mme.Pontmercy', 'name': 'Mme.Pontmercy', 'group': 5 },
    { 'id': 'Mlle.Vaubois', 'name': 'Mlle.Vaubois', 'group': 5 },
    { 'id': 'Lt.Gillenormand', 'name': 'Lt.Gillenormand', 'group': 5 },
    { 'id': 'Marius', 'name': 'Marius', 'group': 8 },
    { 'id': 'BaronessT', 'name': 'BaronessT', 'group': 5 },
    { 'id': 'Mabeuf', 'name': 'Mabeuf', 'group': 8 },
    { 'id': 'Enjolras', 'name': 'Enjolras', 'group': 8 },
    { 'id': 'Combeferre', 'name': 'Combeferre', 'group': 8 },
    { 'id': 'Prouvaire', 'name': 'Prouvaire', 'group': 8 },
    { 'id': 'Feuilly', 'name': 'Feuilly', 'group': 8 },
    { 'id': 'Courfeyrac', 'name': 'Courfeyrac', 'group': 8 },
    { 'id': 'Bahorel', 'name': 'Bahorel', 'group': 8 },
    { 'id': 'Bossuet', 'name': 'Bossuet', 'group': 8 },
    { 'id': 'Joly', 'name': 'Joly', 'group': 8 },
    { 'id': 'Grantaire', 'name': 'Grantaire', 'group': 8 },
    { 'id': 'MotherPlutarch', 'name': 'MotherPlutarch', 'group': 9 },
    { 'id': 'Gueulemer', 'name': 'Gueulemer', 'group': 4 },
    { 'id': 'Babet', 'name': 'Babet', 'group': 4 },
    { 'id': 'Claquesous', 'name': 'Claquesous', 'group': 4 },
    { 'id': 'Montparnasse', 'name': 'Montparnasse', 'group': 4 },
    { 'id': 'Toussaint', 'name': 'Toussaint', 'group': 5 },
    { 'id': 'Child1', 'name': 'Child1', 'group': 10 },
    { 'id': 'Child2', 'name': 'Child2', 'group': 10 },
    { 'id': 'Brujon', 'name': 'Brujon', 'group': 4 },
    { 'id': 'Mme.Hucheloup', 'name': 'Mme.Hucheloup', 'group': 8 }
  ],
  'links': [
    { 'source': 'Claquesous', 'target': 'Mme.Thenardier', 'value': 1 },
    { 'source': 'Claquesous', 'target': 'Javert', 'value': 1 },
    { 'source': 'Claquesous', 'target': 'Eponine', 'value': 1 },
    { 'source': 'Claquesous', 'target': 'Enjolras', 'value': 1 },
    { 'source': 'Montparnasse', 'target': 'Javert', 'value': 1 },
    { 'source': 'Montparnasse', 'target': 'Babet', 'value': 2 },
    { 'source': 'Montparnasse', 'target': 'Gueulemer', 'value': 2 },
    { 'source': 'Montparnasse', 'target': 'Claquesous', 'value': 2 },
    { 'source': 'Montparnasse', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Montparnasse', 'target': 'Gavroche', 'value': 1 },
    { 'source': 'Montparnasse', 'target': 'Eponine', 'value': 1 },
    { 'source': 'Montparnasse', 'target': 'Thenardier', 'value': 1 },
    { 'source': 'Toussaint', 'target': 'Cosette', 'value': 2 },
    { 'source': 'Toussaint', 'target': 'Javert', 'value': 1 },
    { 'source': 'Toussaint', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Child1', 'target': 'Gavroche', 'value': 2 },
    { 'source': 'Child2', 'target': 'Gavroche', 'value': 2 },
    { 'source': 'Child2', 'target': 'Child1', 'value': 3 },
    { 'source': 'Brujon', 'target': 'Babet', 'value': 3 },
    { 'source': 'Brujon', 'target': 'Gueulemer', 'value': 3 },
    { 'source': 'Brujon', 'target': 'Thenardier', 'value': 3 },
    { 'source': 'Brujon', 'target': 'Gavroche', 'value': 1 },
    { 'source': 'Brujon', 'target': 'Eponine', 'value': 1 },
    { 'source': 'Brujon', 'target': 'Claquesous', 'value': 1 },
    { 'source': 'Brujon', 'target': 'Montparnasse', 'value': 1 },
    { 'source': 'Mme.Hucheloup', 'target': 'Bossuet', 'value': 1 },
    { 'source': 'Mme.Hucheloup', 'target': 'Joly', 'value': 1 },
    { 'source': 'Mme.Hucheloup', 'target': 'Grantaire', 'value': 1 },
    { 'source': 'Mme.Hucheloup', 'target': 'Bahorel', 'value': 1 },
    { 'source': 'Mme.Hucheloup', 'target': 'Courfeyrac', 'value': 1 },
    { 'source': 'Mme.Hucheloup', 'target': 'Gavroche', 'value': 1 },
    { 'source': 'Mme.Hucheloup', 'target': 'Enjolras', 'value': 1 }
  ]
}
