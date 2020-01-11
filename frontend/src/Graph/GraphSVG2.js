import React from 'react';
import * as d3 from 'd3';

class Graph extends React.Component {
  constructor(props) {
    super(props);
    this.ref = React.createRef();
    this.margin = { top: 10, right: 30, bottom: 30, left: 40 };
    this.width = 400 - this.margin.left - this.margin.right;
    this.height = 400 - this.margin.top - this.margin.bottom;
  }

  componentDidUpdate() {
    console.log('Update');
    if (this.props.dataset !== null) this.drawGraph();
  }

  async componentDidMount() {
    this.svg = d3
      .select(this.ref.current)
      .append('svg')
      .attr('width', this.width)
      .attr('height', this.height);

    this.simulation = d3
      .forceSimulation(this.props.dataset.nodes)
      .gravity(0.05)
      .distance(100)
      .charge(-100)
      .size([this.width, this.height]);
  }

  drawGraph() {
    const margin = this.margin;
    const width = this.width;
    const height = this.height;
    const dataset = this.props.dataset;
    console.log('dataset', dataset.links);

    this.svg.selectAll('*').remove();

    this.simulation
      .nodes(dataset.nodes)
      .links(dataset.links)
      .start();

    // Initialize the links
    const link = this.svg
      .selectAll('.link')
      .data(dataset.links)
      .enter()
      .append('line')
      .attr('class', 'link')
      .style('stroke', '#aaa');

    // Initialize the nodes
    const node = this.svg
      .selectAll('.node')
      .data(dataset.nodes)
      .enter()
      .append('g')
      .attr('class', 'node')
      .call(this.simulation.drag);

    node
      .append('circle')
      .attr('r', 20)
      .style('fill', '#69b3a2')
      .on('mouseover', data => console.log(data.name));

    node
      .append('text')
      .attr('dx', 12)
      .attr('dy', '.35em')
      .text(() => 'test');

    this.simulation.on('tick', function() {
      link
        .attr('x1', function(d) {
          return d.source.x;
        })
        .attr('y1', function(d) {
          return d.source.y;
        })
        .attr('x2', function(d) {
          return d.target.x;
        })
        .attr('y2', function(d) {
          return d.target.y;
        });
    });

    // // Let's list the force we wanna apply on the network
    // this.simulation = d3
    //   .forceSimulation(dataset.nodes) // Force algorithm is applied to data.nodes
    //   .force(
    //     'link',
    //     d3
    //       .forceLink() // This force provides links between nodes
    //       .id(function(d) {
    //         return d.id;
    //       }) // This provide  the id of a node
    //       .links(dataset.links) // and this the list of links
    //   )
    //   .force('charge', d3.forceManyBody().strength(-400)) // This adds repulsion between nodes. Play with the -400 for the repulsion strength
    //   .force('center', d3.forceCenter(width / 2, height / 2)) // This force attracts nodes to the center of the svg area
    //   .on('tick', ticked);

    // this.rerunSim();

    // // This function is run at each iteration of the force algorithm, updating the nodes position.
    // function ticked() {
    //   link
    //     .attr('x1', function(d) {
    //       return d.source.x;
    //     })
    //     .attr('y1', function(d) {
    //       return d.source.y;
    //     })
    //     .attr('x2', function(d) {
    //       return d.target.x;
    //     })
    //     .attr('y2', function(d) {
    //       return d.target.y;
    //     });

    //   node
    //     .attr('cx', function(d) {
    //       return d.x + 6;
    //     })
    //     .attr('cy', function(d) {
    //       return d.y - 6;
    //     });
    // }
  }

  rerunSim(d) {
    this.simulation.alphaTarget(0.1).restart();
  }

  render() {
    return (
      <div>
        <div ref={this.ref}></div>
      </div>
    );
  }
}

export default Graph;
