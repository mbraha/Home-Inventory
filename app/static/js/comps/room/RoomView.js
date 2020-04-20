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
import RoomListItem from "./RoomListItem";
import { add_room } from "../../utils";
import { AuthContext } from "../../AuthProvider";

class RoomView extends Component {
  static contextType = AuthContext;

  makeRoomItem = (props) => {};

  onClick = (event, data) => {
    console.log("onClick", event, data, this.props);
    this.props.setCurrentRoom(data.name);
  };

  render() {
    console.log("RoomView render props", this.props);
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
        <List.Item disabled>Empty :(</List.Item>
      );
    return (
      <List divided relaxed selection size="large">
        <List.Header as={Header}>Your Rooms</List.Header>
        <List.Item name="add_room" onClick={this.onClick}>
          <List.Content floated="left">Add Room</List.Content>
          <List.Icon name="plus"></List.Icon>
        </List.Item>

        {roomListItems}
      </List>
    );
  }
}
export default RoomView;
