import React, { Component } from "react";
import {
  List,
  Header,
  Input,
  Icon,
  Grid,
  Modal,
  Form,
  Button
} from "semantic-ui-react";
import RoomListItem from "./RoomListItem";
import { add_room } from "../../utils";
import { AuthContext } from "../../AuthProvider";

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
        <List.Header as={Header}>Your Rooms</List.Header>

        {roomListItems}
        <Icon
          id="add_room_icon"
          link
          name="add circle"
          onClick={this.onClick}
        ></Icon>
      </List>
    );
  }
}
export default RoomList;
