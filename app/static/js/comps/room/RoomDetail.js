import React, { Component } from "react";
import {
  List,
  Header,
  Input,
  Icon,
  Grid,
  Modal,
  Item,
  Table
} from "semantic-ui-react";
import { add_room } from "../../utils";
import { AuthContext } from "../../AuthProvider";

class RoomDetail extends Component {
  render() {
    return (
      // <div></div>
      <Table celled striped>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell colSpan="2">Room Name</Table.HeaderCell>
          </Table.Row>
        </Table.Header>

        <Table.Body>
          <Table.Row>
            <Table.Cell>Item 1</Table.Cell>
            <Table.Cell>Value 1</Table.Cell>
          </Table.Row>
        </Table.Body>
      </Table>
    );
  }
}

export default RoomDetail;
