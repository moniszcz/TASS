import React from 'react';
import * as d3 from 'd3';
import './Graph.css';

// https://bl.ocks.org/heybignick/3faf257bbbbc7743bb72310d03b86ee8

class Graph extends React.Component {
  constructor(props) {
    super(props);
    this.ref = React.createRef();
    this.margin = { top: 10, right: 30, bottom: 30, left: 40 };
    this.width = 800 - this.margin.left - this.margin.right;
    this.height = 800 - this.margin.top - this.margin.bottom;
    this.previousDataset = null;
    this.strength = -30;
  }

  componentDidUpdate() {
    if (
      this.props.dataset !== null &&
      this.props.dataset !== this.previousDataset
    ) {
      this.previousDataset = this.props.dataset;
      if (this.props.dataset.links.length > 500) {
        this.strength = -400;
      } else {
        this.strength = -30;
      }
      this.drawGraph();
    }
  }

  async componentDidMount() {
    this.svg = d3
      .select(this.ref.current)
      .append('svg')
      .attr('width', this.width + this.margin.left + this.margin.right)
      .attr('height', this.height + this.margin.top + this.margin.bottom);
  }

  drawGraph() {
    const margin = this.margin;
    const width = this.width;
    const height = this.height;
    const xExtent = [50, width];
    const yExtent = [50, height];
    const dataset = this.props.dataset;

    this.svg.selectAll('*').remove();

    const simulation = d3
      .forceSimulation()
      .force(
        'link',
        d3.forceLink().id(function(d) {
          return d.id;
        })
      )
      .force('charge', d3.forceManyBody().strength(-1000))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('x', d3.forceX(width / 2))
      .force('y', d3.forceY(height / 2))
      .force('bounds', boxingForce);

    // Initialize the links
    const link = this.svg
      .append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(dataset.links)
      .enter()
      .append('line')
      .style('stroke', '#aaa');

    // Initialize the nodes
    const node = this.svg
      .append('g')
      .attr('class', 'nodes')
      .selectAll('g')
      .data(dataset.nodes)
      .enter()
      .append('g')
      .call(
        d3
          .drag()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended)
      );

    const circles = node
      .append('circle')
      .attr('r', 5)
      .style('fill', d => {
        if (d.name === this.props.target) return 'red';
        else return '#69b3a2';
      });

    const labels = node
      .append('text')
      .text(d => d.name)
      .attr('x', 6)
      .attr('y', 3);

    node.append('title').text(d => d.name);

    simulation.nodes(dataset.nodes).on('tick', ticked);
    simulation.force('link').links(dataset.links);

    function ticked() {
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

      node.attr('transform', function(d) {
        return 'translate(' + d.x + ',' + d.y + ')';
      });
    }

    function dragstarted(d) {
      d3.select(this).style('cursor', 'grabbing');
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }

    function dragended(d) {
      d3.select(this).style('cursor', 'grab');
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Custom force to put all nodes in a box
    function boxingForce() {
      const nodes = dataset.nodes;
      for (let node of nodes) {
        // Of the positions exceed the box, set them to the boundary position.
        // You may want to include your nodes width to not overlap with the box.
        node.x = Math.max(xExtent[0], Math.min(xExtent[1], node.x));
        node.y = Math.max(yExtent[0], Math.min(yExtent[1], node.y));
      }
    }

    // // Let's list the force we wanna apply on the network
    // const simulation = d3
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

    // // this.rerunSim();

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
