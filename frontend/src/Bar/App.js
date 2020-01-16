import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart } from 'react-chartjs-2';

import 'chartjs-plugin-colorschemes';
import { Aspect6 } from 'chartjs-plugin-colorschemes/src/colorschemes/colorschemes.office';

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import Select from 'react-select';
import Spinner from 'react-bootstrap/Spinner';

import downloadData from '../utils/Api';

import config from '../config';
import { createNoDataToast, getToastContainer } from '../utils/Toast';

class App extends React.Component {
  constructor(props) {
    super(props);

    // Some Chart options.
    Chart.scaleService.updateScaleDefaults('linear', {
      ticks: {
        min: 0
      }
    });

    this.chartTypes = ['Owned Tanks', 'Owned/Exported Tanks', 'Types of Tanks'];

    this.state = {
      data: {},
      isLoading: false,
      chartType: this.chartTypes[0],
      tankType: '',
      threshold: 0,
      selectedCountries: ''
    };
  }

  componentDidMount() {
    if (!this.state.tankType) {
      this.setState({ tankType: this.props.tankTypes[0] });
    }
  }

  render() {
    const { chartType } = this.state;
    let form;
    if (chartType === this.chartTypes[0]) {
      form = this.getChart1Form();
    } else if (chartType === this.chartTypes[1]) {
      form = this.getChart2Form();
    } else {
      form = this.getChart3Form();
    }
    const view = this.createView(form);
    return view;
  }

  async handleButtonClick() {
    const { threshold, tankType, chartType, selectedCountries } = this.state;

    this.setState({ isLoading: true });
    let data;
    if (chartType === this.chartTypes[0]) {
      const params = { tank_name: tankType, threshold };
      data = await downloadData(config.API_ENDPOINTS.CHART1, params);
    } else if (chartType === this.chartTypes[1]) {
      const params = { country_names: selectedCountries };
      data = await downloadData(config.API_ENDPOINTS.CHART2, params);
    } else {
      const params = { country_names: selectedCountries };
      data = await downloadData(config.API_ENDPOINTS.CHART3, params);
    }
    this.setState({ isLoading: false });
    if (!data) {
      createNoDataToast();
    } else {
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

  handleCountryChange = selectedOptions => {
    if (selectedOptions) {
      const countries = [];
      for (const el of selectedOptions) {
        countries.push(el.value);
      }
      this.setState({ selectedCountries: countries });
    }
  };

  handleSubmit = e => {
    e.preventDefault();
  };
  getButton() {
    const { isLoading } = this.state;

    if (isLoading) {
      return (
        <Button onClick={() => this.handleButtonClick()}>
          <Spinner
            as="span"
            animation="border"
            size="sm"
            role="status"
            aria-hidden="true"
          />
          <span className="sr-only">Loading...</span>
        </Button>
      );
    } else {
      return <Button onClick={() => this.handleButtonClick()}>Update</Button>;
    }
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
          <Select
            options={countries.map(element => {
              return { value: element, label: element };
            })}
            isMulti
            onChange={this.handleCountryChange}
          />
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
          <Select
            options={countries.map(element => {
              return { value: element, label: element };
            })}
            isMulti
            onChange={this.handleCountryChange}
          />
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
    const toastContainer = getToastContainer();
    const button = this.getButton();
    const view = (
      <>
        <Row>
          <Col xs={3}>
            <Form onSubmit={event => this.handleSubmit(event)}>
              <Form.Group controlId="type">
                <Form.Label>Chart type</Form.Label>
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
              {button}
            </Form>
          </Col>
          <Col>
            <Bar
              data={this.state.data}
              width={10}
              height={8}
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
                },
                colorschemes: {
                  scheme: Aspect6
                }
              }}
            />
          </Col>
        </Row>
        {toastContainer}
      </>
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
