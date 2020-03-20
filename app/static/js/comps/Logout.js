import React, { Component } from "react";
import { Button } from "semantic-ui-react";
import { Redirect } from "react-router-dom";
import { full_logout } from "../utils";

class Logout extends Component {
  constructor(props) {
    super(props);
  }

  onClick = () => {
    if (full_logout(this.props.access_token, this.props.refresh_token)) {
      console.log("logout onclick if block");
      this.props.setLoggedInStatus({ revoked: "user logging out" });
    }
  };

  render() {
    console.log("Logout props", this.props);
    if (!this.props.isLoggedIn) {
      console.log("redirecting away from logout");
      return <Redirect to="/" />;
    }
    return <Button content="Logout" onClick={this.onClick}></Button>;
  }
}

export default Logout;
