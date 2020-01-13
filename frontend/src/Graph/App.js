import React from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import GraphSVG from './GraphSVG';
import config from '../config';
import downloadData from '../Api';

import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.graphTypes = ['Sellers', 'Tank'];
    this.state = {
      dataset: null,
      graphType: this.graphTypes[0],
      kCore: 0,
      tankType: '',
      counter: 0,
      selectedCountries: [],
      allianceOnly: false
    };
  }

  componentDidUpdate() {
    if (!this.state.tankType) {
      this.setState({ tankType: this.props.tankTypes[0] });
    }
  }

  render() {
    const { graphType } = this.state;

    if (graphType === 'Sellers') {
      const form = this.getSellersForm();
      const view = this.createView(form);
      return view;
    } else {
      const form = this.getTankForm();
      const view = this.createView(form);
      return view;
    }
  }

  async handleButtonClick() {
    const {
      kCore,
      tankType,
      graphType,
      selectedCountries,
      allianceOnly
    } = this.state;
    console.log(this.state);

    let dataset;

    if (graphType === 'Sellers') {
      const params = { country_names: selectedCountries, k_core: kCore };
      dataset = await downloadData(config.API_ENDPOINTS.SELLERSGRAPH, params);
    } else {
      const params = {
        k_core: kCore,
        tank_name: tankType,
        alliance_only: allianceOnly
      };
      dataset = await downloadData(config.API_ENDPOINTS.TANKGRAPH, params);
    }

    if (!dataset || dataset.nodes.length === 0) {
      toast.info('No data for current query 😟!', {
        position: 'top-right',
        autoClose: 2000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true
      });
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

  handleCountryChange(event) {
    const countries = [];
    for (const el of event.target.selectedOptions) {
      countries.push(el.value);
    }
    this.setState({ selectedCountries: countries });
  }

  /**
   * Create main view of this component.
   * @param {*} formInputs - graph form
   */
  createView(formInputs) {
    const { graphTypes } = this;
    const view = (
      <>
        <Row>
          <Col xs={3}>
            <Form>
              <Form.Group controlId="type">
                <Form.Label>Graph type</Form.Label>
                <Form.Control
                  as="select"
                  onChange={event => this.handleGraphTypeChange(event)}
                >
                  {graphTypes.map(element => (
                    <option>{element}</option>
                  ))}
                </Form.Control>
              </Form.Group>
              {formInputs}
              <Button onClick={() => this.handleButtonClick()}>Update</Button>
            </Form>
          </Col>
          <Col>
            <GraphSVG dataset={this.state.dataset}></GraphSVG>
          </Col>
        </Row>
        <ToastContainer
          position="top-right"
          autoClose={2000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnVisibilityChange={false}
          draggable
          pauseOnHover
        />
      </>
    );
    return view;
  }

  /**
   * Creates a form for Sellers Graph Type.
   */
  getSellersForm() {
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
        <Form.Group controlId="k-core">
          <Form.Label>K-core</Form.Label>
          <Form.Control
            type="text"
            value={this.state.kCore}
            onChange={event => this.handleKcoreChange(event)}
          ></Form.Control>
        </Form.Group>
      </>
    );
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
            {tankTypes.map(element => (
              <option>{element}</option>
            ))}
          </Form.Control>
        </Form.Group>
        <Form.Group controlId="k-core">
          <Form.Label>K-core</Form.Label>
          <Form.Control
            type="text"
            value={this.state.kCore}
            onChange={event => this.handleKcoreChange(event)}
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
            {tankTypes.map(element => (
              <option>{element}</option>
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
}

export default App;
