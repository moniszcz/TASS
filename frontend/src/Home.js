import React from 'react';
import Image from 'react-bootstrap/Image';

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
      </>
    );
  }
}

export default Home;
