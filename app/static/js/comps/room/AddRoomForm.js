import React, { Component } from "react";
import { Form, Button, Container } from "semantic-ui-react";
import { add_room } from "../../utils";
import { AuthContext } from "../../AuthProvider";

class AddRoomForm extends Component {
  static contextType = AuthContext;

  constructor(props) {
    console.log("AddRoomForm constructor");
    super(props);

    this.state = { new_room: "", add_stuff_count: 0 };
  }

  handleChange = (event, { value }) => {
    this.setState({ new_room: value });
  };

  handleSubmit = async () => {
    console.log("AddRoom handleSubmit context", this.context);
    console.log("AddRoom handleSubmit state", this.state);
    const { new_room } = this.state;
    let res = await add_room(this.context.state.current_user, new_room);

    if (typeof res === "number") {
      console.log("AddRoom handleSubmit error", res);
    } else {
      // Room add success. Add to list and change detail view to it.
      console.log("AddRoom handleSubmit success", res);
      this.props.addRoom(new_room);
    }
  };

  onClickCancel = () => {
    this.props.setCurrentRoom();
  };

  onClickAddStuff = () => {
    console.log("more stuff clicked");
    this.setState({ add_stuff_count: this.state.add_stuff_count + 1 });
  };

  render() {
    console.log("AddRoomForm render state", this.state);
    const { new_room } = this.state;

    let tempArr = Array(this.state.add_stuff_count);
    console.log("tempArr", tempArr);

    /*
    Okay this is crazy. Why not a for loop? To learn!

    Using the count in state, create an array of that length filled
    with nulls. Map each null to the desired React element.
    1. Initialize array this way does not set values, only space.
    2. Map needs values to work on, or it returns nothing.
    */
    const addStuffFormField = Array(this.state.add_stuff_count)
      .fill(null)
      .map((item, index) => (
        <Form.Group key={index} widths={2}>
          <Form.Input placeholder="Item Name"></Form.Input>
          <Form.Input placeholder="Item Value"></Form.Input>
        </Form.Group>
      ));
    console.log("addStuffFormField", addStuffFormField);

    return (
      <Container>
        <Form onSubmit={this.handleSubmit}>
          <Form.Group inline>
            <Form.Field required>
              <Form.Input
                placeholder="Room Name"
                onChange={this.handleChange}
                value={new_room}
              ></Form.Input>
            </Form.Field>

            <Form.Button positive>Create</Form.Button>
            <Form.Button onClick={this.onClickCancel} negative>
              Cancel
            </Form.Button>
          </Form.Group>
          {addStuffFormField}
        </Form>
        <Button color="blue" onClick={this.onClickAddStuff}>
          More Stuff
        </Button>
      </Container>
    );
  }
}

export default AddRoomForm;
