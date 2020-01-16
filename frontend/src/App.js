import React from 'react';
import './App.css';
import 'react-toastify/dist/ReactToastify.css';

import Home from './Home';

import { default as GraphView } from './Graph/App';
import { default as BarChart } from './Bar/App';

import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';
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
      selectedOption: 'graph',
      tankTypes: [],
      countries: []
    };
  }

  async componentDidMount() {
    createLoadingDataToast();
    let response = await Promise.all([
      await downloadData(config.API_ENDPOINTS.TANKTYPES, {}),
      await downloadData(config.API_ENDPOINTS.COUNTRIES, {})
    ]);
    dismissToasts();
    const { tankTypes } = response[0];
    const { countries } = response[1];
    this.setState({ tankTypes, countries });
  }

  setSelectedOption(selectedOption) {
    this.setState({ selectedOption });
  }

  render() {
    const { selectedOption } = this.state;
    const toastContainer = getToastContainer();

    return (
      <Router>
        <div className="App">
          <Navbar bg="light" expand="lg">
            <LinkContainer to="/">
              <Navbar.Brand>React-Bootstrap</Navbar.Brand>
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
          <Container>
            <Switch>
              <Route path="/graphs">
                <GraphView
                  tankTypes={this.state.tankTypes}
                  countries={this.state.countries}
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
