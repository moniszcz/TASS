import React from 'react';
import './App.css';

import { default as GraphView } from './Graph/App';
import { default as BarChart } from './Bar/App';

import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';

import downloadData from './Api';
import config from './config';

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
    const { tankTypes } = await downloadData(
      config.API_ENDPOINTS.TANKTYPES,
      {}
    );
    const { countries } = await downloadData(
      config.API_ENDPOINTS.COUNTRIES,
      {}
    );
    this.setState({ tankTypes, countries });
  }

  setSelectedOption(selectedOption) {
    this.setState({ selectedOption });
  }

  render() {
    const { selectedOption } = this.state;

    return (
      <div className="App">
        <Container>
          <Row>
            <Col>
              <Row>
                <Col
                  className={selectedOption === 'graph' ? 'selected' : null}
                  onClick={() => this.setSelectedOption('graph')}
                >
                  <p href="#">Graph</p>
                </Col>
                <Col
                  className={selectedOption !== 'graph' ? 'selected' : null}
                  onClick={() => this.setSelectedOption('barChart')}
                >
                  <p href="#">Bar Chart</p>
                </Col>
              </Row>
            </Col>
          </Row>

          <Chart type={selectedOption} state={this.state}></Chart>
        </Container>
      </div>
    );
  }
}

function Chart(props) {
  const { tankTypes, countries } = props.state;
  if (props.type === 'graph') {
    return <GraphView tankTypes={tankTypes} countries={countries}></GraphView>;
  } else {
    return <BarChart tankTypes={tankTypes} countries={countries}></BarChart>;
  }
}

export default App;
