import React, { Component } from "react";
import { Switch, Route } from "react-router-dom";
import RegisterForm from "./comps/Register";

class App extends Component {
  state = {
    isLoggedIn: false,
    access_token: null,
    refresh_token: null
  };

  setLoggedInStatus = status => {
    if (status.hasOwnProperty("error")) {
      this.setState({ isLoggedIn: false });
    } else {
      this.setState({
        isLoggedIn: true,
        access_token: status.access_token,
        refresh_token: status.refresh_token
      });
    }
  };

  render() {
    console.log("APP state", this.state);
    return (
      <Switch>
        <Route path="/register">
          <RegisterForm setLoggedInStatus={this.setLoggedInStatus} />
        </Route>
        <Route path="/">
          <h1>home!</h1>
        </Route>
      </Switch>
    );
  }
}

export default App;
