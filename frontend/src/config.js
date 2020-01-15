const config = {
  ENVDEV: window.location.href.match('localhost:3000') ? true : false,
  APIURL: 'http://127.0.0.1:5000',
  APIREMOTEURL: 'https://offpics.pythonanywhere.com',
  API_ENDPOINTS: {
    SELLERSGRAPH: 'sellersGraph',
    TANKGRAPH: 'tankGraph',
    CHART1: 'chart1',
    CHART2: 'chart2',
    CHART3: 'chart3',
    TANKTYPES: 'tankTypes',
    COUNTRIES: 'countries'
  }
};

export default config;
