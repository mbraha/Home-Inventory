import React, { Component } from "react";
import { List, Header, Input, Icon, Grid, Modal } from "semantic-ui-react";
import { add_room } from "../utils";
import { AuthContext } from "../AuthProvider";

class RoomListItem extends Component {
  constructor(props) {
    super(props);

    this.state = {
      name: "",
      items: []
    };
  }

  render() {
    return (
      <List.Item
        header={this.props.name}
        description={"item count: " + this.props.stuff.length}
        onClick={this.onClick}
      ></List.Item>
    );
  }
}

class RoomList extends Component {
  static contextType = AuthContext;

  makeRoomItem = props => {};

  onClick = (event, data) => {
    console.log("icon clicked", event, data);
    console.log("onClick", this.context);
    // add_room(this.context.state.current_user);
  };

  render() {
    console.log("RoomList render props", this.props);
    let roomListItems =
      this.props.rooms.length > 0 ? (
        this.props.rooms.map((room, index) => (
          <RoomListItem
            key={index}
            name={room.name}
            stuff={room.stuff}
          ></RoomListItem>
        ))
      ) : (
        <></>
      );
    return (
      <List divided relaxed selection size="large">
        <Grid celled padded>
          <Grid.Row>
            <Header>Your Rooms</Header>
            <Input></Input>
            <Icon
              id="add_room_icon"
              link
              name="add circle"
              onClick={this.onClick}
            ></Icon>
          </Grid.Row>
        </Grid>

        {roomListItems}
      </List>
    );
  }
}

export default RoomList;
