import React, { Component } from "react";
import Greeter from "./Greeter";
import { RoomView, AddRoomDetail } from "./room";
import { Grid, Divider } from "semantic-ui-react";
import { AuthContext } from "../AuthProvider";
import { get_user } from "../utils";

class HomePage extends Component {
  /*
  Home page is responsible for main UX. It knows the user and 
  their rooms.

  RoomView dictates what RoomDetail should show.
  */
  static contextType = AuthContext;
  constructor() {
    super();
    this.state = { rooms: [], current_room: null };

    console.log("HomePage constructor context", this.context);
  }

  async componentDidMount() {
    // Once we know the user name, obtain their info from DB.
    console.log("HomePage componentDidMount context", this.context);
    const { current_user } = this.context.state;
    if (current_user) {
      let u = await get_user(current_user);
      console.log("HomePage componentDidMount u", u);
      if (typeof u === "number") {
        console.log("HomePage componentDidMount error finding user.", u);
        this.context.setLoggedInStatus({ revoked: true });
      } else {
        console.log("HomePage componentDidMount user", u);
        // Load rooms into state
        if (u.rooms.length > 0) {
          this.setState({ rooms: u.rooms });
        }
      }
    }
  }

  addRoom = (new_room_name, stuff = {}) => {
    this.setState((prevState) => ({
      rooms: [...prevState.rooms, { name: new_room_name, stuff: stuff }],
      current_room: new_room_name,
    }));
  };

  setCurrentRoom = (new_room_name, stuff = {}) => {
    if (new_room_name == "add_room") {
      this.setState({ current_room: new_room_name });
    }
    // If this is a new room, add to list.
    // else if (!this.state.rooms.find((room) => room.name == new_room_name)) {
    //   console.log("setCurrentRoom new room", new_room_name);
    //   // A newly added room, which might have had stuff. Load into state
    //   this.setState((prevState) => ({
    //     rooms: [...prevState.rooms, { name: new_room_name, stuff: stuff }],
    //     current_room: new_room_name,
    //   }));
    // }
    else {
      this.setState({ current_room: new_room_name });
    }
  };

  render() {
    console.log("Homepage render context", this.context);
    console.log("Homepage render state", this.state);

    const { current_room } = this.state;

    let detailView;
    if (current_room === null) {
      // Don't show anything.
      detailView = <></>;
    } else if (current_room == "add_room") {
      // Show Add Room detail comp.
      detailView = <AddRoomDetail addRoom={this.addRoom}></AddRoomDetail>;
    }

    return (
      <Grid celled>
        <Grid.Row>
          <Greeter></Greeter>
        </Grid.Row>

        <Grid.Row>
          <Divider hidden>Div</Divider>
        </Grid.Row>

        <Grid.Row columns={3}>
          <Grid.Column width={4}>
            <Grid.Row>
              <RoomView
                addRoom={this.addRoom}
                rooms={this.state.rooms}
                setCurrentRoom={this.setCurrentRoom}
              ></RoomView>
            </Grid.Row>
          </Grid.Column>

          <Grid.Column width={2}>
            <Divider hidden vertical>
              Div
            </Divider>
          </Grid.Column>

          <Grid.Column width={6}>{detailView}</Grid.Column>
        </Grid.Row>
      </Grid>
    );
  }
}

export default HomePage;
