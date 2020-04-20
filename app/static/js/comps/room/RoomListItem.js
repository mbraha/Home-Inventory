import React, { Component } from "react";
import {
  List,
  Header,
  Input,
  Icon,
  Grid,
  Modal,
  Form,
  Button,
} from "semantic-ui-react";
import { add_room } from "../../utils";
import { AuthContext } from "../../AuthProvider";

class RoomListItem extends Component {
  constructor(props) {
    super(props);

    this.state = {
      name: "",
      items: [],
    };
  }

  render() {
    return (
      <List.Item
        header={this.props.name}
        description={"item count: " + Object.keys(this.props.stuff).length}
        onClick={this.onClick}
      ></List.Item>
    );
  }
}

export default RoomListItem;
