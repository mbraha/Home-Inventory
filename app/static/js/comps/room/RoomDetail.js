import React, { Component } from "react";
import { Checkbox, Table } from "semantic-ui-react";

class RoomDetail extends Component {
  unpackStuff = (stuff) => {
    console.log("unpackStuff", stuff);
    let items = [];
    for (let name in stuff) {
      items.push({ name: name, value: stuff[name] });
    }
    console.log("items", items);
    return items;
  };

  render() {
    console.log("RoomDetail props", this.props);
    const { name: room_name, stuff } = this.props.room;
    // const propRoom = { name: "den", stuff: { bed: "500", lamp: "70" } };
    const items = this.unpackStuff(stuff);
    let itemRows = items.map((item, index) => (
      <Table.Row key={index}>
        <Table.Cell>{item.name}</Table.Cell>
        <Table.Cell>${item.value}</Table.Cell>
        <Table.Cell>
          <Checkbox name={item.name} onChange={this.onChangeEditBox}></Checkbox>
        </Table.Cell>
      </Table.Row>
    ));
    return (
      <Table celled>
        <Table.Header>
          <Table.Row>
            <Table.HeaderCell colSpan="2">{room_name}</Table.HeaderCell>
          </Table.Row>
          <Table.Row>
            <Table.HeaderCell>Name</Table.HeaderCell>
            <Table.HeaderCell>Value</Table.HeaderCell>
            <Table.HeaderCell>Edit</Table.HeaderCell>
          </Table.Row>
        </Table.Header>

        <Table.Body>{itemRows}</Table.Body>
      </Table>
    );
  }
}

export default RoomDetail;
