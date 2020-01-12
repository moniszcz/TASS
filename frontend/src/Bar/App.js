import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'react-chartjs-2';

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';

import downloadData from '../Api';

import config from '../config';

class App extends React.Component {
  constructor(props) {
    super(props);

    // Some Chart options.
    Chart.scaleService.updateScaleDefaults('linear', {
      ticks: {
        min: 0
      }
    });

    this.chartTypes = ['Chart1', 'Chart2', 'Chart3'];

    this.state = {
      data: {},
      chartType: this.chartTypes[0],
      tankType: '',
      threshold: 0,
      selectedCountries: ''
    };
  }

  componentDidUpdate() {
    if (!this.state.tankType) {
      this.setState({ tankType: this.props.tankTypes[0] });
    }
  }

  render() {
    const { chartType } = this.state;
    let form;
    if (chartType === 'Chart1') {
      form = this.getChart1Form();
    } else if (chartType === 'Chart2') {
      form = this.getChart2Form();
    } else {
      form = this.getChart3Form();
    }
    const view = this.createView(form);
    return view;
  }

  async handleButtonClick() {
    const { threshold, tankType, chartType, selectedCountries } = this.state;
    console.log('state', this.state);

    if (chartType === 'Chart1') {
      const params = { tank_name: tankType, threshold };
      const data = await downloadData(config.API_ENDPOINTS.CHART1, params);
      this.setState({ data });
    } else if (chartType === 'Chart2') {
      const params = { country_names: selectedCountries };
      const data = await downloadData(config.API_ENDPOINTS.CHART2, params);
      this.setState({ data });
    } else {
      const params = { country_names: selectedCountries };
      const data = await downloadData(config.API_ENDPOINTS.CHART3, params);
      this.setState({ data });
    }
  }

  handleChartTypeChange(event) {
    this.setState({ chartType: event.target.value });
  }

  handleTankTypeChange(event) {
    this.setState({ tankType: event.target.value });
  }

  handleThresholdChange(event) {
    const isInt = /^[0-9]+$/;
    if (isInt.test(event.target.value) || event.target.value === '')
      this.setState({ threshold: event.target.value });
  }

  handleCountryChange(event) {
    const countries = [];
    for (const el of event.target.selectedOptions) {
      countries.push(el.value);
    }
    this.setState({ selectedCountries: countries });
  }

  /**
   * Creates a form for Sellers Graph Type.
   */
  getChart1Form() {
    const { tankTypes } = this.props;
    return (
      <>
        <Form.Group controlId="type">
          <Form.Label>Tank</Form.Label>
          <Form.Control
            as="select"
            onChange={event => this.handleTankTypeChange(event)}
          >
            {tankTypes.map(element => (
              <option>{element}</option>
            ))}
          </Form.Control>
        </Form.Group>
        <Form.Group controlId="threshold">
          <Form.Label>threshold</Form.Label>
          <Form.Control
            type="text"
            value={this.state.threshold}
            onChange={event => this.handleThresholdChange(event)}
          ></Form.Control>
        </Form.Group>
      </>
    );
  }
  /**
   * Creates a form for Sellers Graph Type.
   */
  getChart2Form() {
    const { countries } = this.props;
    return (
      <>
        <Form.Group controlId="country">
          <Form.Label>Country</Form.Label>
          <Form.Control
            as="select"
            multiple
            onChange={event => this.handleCountryChange(event)}
          >
            {countries.map(element => (
              <option>{element}</option>
            ))}
          </Form.Control>
        </Form.Group>
      </>
    );
  }
  /**
   * Creates a form for Sellers Graph Type.
   */
  getChart3Form() {
    const { countries } = this.props;
    return (
      <>
        <Form.Group controlId="country">
          <Form.Label>Country</Form.Label>
          <Form.Control
            as="select"
            multiple
            onChange={event => this.handleCountryChange(event)}
          >
            {countries.map(element => (
              <option>{element}</option>
            ))}
          </Form.Control>
        </Form.Group>
      </>
    );
  }

  /**
   * Create main view of this component.
   * @param {*} formInputs - graph form
   */
  createView(formInputs) {
    const { chartTypes } = this;
    const view = (
      <Row>
        <Col xs={3}>
          <Form>
            <Form.Group controlId="type">
              <Form.Label>Graph type</Form.Label>
              <Form.Control
                as="select"
                onChange={event => this.handleChartTypeChange(event)}
              >
                {chartTypes.map(element => (
                  <option>{element}</option>
                ))}
              </Form.Control>
            </Form.Group>
            {formInputs}
            <Button onClick={() => this.handleButtonClick()}>Update</Button>
          </Form>
        </Col>
        <Col>
          <h2>Number of tanks in countries</h2>
          <Bar
            data={this.state.data}
            width={10}
            height={2}
            options={{
              maintainAspectRatio: true,
              scales: {
                xAxes: [
                  {
                    stacked: true
                  }
                ],
                yAxes: [
                  {
                    stacked: true
                  }
                ]
              }
            }}
          />
        </Col>
      </Row>
    );
    return view;
  }
}

export default App;

// const data =  {
//   labels: ['Poland', 'Germany', 'Russia'],
//   datasets: [
//     {
//       label: 'Number of tanks',
//       backgroundColor: 'rgba(255,99,132,0.2)',
//       borderColor: 'rgba(255,99,132,1)',
//       borderWidth: 2,
//       hoverBackgroundColor: 'rgba(255,99,132,0.4)',
//       hoverBorderColor: 'rgba(255,99,132,1)',
//       data: [65, 59, 80]
//     }
//   ]
// }
