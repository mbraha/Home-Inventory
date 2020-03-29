import React, { Component } from "react";
import { List, Header, Button, Icon, Grid } from "semantic-ui-react";

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

  onClick = () => {
    console.log("icon clicked");
  };

  render() {
    return (
      <List divided relaxed selection size="large">
        <Grid padded>
          <Grid.Row>
            <Header>Your Rooms</Header>
            <Icon
              id="add_room_icon"
              link
              name="add circle"
              onClick={this.onClick}
            ></Icon>
          </Grid.Row>
        </Grid>

        <RoomListItem name="room1"></RoomListItem>
        <RoomListItem name="room2"></RoomListItem>
      </List>
    );
  }
}

export default RoomList;
