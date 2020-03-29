import React, { Component } from "react";
import Greeter from "./Greeter";
import RoomList from "./Room";
import { Grid, Divider } from "semantic-ui-react";
import { AuthContext } from "../AuthProvider";
import { get_users } from "../utils";

class HomePage extends Component {
  /*
  Home page is responsible for main UX. It knows the user and 
  their rooms.
  */
  static contextType = AuthContext;
  constructor() {
    super();
    this.state = { rooms: [] };

    console.log("HomePage constructor context", this.context);
  }

  componentDidMount() {
    // Good place to get user room info once they log in
    console.log("HomePage componentDidMount context", this.context);
    if (this.context.state.isLoggedIn) {
      // let temp = get_users();
      console.log("HomePage componentDidMount isLoggedIn");
    }
  }

  async componentDidUpdate() {
    console.log("HomePage componentDidUpdate", this.context);
    if (this.context.state.isLoggedIn) {
      console.log("HomePage componentDidUpdate isLoggedIn");
      let temp = await get_users();
      let user = temp.find(u => u.username == this.context.state.current_user);
      console.log("HomePage componentDidUpdate get_users user", user);
      // if (user.rooms.length > 0) {
      //   this.setState({});
      // }
    }
  }

  render() {
    console.log("Homepage render context", this.context);
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
              <RoomList></RoomList>
            </Grid.Row>
          </Grid.Column>

          <Grid.Column width={2}>
            <Divider hidden vertical>
              Div
            </Divider>
          </Grid.Column>

          <Grid.Column width={6}>ROOM DETAIL</Grid.Column>
        </Grid.Row>
      </Grid>
    );
  }
}

export default HomePage;
