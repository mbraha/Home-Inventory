import React, { Component } from "react";
import { Switch, Route } from "react-router-dom";
import RegisterForm from "./comps/Register";
import LoginForm from "./comps/Login";

class App extends Component {
  state = {
    current_user: "",
    isLoggedIn: false,
    access_token: null,
    refresh_token: null
  };

  setLoggedInStatus = status => {
    if (status.hasOwnProperty("error")) {
      console.log("status has error");
      this.setState({ isLoggedIn: false });
    } else {
      // console.log("status", status);
      this.setState({
        isLoggedIn: true,
        access_token: status.access_token,
        refresh_token: status.refresh_token
      });
    }
  };

  render() {
    console.log("APP state", this.state);
    const { isLoggedIn } = this.state;
    return (
      <Switch>
        <Route exact path="/">
          <h1>home!</h1>
        </Route>

        <Route path="/register">
          <RegisterForm
            setLoggedInStatus={this.setLoggedInStatus}
            isLoggedIn={isLoggedIn}
          />
        </Route>

        <Route path="/login">
          <LoginForm
            setLoggedInStatus={this.setLoggedInStatus}
            isLoggedIn={isLoggedIn}
          />
        </Route>
      </Switch>
    );
  }
}

export default App;
