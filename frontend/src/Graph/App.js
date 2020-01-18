import React from 'react';

import GraphSVG from './GraphSVG';
import config from '../config';
import downloadData from '../utils/Api';

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';
import Select from 'react-select';
import { getToastContainer, createNoDataToast } from '../utils/Toast';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.graphTypes = ['Sellers', 'Tank', 'Alliance'];
    this.state = {
      isLoading: false,
      dataset: null,
      graphType: this.graphTypes[0],
      kCore: 0,
      tankType: 'AMX-13',
      counter: 0,
      selectedCountry: 'Argentina',
      allianceOnly: false,
      selectedCountries: [],
      kCoreOption: false
    };
  }

  componentDidMount() {
    if (this.state.tankType === '' && this.props.tankTypes) {
      this.setState({ tankType: this.props.tankTypes[0] });
    }
    if (this.state.selectedCountry === '' && this.props.sellers) {
      this.setState({ selectedCountry: this.props.sellers[0] });
    }
  }

  render() {
    const { graphType } = this.state;

    if (graphType === 'Sellers') {
      const form = this.getSellersForm();
      const view = this.createView(form);
      return view;
    } else if (graphType === 'Tank') {
      const form = this.getTankForm();
      const view = this.createView(form);
      return view;
    } else {
      const form = this.getAllianceForm();
      const view = this.createView(form);
      return view;
    }
  }

  async handleButtonClick() {
    const {
      kCore,
      kCoreOption,
      tankType,
      graphType,
      selectedCountry,
      allianceOnly,
      selectedCountries
    } = this.state;

    let dataset;

    this.setState({ isLoading: true });
    if (graphType === 'Sellers') {
      const params = {
        country_name: selectedCountry
      };
      dataset = await downloadData(config.API_ENDPOINTS.SELLERSGRAPH, params);
    } else if (graphType === 'Tank') {
      const params = {
        k_core: kCore,
        tank_name: tankType,
        alliance_only: allianceOnly
      };
      dataset = await downloadData(config.API_ENDPOINTS.TANKGRAPH, params);
    } else {
      const params = {
        country_names: selectedCountries,
        k_core: kCore,
        k_core_option: kCoreOption
      };
      dataset = await downloadData(config.API_ENDPOINTS.ALLIANCEGRAPH, params);
    }
    this.setState({ isLoading: false });

    if (!dataset || dataset.nodes.length === 0) {
      createNoDataToast();
    } else {
      this.setState({ dataset });
    }
  }

  handleKcoreChange(event) {
    const isInt = /^[0-9]+$/;
    if (isInt.test(event.target.value) || event.target.value === '')
      this.setState({ kCore: event.target.value });
  }

  handleGraphTypeChange(event) {
    this.setState({ graphType: event.target.value });
  }

  handleTankTypeChange(event) {
    this.setState({ tankType: event.target.value });
  }
  handleAllianceOnlyChange(event) {
    this.setState({ allianceOnly: event.target.checked });
  }
  handleKcoreOptionChange(event) {
    this.setState({ kCoreOption: event.target.checked });
  }

  handleCountryChange(event) {
    this.setState({ selectedCountry: event.target.value });
  }

  handleCountriesChange = selectedOptions => {
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
    this.handleButtonClick();
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
   * Create main view of this component.
   * @param {*} formInputs - graph form
   */
  createView(formInputs) {
    const { graphTypes } = this;
    const { graphType } = this.state;
    const toastContainer = getToastContainer();
    const button = this.getButton();
    let target;
    if (graphType === 'Sellers') {
      target = this.state.selectedCountry;
    } else {
      target = this.state.tankType;
    }
    const view = (
      <>
        <Row>
          <Col xs={3}>
            <Form onSubmit={event => this.handleSubmit(event)}>
              <Form.Group controlId="type">
                <Form.Label>Graph type</Form.Label>
                <Form.Control
                  as="select"
                  onChange={event => this.handleGraphTypeChange(event)}
                >
                  {graphTypes.map((element, i) => (
                    <option key={i}>{element}</option>
                  ))}
                </Form.Control>
              </Form.Group>
              {formInputs}
              {button}
            </Form>
          </Col>
          <Col>
            <GraphSVG dataset={this.state.dataset} target={target}></GraphSVG>
          </Col>
        </Row>
        {toastContainer}
      </>
    );
    return view;
  }

  /**
   * Creates a form for Sellers Graph Type.
   */
  getSellersForm() {
    const { sellers } = this.props;
    const form = (
      <>
        <Form.Group controlId="type">
          <Form.Label>Country</Form.Label>
          <Form.Control
            as="select"
            value={this.state.selectedCountry}
            onChange={event => this.handleCountryChange(event)}
          >
            {sellers.map((element, i) => (
              <option key={i}>{element}</option>
            ))}
          </Form.Control>
        </Form.Group>
      </>
    );
    return form;
  }

  /**
   * Creates form for Tank Graph Type
   */
  getTankForm() {
    const { tankTypes } = this.props;
    const formWithAllianceOnly = (
      <>
        <Form.Group controlId="type">
          <Form.Label>Tank</Form.Label>
          <Form.Control
            as="select"
            onChange={event => this.handleTankTypeChange(event)}
          >
            {tankTypes.map((element, i) => (
              <option key={i}>{element}</option>
            ))}
          </Form.Control>
        </Form.Group>
        <Form.Group controlId="k-core">
          <Form.Label>K-core</Form.Label>
          <Form.Control
            type="text"
            value={this.state.kCore}
            onChange={event => this.handleKcoreChange(event)}
            onKeyPress={event => {
              if (event.key === 'Enter') {
                event.preventDefault();
                this.handleButtonClick();
              }
            }}
          ></Form.Control>
        </Form.Group>
        <Form.Group controlId="formBasicCheckbox">
          <Form.Check
            type="checkbox"
            label="Alliance only"
            checked={this.state.allianceOnly}
            onChange={event => this.handleAllianceOnlyChange(event)}
          />
        </Form.Group>
      </>
    );
    const formWithoutAllianceOnly = (
      <>
        <Form.Group controlId="type">
          <Form.Label>Tank</Form.Label>
          <Form.Control
            as="select"
            onChange={event => this.handleTankTypeChange(event)}
          >
            {tankTypes.map((element, i) => (
              <option key={i}>{element}</option>
            ))}
          </Form.Control>
        </Form.Group>
        <Form.Group controlId="formBasicCheckbox">
          <Form.Check
            type="checkbox"
            label="Alliance only"
            checked={this.state.allianceOnly}
            onChange={event => this.handleAllianceOnlyChange(event)}
          />
        </Form.Group>
      </>
    );

    if (this.state.allianceOnly) return formWithAllianceOnly;
    else return formWithoutAllianceOnly;
  }

  getAllianceForm() {
    const { countries } = this.props;
    const formWithKcore = (
      <>
        <Form.Group controlId="country">
          <Form.Label>Country</Form.Label>
          <Select
            options={countries.map(element => {
              return { value: element, label: element };
            })}
            isMulti
            onChange={this.handleCountriesChange}
          />
        </Form.Group>
        <Form.Group controlId="k-core">
          <Form.Label>K-core</Form.Label>
          <Form.Control
            type="text"
            value={this.state.kCore}
            onChange={event => this.handleKcoreChange(event)}
            onKeyPress={event => {
              if (event.key === 'Enter') {
                event.preventDefault();
                this.handleButtonClick();
              }
            }}
          ></Form.Control>
        </Form.Group>
        <Form.Group controlId="formBasicCheckbox">
          <Form.Check
            type="checkbox"
            label="K-core"
            checked={this.state.kCoreOption}
            onChange={event => this.handleKcoreOptionChange(event)}
          />
        </Form.Group>
      </>
    );
    const formWithoutKcore = (
      <>
        <Form.Group controlId="country">
          <Form.Label>Country</Form.Label>
          <Select
            options={countries.map(element => {
              return { value: element, label: element };
            })}
            isMulti
            onChange={this.handleCountriesChange}
          />
        </Form.Group>
        <Form.Group controlId="formBasicCheckbox">
          <Form.Check
            type="checkbox"
            label="K-core"
            checked={this.state.kCoreOption}
            onChange={event => this.handleKcoreOptionChange(event)}
          />
        </Form.Group>
      </>
    );

    if (this.state.kCoreOption) return formWithKcore;
    else return formWithoutKcore;
  }
}

export default App;
