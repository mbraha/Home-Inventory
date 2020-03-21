import React, { Component } from "react";
import { Menu } from "semantic-ui-react";
import { full_logout } from "../utils";

class LogoutButton extends Component {
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
    return (
      <Menu.Item content="Logout" onClick={this.onClick}>
        Logout
      </Menu.Item>
    );
  }
}

export default LogoutButton;
