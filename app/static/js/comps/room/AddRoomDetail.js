import React, { Component } from "react";
import { Form } from "semantic-ui-react";
import { add_room } from "../../utils";
import { AuthContext } from "../../AuthProvider";

class AddRoomDetail extends Component {
  static contextType = AuthContext;

  constructor(props) {
    console.log("AddRoomDetail constructor");
    super(props);

    this.state = { new_room: "" };
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

  render() {
    const { new_room } = this.state;
    return (
      <Form onSubmit={this.handleSubmit}>
        <Form.Group inline>
          <Form.Input
            placeholder="Room Name"
            onChange={this.handleChange}
            value={new_room}
          ></Form.Input>
          <Form.Button positive>Create</Form.Button>
        </Form.Group>
      </Form>
    );
  }
}

export default AddRoomDetail;
