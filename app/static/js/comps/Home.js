import React, { Component } from "react";
import Greeter from "./Greeter";

class HomePage extends Component {
  render() {
    console.log("Homepage render");
    return <Greeter></Greeter>;
  }
}

export default HomePage;
