import React, { Component } from "react";
import { Menu } from "semantic-ui-react";
import { Link } from "react-router-dom";
import LogoutButton from "./Logout";
import { AuthContext } from "../AuthProvider";

class NavBar extends Component {
  static contextType = AuthContext;

  render() {
    console.log("NavBar render context", this.context);
    let rightMenu = null;
    if (this.context.state.isLoggedIn) {
      rightMenu = (
        <Menu.Menu position="right">
          <Menu.Item as={LogoutButton}></Menu.Item>
        </Menu.Menu>
      );
    } else {
      rightMenu = (
        <Menu.Menu position="right">
          <Menu.Item as={Link} to="/register">
            Register
          </Menu.Item>
          <Menu.Item as={Link} to="/login">
            Login
          </Menu.Item>
        </Menu.Menu>
      );
    }
    return (
      <Menu style={{ marginTop: "10px" }}>
        <Menu.Item header as={Link} to="/">
          Home-Inventory
        </Menu.Item>
        <Menu.Item>Rooms</Menu.Item>
        {rightMenu}
      </Menu>
    );
  }
}

export default NavBar;
