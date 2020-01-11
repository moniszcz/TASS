import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'react-chartjs-2';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

class App extends React.Component {
  constructor(props) {
    super(props);
    Chart.scaleService.updateScaleDefaults('linear', {
      ticks: {
        min: 0
      }
    });
    this.state = {
      data: {
        labels: ['Poland', 'Germany', 'Russia'],
        datasets: [
          {
            label: 'Number of tanks',
            backgroundColor: 'rgba(255,99,132,0.2)',
            borderColor: 'rgba(255,99,132,1)',
            borderWidth: 2,
            hoverBackgroundColor: 'rgba(255,99,132,0.4)',
            hoverBorderColor: 'rgba(255,99,132,1)',
            data: [65, 59, 80]
          }
        ]
      }
    };
  }

  render() {
    return (
      <Row>
        <Col>
          <h2>Number of tanks in countries</h2>
          <Bar
            data={this.state.data}
            width={10}
            height={2}
            options={{
              maintainAspectRatio: true
            }}
          />
        </Col>
      </Row>
    );
  }
}

export default App;
