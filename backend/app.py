import sqlalchemy as db
from sqlalchemy import distinct
from sqlalchemy.orm import sessionmaker

from flask import Flask, request, jsonify
from flask_cors import CORS

from sqlalchemy.ext.declarative import declarative_base

import networkx as nx

from functools import reduce

Base = declarative_base()

app = Flask(__name__.split(".")[0])
CORS(app)

engine = db.create_engine("sqlite:///main.db")
Session = sessionmaker(bind=engine)


@app.route("/tankTypes")
def return_tanktypes():
    # Connect to the database.
    session = Session()
    # Query the tank types.
    response = [
        instance.name for instance in session.query(Tank.name).distinct()
    ]
    unique_response = sorted(set(response))
    session.close()
    # Return
    return jsonify({"tankTypes": unique_response})


@app.route("/countries")
def return_countries():
    session = Session()
    response = [instance.name for instance in session.query(Country).all()]
    session.close()
    return jsonify({"countries": response})


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
    threshold = int(request.args.get("threshold"))

    session = Session()

    query = session.query(Tank).filter_by(name=tank_name)
    country_names = [
        instance.country.name
        for instance in query
        if instance.quantity >= threshold
    ]
    quantity = [
        instance.quantity
        for instance in query
        if instance.quantity >= threshold
    ]

    chart = {
        "labels": country_names,
        "datasets": [
            {"label": "Number of tanks", "borderWidth": 2, "data": quantity}
        ],
    }

    session.close()

    return jsonify(chart)


@app.route("/chart2")
def chart2_get():
    """?????? Wykres wielkości produkcji ??????
    TODO: Make country names a list.

    Kolejnym interesującym scenariuszem użycia aplikacji byłby wykres prezentujący ilości wyprodukowanych czołgów oraz ich eksport 
    przez kraje wybrane przez użytkownika

    :param country_names:
    :type country_names: List[str]

    :rtype: Chart
    """
    country_names = request.args.getlist("country_names[]")

    session = Session()

    # list of countries ids
    country_ids = []
    # aggregative quantity of owned tanks (country_name[0] has quantity[0] tanks etc.)
    quantity = []
    # aggregative quantity of possessed tanks (country_name[0] has produced export_quantity[0] tanks etc.)
    export_quantity = []

    for country_name in country_names:
        country_id = (
            session.query(Country.id).filter_by(name=country_name).one()[0]
        )
        country_ids.append(country_id)

    # tanks owned
    for c_id in country_ids:
        # owned tanks by type for country_id equal c_id
        tmp = []
        # list of tuples, where first element is a quantity of tanks per type
        quants = session.query(Tank.quantity).filter_by(country_id=c_id).all()
        for quant in quants:
            tmp.append(quant[0])
        # list for reduce function can't be empty
        if not tmp:
            tmp.append(0)
        quantity.append(reduce(lambda a, b: a + b, tmp))

    # tanks exported
    for c_id in country_ids:
        # exported tanks by type for country_id equal c_id
        tmp = []
        exps = session.query(Tank.quantity).filter_by(origin_id=c_id).all()
        for exp in exps:
            tmp.append(exp[0])
        if not tmp:
            tmp.append(0)
        export_quantity.append(reduce(lambda a, b: a + b, tmp))

    session.close()

    chart = {
        "labels": country_names,
        "datasets": [
            {"label": "Number of tanks", "borderWidth": 2, "data": quantity},
            {
                "label": "Number of exported tanks",
                "borderWidth": 2,
                "data": export_quantity,
            },
        ],
    }

    return jsonify(chart)


@app.route("/chart3")
def chart3_get():
    """?????? Wykres posiadanych czołgów ??????
    TODO: Make country names a list.

    Użytkownik będzie miał możliwość wyboru z dropdownu kilku krajów dla których chce przeprowadzić porównanie, 
    a następnie wykreślić na wykresie informacje o ilości i typach posiadanych czołgów

    :param country_name:
    :type country_name: List[str]

    :rtype: Chart
    """
    country_names = request.args.getlist("country_names[]")

    session = Session()

    country_tanks = {}

    tank_names = set()

    output = {}

    for country_name in country_names:
        country_tanks[country_name] = {}

    for country_name in country_names:
        country = session.query(Country).filter_by(name=country_name).one()
        for tank in country.country:
            tank_names.add(tank.name)
            country_tanks[country_name][tank.name] = tank.quantity

    for tank_name in tank_names:
        output[tank_name] = []

    for country, tanks in country_tanks.items():
        for tank_name in tank_names:
            if tank_name in tanks:
                output[tank_name].append(tanks[tank_name])
            else:
                output[tank_name].append(0)

    labels = country_names
    datasets = []

    for key, value in output.items():
        row = {"label": key, "borderWidth": 2, "data": value}
        datasets.append(row)

    chart = {"labels": labels, "datasets": datasets}

    session.close()

    return jsonify(chart)


@app.route("/sellersGraph")
def sellers_graph_get():
    """Graf powiązań producentów z krajami kupującymi

    Graf przedstawiający powiązania producentów z krajami do których eksportowane są ich czołgi. 
    Dodatkowo przewidziana opcja ograniczenia do krajów będących w sojuszu.

    :param country_name:
    :type country_name: str
    :param k_core:
    :type k_core: int
    :param alliance_only: tylko kraje będące w sojuszu
    :type alliance_only: bool

    :rtype: Graph
    """
    country_name = request.args.get("country_name")
    k_core = request.args.get("k_core")
    if k_core:
        k_core = int(k_core)
    alliance_only = request.args.get("alliance_only") == "true"

    session = Session()
    c_id = session.query(Country.id).filter_by(name=country_name).one()[0]

    # Find countries possessing tanks produced by country_name
    query = session.query(Tank).filter_by(origin_id=c_id)
    ids_lst = [res.country_id for res in query]
    ids_lst.append(c_id)
    ids_lst = sorted(set(ids_lst))

    edges = [
        {"source": c_id, "target": ids_lst[i]} for i in range(len(ids_lst))
    ]

    edges_graph = [(c_id, ids_lst[i]) for i in range(len(ids_lst))]

    if not alliance_only:
        nodes = []
        for i in ids_lst:
            country_n = session.query(Country.name).filter_by(id=i).one()[0]
            nodes.append({"id": i, "name": country_n})

        links = edges

    if alliance_only:
        query_alliance = session.query(Alliance).all()
        all_sellers = [
            {"source": instance.country1_id, "target": instance.country2_id}
            for instance in query_alliance
        ]

        alliance_sellers = []
        for i in range(len(ids_lst)):
            for j in range(i + 1, len(ids_lst)):
                alliance_sellers.append(
                    {"source": ids_lst[i], "target": ids_lst[j]}
                )

        links = [d for d in alliance_sellers if d in all_sellers]

        ids = []

        for i in range(len(links)):
            for key, val in links[i].items():
                ids.append(val)
        ids_unique = sorted(set(ids))

        nodes = []
        for i in ids_unique:
            country_n = session.query(Country.name).filter_by(id=i).one()[0]
            nodes.append({"id": i, "name": country_n})
        # query_alliance = session.query(Alliance).filter_by(country1_id=c_id)
        # all_sellers = [
        #     {"source": c_id, "target": instance.country2_id}
        #     for instance in query_alliance
        # ]
        # all_sellers_graph = [
        #     (c_id, instance.country2_id) for instance in query_alliance
        # ]

        # alliance_sellers = [d for d in edges if d in all_sellers]

        # alliance_sellers_graph = list(
        #     set(edges_graph).intersection(all_sellers_graph)
        # )

        # G = nx.Graph()
        # G.add_edges_from(alliance_sellers_graph)
        # G.to_undirected()
        # G1 = nx.k_core(G, k=k_core)
        # g = nx.to_dict_of_lists(G1)

        # links = []
        # for val in g.values():
        #     for i in range(len(val)):
        #         if val[i] != c_id:
        #             links.append({"source": c_id, "target": val[i]})

        # nodes = []
        # for key in g.keys():
        #     country_name = (
        #         session.query(Country.name).filter_by(id=key).one()[0]
        #     )
        #     nodes.append({"id": key, "name": country_name})

    session.close()

    response = {"nodes": nodes, "links": links}
    return jsonify(response)


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
    if k_core:
        k_core = int(k_core)
    alliance_only = request.args.get("alliance_only") == "true"

    session = Session()
    # Find countries possesing the same type of tanks
    query = (
        session.query(Country)
        .join(Country.country)
        .filter(Country.country.property.mapper.class_.name == tank_name)
    )
    ids_lst = [res.id for res in query]
    edges = []
    edges_graph = []
    for i in range(len(ids_lst)):
        for j in range(i + 1, len(ids_lst)):
            edges.append({"source": ids_lst[i], "target": ids_lst[j]})
            edges_graph.append((ids_lst[i], ids_lst[j]))

    if not alliance_only:
        nodes = [
            {"id": instance.id, "name": instance.name} for instance in query
        ]
        nodes_graph = [(instance.id, instance.name) for instance in query]

        links = edges

    if alliance_only:
        query_alliance = session.query(Alliance).all()
        all_tanks = [
            {"source": instance.country1_id, "target": instance.country2_id}
            for instance in query_alliance
        ]
        all_tanks_graph = [
            (instance.country1_id, instance.country2_id)
            for instance in query_alliance
        ]

        alliance_tanks = [d for d in edges if d in all_tanks]
        alliance_tanks_graph = list(
            set(edges_graph).intersection(all_tanks_graph)
        )

        G = nx.Graph()
        G.add_edges_from(alliance_tanks_graph)
        G.to_undirected()
        G1 = nx.k_core(G, k=k_core)
        g = nx.to_dict_of_lists(G1)

        links = []
        for key, val in g.items():
            for i in range(len(val)):
                links.append({"source": key, "target": val[i]})

        nodes = []
        for key in g.keys():
            country_name = (
                session.query(Country.name).filter_by(id=key).one()[0]
            )
            nodes.append({"id": key, "name": country_name})

    session.close()

    response = {"nodes": nodes, "links": links}
    return jsonify(response)


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
