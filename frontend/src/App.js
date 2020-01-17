import React from 'react';
import './App.css';
import 'react-toastify/dist/ReactToastify.css';

import Home from './Home';

import { default as GraphView } from './Graph/App';
import { default as BarChart } from './Bar/App';

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { LinkContainer } from 'react-router-bootstrap';

import downloadData from './utils/Api';
import config from './config';

import {
  createLoadingDataToast,
  getToastContainer,
  dismissToasts
} from './utils/Toast';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tankTypes: [],
      countries: [],
      sellers: []
    };
  }

  async componentDidMount() {
    createLoadingDataToast();
    let response = await Promise.all([
      await downloadData(config.API_ENDPOINTS.TANKTYPES, {}),
      await downloadData(config.API_ENDPOINTS.COUNTRIES, {}),
      await downloadData(config.API_ENDPOINTS.SELLERS, {})
    ]);
    dismissToasts();
    console.log('response', response);
    const { tankTypes } = response[0];
    const { countries } = response[1];
    const { sellers } = response[2];
    console.log(sellers);
    this.setState({ tankTypes, countries, sellers });
  }

  render() {
    const toastContainer = getToastContainer();

    return (
      <Router>
        <div className="App">
          <Navbar bg="dark" variant="dark" expand="lg">
            <LinkContainer to="/">
              <Navbar.Brand>Tankify</Navbar.Brand>
            </LinkContainer>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
              <Nav className="mr-auto">
                <LinkContainer to="/graphs">
                  <Nav.Link>Graphs</Nav.Link>
                </LinkContainer>
                <LinkContainer to="/bars">
                  <Nav.Link>Bar Charts</Nav.Link>
                </LinkContainer>
              </Nav>
            </Navbar.Collapse>
          </Navbar>
          {toastContainer}
          <Container>
            <Switch>
              <Route path="/graphs">
                <GraphView
                  tankTypes={this.state.tankTypes}
                  countries={this.state.countries}
                  sellers={this.state.sellers}
                ></GraphView>
              </Route>
              <Route path="/bars">
                <BarChart
                  tankTypes={this.state.tankTypes}
                  countries={this.state.countries}
                ></BarChart>
              </Route>
              <Route path="/">
                <Home />
              </Route>
            </Switch>
          </Container>
        </div>
      </Router>
    );
  }
}

export default App;
