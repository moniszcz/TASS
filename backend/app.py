from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/tankTypes")
def return_tanktypes():
    return jsonify({ 'tankTypes': ['Foo', 'Bar', 'Baz'] })

@app.route("/countries")
def return_countries():
    return jsonify({ 'countries': ['Poland', 'Germany', 'Finland'] })


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
    { 'source': 'Napoleon', 'target': 'Myriel', 'value': 1 },
    { 'source': 'Mlle.Baptistine', 'target': 'Myriel', 'value': 8 },
    { 'source': 'Mme.Magloire', 'target': 'Myriel', 'value': 10 },
    { 'source': 'Mme.Magloire', 'target': 'Mlle.Baptistine', 'value': 6 },
    { 'source': 'CountessdeLo', 'target': 'Myriel', 'value': 1 },
    { 'source': 'Geborand', 'target': 'Myriel', 'value': 1 },
    { 'source': 'Champtercier', 'target': 'Myriel', 'value': 1 },
    { 'source': 'Cravatte', 'target': 'Myriel', 'value': 1 },
    { 'source': 'Count', 'target': 'Myriel', 'value': 2 },
    { 'source': 'OldMan', 'target': 'Myriel', 'value': 1 },
    { 'source': 'Valjean', 'target': 'Labarre', 'value': 1 },
    { 'source': 'Valjean', 'target': 'Mme.Magloire', 'value': 3 },
    { 'source': 'Valjean', 'target': 'Mlle.Baptistine', 'value': 3 },
    { 'source': 'Valjean', 'target': 'Myriel', 'value': 5 },
    { 'source': 'Marguerite', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Mme.deR', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Isabeau', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Gervais', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Listolier', 'target': 'Tholomyes', 'value': 4 },
    { 'source': 'Fameuil', 'target': 'Tholomyes', 'value': 4 },
    { 'source': 'Fameuil', 'target': 'Listolier', 'value': 4 },
    { 'source': 'Blacheville', 'target': 'Tholomyes', 'value': 4 },
    { 'source': 'Blacheville', 'target': 'Listolier', 'value': 4 },
    { 'source': 'Blacheville', 'target': 'Fameuil', 'value': 4 },
    { 'source': 'Favourite', 'target': 'Tholomyes', 'value': 3 },
    { 'source': 'Favourite', 'target': 'Listolier', 'value': 3 },
    { 'source': 'Favourite', 'target': 'Fameuil', 'value': 3 },
    { 'source': 'Favourite', 'target': 'Blacheville', 'value': 4 },
    { 'source': 'Dahlia', 'target': 'Tholomyes', 'value': 3 },
    { 'source': 'Dahlia', 'target': 'Listolier', 'value': 3 },
    { 'source': 'Dahlia', 'target': 'Fameuil', 'value': 3 },
    { 'source': 'Dahlia', 'target': 'Blacheville', 'value': 3 },
    { 'source': 'Dahlia', 'target': 'Favourite', 'value': 5 },
    { 'source': 'Zephine', 'target': 'Tholomyes', 'value': 3 },
    { 'source': 'Zephine', 'target': 'Listolier', 'value': 3 },
    { 'source': 'Zephine', 'target': 'Fameuil', 'value': 3 },
    { 'source': 'Zephine', 'target': 'Blacheville', 'value': 3 },
    { 'source': 'Zephine', 'target': 'Favourite', 'value': 4 },
    { 'source': 'Zephine', 'target': 'Dahlia', 'value': 4 },
    { 'source': 'Fantine', 'target': 'Tholomyes', 'value': 3 },
    { 'source': 'Fantine', 'target': 'Listolier', 'value': 3 },
    { 'source': 'Fantine', 'target': 'Fameuil', 'value': 3 },
    { 'source': 'Fantine', 'target': 'Blacheville', 'value': 3 },
    { 'source': 'Fantine', 'target': 'Favourite', 'value': 4 },
    { 'source': 'Fantine', 'target': 'Dahlia', 'value': 4 },
    { 'source': 'Fantine', 'target': 'Zephine', 'value': 4 },
    { 'source': 'Fantine', 'target': 'Marguerite', 'value': 2 },
    { 'source': 'Fantine', 'target': 'Valjean', 'value': 9 },
    { 'source': 'Mme.Thenardier', 'target': 'Fantine', 'value': 2 },
    { 'source': 'Mme.Thenardier', 'target': 'Valjean', 'value': 7 },
    { 'source': 'Thenardier', 'target': 'Mme.Thenardier', 'value': 13 },
    { 'source': 'Thenardier', 'target': 'Fantine', 'value': 1 },
    { 'source': 'Thenardier', 'target': 'Valjean', 'value': 12 },
    { 'source': 'Cosette', 'target': 'Mme.Thenardier', 'value': 4 },
    { 'source': 'Cosette', 'target': 'Valjean', 'value': 31 },
    { 'source': 'Cosette', 'target': 'Tholomyes', 'value': 1 },
    { 'source': 'Cosette', 'target': 'Thenardier', 'value': 1 },
    { 'source': 'Javert', 'target': 'Valjean', 'value': 17 },
    { 'source': 'Javert', 'target': 'Fantine', 'value': 5 },
    { 'source': 'Javert', 'target': 'Thenardier', 'value': 5 },
    { 'source': 'Javert', 'target': 'Mme.Thenardier', 'value': 1 },
    { 'source': 'Javert', 'target': 'Cosette', 'value': 1 },
    { 'source': 'Fauchelevent', 'target': 'Valjean', 'value': 8 },
    { 'source': 'Fauchelevent', 'target': 'Javert', 'value': 1 },
    { 'source': 'Bamatabois', 'target': 'Fantine', 'value': 1 },
    { 'source': 'Bamatabois', 'target': 'Javert', 'value': 1 },
    { 'source': 'Bamatabois', 'target': 'Valjean', 'value': 2 },
    { 'source': 'Perpetue', 'target': 'Fantine', 'value': 1 },
    { 'source': 'Simplice', 'target': 'Perpetue', 'value': 2 },
    { 'source': 'Simplice', 'target': 'Valjean', 'value': 3 },
    { 'source': 'Simplice', 'target': 'Fantine', 'value': 2 },
    { 'source': 'Simplice', 'target': 'Javert', 'value': 1 },
    { 'source': 'Scaufflaire', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Woman1', 'target': 'Valjean', 'value': 2 },
    { 'source': 'Woman1', 'target': 'Javert', 'value': 1 },
    { 'source': 'Judge', 'target': 'Valjean', 'value': 3 },
    { 'source': 'Judge', 'target': 'Bamatabois', 'value': 2 },
    { 'source': 'Champmathieu', 'target': 'Valjean', 'value': 3 },
    { 'source': 'Champmathieu', 'target': 'Judge', 'value': 3 },
    { 'source': 'Champmathieu', 'target': 'Bamatabois', 'value': 2 },
    { 'source': 'Brevet', 'target': 'Judge', 'value': 2 },
    { 'source': 'Brevet', 'target': 'Champmathieu', 'value': 2 },
    { 'source': 'Brevet', 'target': 'Valjean', 'value': 2 },
    { 'source': 'Brevet', 'target': 'Bamatabois', 'value': 1 },
    { 'source': 'Chenildieu', 'target': 'Judge', 'value': 2 },
    { 'source': 'Chenildieu', 'target': 'Champmathieu', 'value': 2 },
    { 'source': 'Chenildieu', 'target': 'Brevet', 'value': 2 },
    { 'source': 'Chenildieu', 'target': 'Valjean', 'value': 2 },
    { 'source': 'Chenildieu', 'target': 'Bamatabois', 'value': 1 },
    { 'source': 'Cochepaille', 'target': 'Judge', 'value': 2 },
    { 'source': 'Cochepaille', 'target': 'Champmathieu', 'value': 2 },
    { 'source': 'Cochepaille', 'target': 'Brevet', 'value': 2 },
    { 'source': 'Cochepaille', 'target': 'Chenildieu', 'value': 2 },
    { 'source': 'Cochepaille', 'target': 'Valjean', 'value': 2 },
    { 'source': 'Cochepaille', 'target': 'Bamatabois', 'value': 1 },
    { 'source': 'Pontmercy', 'target': 'Thenardier', 'value': 1 },
    { 'source': 'Boulatruelle', 'target': 'Thenardier', 'value': 1 },
    { 'source': 'Eponine', 'target': 'Mme.Thenardier', 'value': 2 },
    { 'source': 'Eponine', 'target': 'Thenardier', 'value': 3 },
    { 'source': 'Anzelma', 'target': 'Eponine', 'value': 2 },
    { 'source': 'Anzelma', 'target': 'Thenardier', 'value': 2 },
    { 'source': 'Anzelma', 'target': 'Mme.Thenardier', 'value': 1 },
    { 'source': 'Woman2', 'target': 'Valjean', 'value': 3 },
    { 'source': 'Woman2', 'target': 'Cosette', 'value': 1 },
    { 'source': 'Woman2', 'target': 'Javert', 'value': 1 },
    { 'source': 'MotherInnocent', 'target': 'Fauchelevent', 'value': 3 },
    { 'source': 'MotherInnocent', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Gribier', 'target': 'Fauchelevent', 'value': 2 },
    { 'source': 'Mme.Burgon', 'target': 'Jondrette', 'value': 1 },
    { 'source': 'Gavroche', 'target': 'Mme.Burgon', 'value': 2 },
    { 'source': 'Gavroche', 'target': 'Thenardier', 'value': 1 },
    { 'source': 'Gavroche', 'target': 'Javert', 'value': 1 },
    { 'source': 'Gavroche', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Gillenormand', 'target': 'Cosette', 'value': 3 },
    { 'source': 'Gillenormand', 'target': 'Valjean', 'value': 2 },
    { 'source': 'Magnon', 'target': 'Gillenormand', 'value': 1 },
    { 'source': 'Magnon', 'target': 'Mme.Thenardier', 'value': 1 },
    { 'source': 'Mlle.Gillenormand', 'target': 'Gillenormand', 'value': 9 },
    { 'source': 'Mlle.Gillenormand', 'target': 'Cosette', 'value': 2 },
    { 'source': 'Mlle.Gillenormand', 'target': 'Valjean', 'value': 2 },
    { 'source': 'Mme.Pontmercy', 'target': 'Mlle.Gillenormand', 'value': 1 },
    { 'source': 'Mme.Pontmercy', 'target': 'Pontmercy', 'value': 1 },
    { 'source': 'Mlle.Vaubois', 'target': 'Mlle.Gillenormand', 'value': 1 },
    { 'source': 'Lt.Gillenormand', 'target': 'Mlle.Gillenormand', 'value': 2 },
    { 'source': 'Lt.Gillenormand', 'target': 'Gillenormand', 'value': 1 },
    { 'source': 'Lt.Gillenormand', 'target': 'Cosette', 'value': 1 },
    { 'source': 'Marius', 'target': 'Mlle.Gillenormand', 'value': 6 },
    { 'source': 'Marius', 'target': 'Gillenormand', 'value': 12 },
    { 'source': 'Marius', 'target': 'Pontmercy', 'value': 1 },
    { 'source': 'Marius', 'target': 'Lt.Gillenormand', 'value': 1 },
    { 'source': 'Marius', 'target': 'Cosette', 'value': 21 },
    { 'source': 'Marius', 'target': 'Valjean', 'value': 19 },
    { 'source': 'Marius', 'target': 'Tholomyes', 'value': 1 },
    { 'source': 'Marius', 'target': 'Thenardier', 'value': 2 },
    { 'source': 'Marius', 'target': 'Eponine', 'value': 5 },
    { 'source': 'Marius', 'target': 'Gavroche', 'value': 4 },
    { 'source': 'BaronessT', 'target': 'Gillenormand', 'value': 1 },
    { 'source': 'BaronessT', 'target': 'Marius', 'value': 1 },
    { 'source': 'Mabeuf', 'target': 'Marius', 'value': 1 },
    { 'source': 'Mabeuf', 'target': 'Eponine', 'value': 1 },
    { 'source': 'Mabeuf', 'target': 'Gavroche', 'value': 1 },
    { 'source': 'Enjolras', 'target': 'Marius', 'value': 7 },
    { 'source': 'Enjolras', 'target': 'Gavroche', 'value': 7 },
    { 'source': 'Enjolras', 'target': 'Javert', 'value': 6 },
    { 'source': 'Enjolras', 'target': 'Mabeuf', 'value': 1 },
    { 'source': 'Enjolras', 'target': 'Valjean', 'value': 4 },
    { 'source': 'Combeferre', 'target': 'Enjolras', 'value': 15 },
    { 'source': 'Combeferre', 'target': 'Marius', 'value': 5 },
    { 'source': 'Combeferre', 'target': 'Gavroche', 'value': 6 },
    { 'source': 'Combeferre', 'target': 'Mabeuf', 'value': 2 },
    { 'source': 'Prouvaire', 'target': 'Gavroche', 'value': 1 },
    { 'source': 'Prouvaire', 'target': 'Enjolras', 'value': 4 },
    { 'source': 'Prouvaire', 'target': 'Combeferre', 'value': 2 },
    { 'source': 'Feuilly', 'target': 'Gavroche', 'value': 2 },
    { 'source': 'Feuilly', 'target': 'Enjolras', 'value': 6 },
    { 'source': 'Feuilly', 'target': 'Prouvaire', 'value': 2 },
    { 'source': 'Feuilly', 'target': 'Combeferre', 'value': 5 },
    { 'source': 'Feuilly', 'target': 'Mabeuf', 'value': 1 },
    { 'source': 'Feuilly', 'target': 'Marius', 'value': 1 },
    { 'source': 'Courfeyrac', 'target': 'Marius', 'value': 9 },
    { 'source': 'Courfeyrac', 'target': 'Enjolras', 'value': 17 },
    { 'source': 'Courfeyrac', 'target': 'Combeferre', 'value': 13 },
    { 'source': 'Courfeyrac', 'target': 'Gavroche', 'value': 7 },
    { 'source': 'Courfeyrac', 'target': 'Mabeuf', 'value': 2 },
    { 'source': 'Courfeyrac', 'target': 'Eponine', 'value': 1 },
    { 'source': 'Courfeyrac', 'target': 'Feuilly', 'value': 6 },
    { 'source': 'Courfeyrac', 'target': 'Prouvaire', 'value': 3 },
    { 'source': 'Bahorel', 'target': 'Combeferre', 'value': 5 },
    { 'source': 'Bahorel', 'target': 'Gavroche', 'value': 5 },
    { 'source': 'Bahorel', 'target': 'Courfeyrac', 'value': 6 },
    { 'source': 'Bahorel', 'target': 'Mabeuf', 'value': 2 },
    { 'source': 'Bahorel', 'target': 'Enjolras', 'value': 4 },
    { 'source': 'Bahorel', 'target': 'Feuilly', 'value': 3 },
    { 'source': 'Bahorel', 'target': 'Prouvaire', 'value': 2 },
    { 'source': 'Bahorel', 'target': 'Marius', 'value': 1 },
    { 'source': 'Bossuet', 'target': 'Marius', 'value': 5 },
    { 'source': 'Bossuet', 'target': 'Courfeyrac', 'value': 12 },
    { 'source': 'Bossuet', 'target': 'Gavroche', 'value': 5 },
    { 'source': 'Bossuet', 'target': 'Bahorel', 'value': 4 },
    { 'source': 'Bossuet', 'target': 'Enjolras', 'value': 10 },
    { 'source': 'Bossuet', 'target': 'Feuilly', 'value': 6 },
    { 'source': 'Bossuet', 'target': 'Prouvaire', 'value': 2 },
    { 'source': 'Bossuet', 'target': 'Combeferre', 'value': 9 },
    { 'source': 'Bossuet', 'target': 'Mabeuf', 'value': 1 },
    { 'source': 'Bossuet', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Joly', 'target': 'Bahorel', 'value': 5 },
    { 'source': 'Joly', 'target': 'Bossuet', 'value': 7 },
    { 'source': 'Joly', 'target': 'Gavroche', 'value': 3 },
    { 'source': 'Joly', 'target': 'Courfeyrac', 'value': 5 },
    { 'source': 'Joly', 'target': 'Enjolras', 'value': 5 },
    { 'source': 'Joly', 'target': 'Feuilly', 'value': 5 },
    { 'source': 'Joly', 'target': 'Prouvaire', 'value': 2 },
    { 'source': 'Joly', 'target': 'Combeferre', 'value': 5 },
    { 'source': 'Joly', 'target': 'Mabeuf', 'value': 1 },
    { 'source': 'Joly', 'target': 'Marius', 'value': 2 },
    { 'source': 'Grantaire', 'target': 'Bossuet', 'value': 3 },
    { 'source': 'Grantaire', 'target': 'Enjolras', 'value': 3 },
    { 'source': 'Grantaire', 'target': 'Combeferre', 'value': 1 },
    { 'source': 'Grantaire', 'target': 'Courfeyrac', 'value': 2 },
    { 'source': 'Grantaire', 'target': 'Joly', 'value': 2 },
    { 'source': 'Grantaire', 'target': 'Gavroche', 'value': 1 },
    { 'source': 'Grantaire', 'target': 'Bahorel', 'value': 1 },
    { 'source': 'Grantaire', 'target': 'Feuilly', 'value': 1 },
    { 'source': 'Grantaire', 'target': 'Prouvaire', 'value': 1 },
    { 'source': 'MotherPlutarch', 'target': 'Mabeuf', 'value': 3 },
    { 'source': 'Gueulemer', 'target': 'Thenardier', 'value': 5 },
    { 'source': 'Gueulemer', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Gueulemer', 'target': 'Mme.Thenardier', 'value': 1 },
    { 'source': 'Gueulemer', 'target': 'Javert', 'value': 1 },
    { 'source': 'Gueulemer', 'target': 'Gavroche', 'value': 1 },
    { 'source': 'Gueulemer', 'target': 'Eponine', 'value': 1 },
    { 'source': 'Babet', 'target': 'Thenardier', 'value': 6 },
    { 'source': 'Babet', 'target': 'Gueulemer', 'value': 6 },
    { 'source': 'Babet', 'target': 'Valjean', 'value': 1 },
    { 'source': 'Babet', 'target': 'Mme.Thenardier', 'value': 1 },
    { 'source': 'Babet', 'target': 'Javert', 'value': 2 },
    { 'source': 'Babet', 'target': 'Gavroche', 'value': 1 },
    { 'source': 'Babet', 'target': 'Eponine', 'value': 1 },
    { 'source': 'Claquesous', 'target': 'Thenardier', 'value': 4 },
    { 'source': 'Claquesous', 'target': 'Babet', 'value': 4 },
    { 'source': 'Claquesous', 'target': 'Gueulemer', 'value': 4 },
    { 'source': 'Claquesous', 'target': 'Valjean', 'value': 1 },
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
