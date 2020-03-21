import React, { Component } from "react";
import Layout from "./Layout";

class HomePage extends Component {
  render() {
    return (
      <Layout
        setLoggedInStatus={this.props.setLoggedInStatus}
        isLoggedIn={this.props.isLoggedIn}
      >
        <h1>home!</h1>
        <h2>Hello {this.props.current_user}</h2>
        {this.props.isLoggedIn ? (
          <h2> You're logged in :) </h2>
        ) : (
          <h2> You're not logged in :( </h2>
        )}
      </Layout>
    );
  }
}

export default HomePage;
