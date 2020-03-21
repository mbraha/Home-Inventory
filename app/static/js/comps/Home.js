import React, { Component } from "react";
import Greeter from "./Greeter";
import { Grid, Divider, Header } from "semantic-ui-react";

class HomePage extends Component {
  render() {
    console.log("Homepage render");
    return (
      <Grid celled>
        <Grid.Row>
          <Greeter></Greeter>
        </Grid.Row>
        <Grid.Row>
          <Divider hidden>Div</Divider>
        </Grid.Row>
        <Grid.Row columns={3}>
          <Grid.Column width={3}>
            <Grid.Row>
              <Header>Your Rooms</Header>
            </Grid.Row>
            <Grid.Row>Room 1</Grid.Row>
            <Grid.Row>Room 2</Grid.Row>
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
