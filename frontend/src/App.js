import React from 'react';
import './App.css';

import { default as GraphView } from './Graph/App';
import { default as BarChart } from './Bar/App';

import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedOption: 'graph'
    };
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

          <Chart type={selectedOption}></Chart>
        </Container>
      </div>
    );
  }
}

function Chart(props) {
  if (props.type === 'graph') {
    return <GraphView></GraphView>;
  } else {
    return <BarChart></BarChart>;
  }
}

export default App;
