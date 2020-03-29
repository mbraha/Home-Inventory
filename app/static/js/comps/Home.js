import React, { Component } from "react";
import Greeter from "./Greeter";
import RoomList from "./Room";
import { Grid, Divider } from "semantic-ui-react";
import { AuthContext } from "../AuthProvider";

class HomePage extends Component {
  /*
  Home page is responsible for main UX. It knows the user and 
  their rooms.
  */
  static contextType = AuthContext;
  constructor(props) {
    super(props);

    console.log("HomePage constructor", props);
  }

  componentDidMount() {
    // Good place to get user room info once they log in
    console.log("HomePage componentDidMount", this.context);
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
