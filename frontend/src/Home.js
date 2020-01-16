import React from 'react';
import Image from 'react-bootstrap/Image';
import { LinkContainer } from 'react-router-bootstrap';
import Button from 'react-bootstrap/Button';

class Home extends React.Component {
  render() {
    return (
      <>
        <Image
          className="home--tank"
          src={process.env.PUBLIC_URL + 'tank.svg'}
          fluid
          rounded
        />
        <h1>Tankify</h1>
        <h2>Motto</h2>
        <h3>Some catchy text here</h3>
      </>
    );
  }
}

export default Home;
