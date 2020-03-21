import React from "react";
import { Menu } from "semantic-ui-react";
import { Link } from "react-router-dom";
import LogoutButton from "./Logout";

export default props => {
  let rightMenu = <div></div>;
  if (props.isLoggedIn) {
    rightMenu = (
      <Menu.Menu position="right">
        <Menu.Item
          as={LogoutButton}
          setLoggedInStatus={props.setLoggedInStatus}
          isLoggedIn={props.isLoggedIn}
          access_token={props.access_token}
          refresh_token={props.refresh_token}
        ></Menu.Item>
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
      <Menu.Item as={Link} to="/">
        Home-Inventory
      </Menu.Item>
      <Menu.Item>Rooms</Menu.Item>
      {rightMenu}
    </Menu>
  );
};
