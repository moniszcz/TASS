import React from 'react';

import GraphSVG from './GraphSVG';

import graph1 from '../data/graphs/graph1';
import graph2 from '../data/graphs/graph2';
import config from '../config';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.graphTypes = ['Alliance', 'Tank'];
    this.tankTypes = ['Foo', 'Bar'];
    this.tmp = true;
    this.state = {
      dataset: null,
      graphType: this.graphTypes[0],
      kCore: '',
      tynkType: '',
      counter: 0
    };
  }

  async componentDidMount() {
    const dataset = await this.downloadGraphData('dataset1');
    console.log(dataset);
    this.setState({ dataset });
  }

  async downloadGraphData(datasetOption) {
    if (config.ENVDEV) {
      const url = `${config.ENVAPIURL}/${datasetOption}`;
      const response = await fetch(url);
      const dataset = await response.json();
      return dataset;
    }
  }

  async updateData() {
    const dataset = await this.downloadGraphData('dataset2');
    await this.setState({ dataset });
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

  /**
   * Create main view of this component.
   * @param {*} formInputs - graph form
   */
  createView(formInputs) {
    const { graphTypes } = this;
    const view = (
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
            <Button onClick={() => this.updateData()}>Update</Button>
          </Form>
        </Col>
        <Col>
          <GraphSVG dataset={this.state.dataset}></GraphSVG>
        </Col>
      </Row>
    );
    return view;
  }

  /**
   * Creates a form for Alliance Graph Type.
   */
  getAllianceForm() {
    return (
      <Form.Group controlId="k-core">
        <Form.Label>K-core</Form.Label>
        <Form.Control
          type="text"
          value={this.state.kCore}
          onChange={event => this.handleKcoreChange(event)}
        ></Form.Control>
      </Form.Group>
    );
  }

  /**
   * Creates form for Tank Graph Type
   */
  getTankForm() {
    const { tankTypes } = this;
    return (
      <>
        <Form.Group controlId="k-core">
          <Form.Label>K-core</Form.Label>
          <Form.Control
            type="text"
            value={this.state.kCore}
            onChange={event => this.handleKcoreChange(event)}
          ></Form.Control>
        </Form.Group>
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
      </>
    );
  }

  render() {
    const { graphTypes } = this;
    const { dataset, graphType, kCore } = this.state;

    if (graphType === 'Alliance') {
      const form = this.getAllianceForm();
      const view = this.createView(form);
      return view;
    } else {
      const form = this.getTankForm();
      const view = this.createView(form);
      return view;
    }
  }
}

export default App;
