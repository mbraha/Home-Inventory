import React, { Component } from "react";
import { List, Header } from "semantic-ui-react";

class RoomListItem extends Component {
  constructor(props) {
    super(props);
    console.log("RoomListItem constructor props", props);

    this.state = {
      name: "",
      items: []
    };
  }

  //   onClick = ()
  render() {
    console.log("RoomListItem render props", this.props);
    return (
      <List.Item
        header={this.props.name}
        description="item count"
        onClick={this.onClick}
      ></List.Item>
    );
  }
}

class RoomList extends Component {
  makeRoomItem = props => {};

  render() {
    return (
      <List divided relaxed selection size="large">
        <List.Item disabled>
          <Header>Your Rooms</Header>
        </List.Item>

        <RoomListItem name="room1"></RoomListItem>
        <RoomListItem name="room2"></RoomListItem>
      </List>
    );
  }
}

export default RoomList;
