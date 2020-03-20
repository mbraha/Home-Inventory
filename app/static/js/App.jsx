import React, { Component } from "react";
import { Switch, Route } from "react-router-dom";
import RegisterForm from "./comps/Register";
import LoginForm from "./comps/Login";
import Logout from "./comps/Logout";
import { get_new_access_token } from "./utils";

class App extends Component {
  state = {
    current_user: "",
    isLoggedIn: false,
    access_token: null,
    refresh_token: null,
    timer_id: null
  };

  async componentDidMount() {
    const refresh_token = localStorage.getItem("refresh_token");
    console.log("got token from storage", refresh_token);
    if (refresh_token === null) {
      // User needs to register/login
      return 0;
    } else {
      // Try and get a new access token
      const new_access_token = await get_new_access_token(refresh_token);
      console.log("App didMount new_token", new_access_token);
      if (new_access_token && new_access_token.hasOwnProperty("access_token")) {
        this.setState({
          isLoggedIn: true,
          access_token: new_access_token.access_token,
          refresh_token: refresh_token
        });
      } else {
        // Failed to get access token
        this.setState({
          refresh_token
        });
      }
      const timer_id = setInterval(() => this.silentRefresh(), 1000 * 60 * 14);
      this.setState({ timer_id });
    }
  }

  async silentRefresh() {
    console.log("silentRefresh");
    const { refresh_token } = this.state;
    const new_access_token = await get_new_access_token(refresh_token);
    console.log("App silent_refresh new_access_token", new_access_token);
    if (new_access_token && new_access_token.hasOwnProperty("access_token")) {
      this.setState({ isLoggedIn: true, access_token: new_access_token });
    }
  }

  // For Auth forms to use.
  setLoggedInStatus = status => {
    if (status.hasOwnProperty("error")) {
      console.log("status has error");
      this.setState({ isLoggedIn: false });
    } else if (status.hasOwnProperty("revoked")) {
      localStorage.removeItem("refresh_token");
      this.setState({ isLoggedIn: false });
    } else {
      // console.log("status", status);
      localStorage.setItem("refresh_token", status.refresh_token);
      this.setState({
        isLoggedIn: true,
        access_token: status.access_token,
        refresh_token: status.refresh_token
      });
    }
  };

  render() {
    console.log("APP state", this.state);
    const { isLoggedIn, access_token, refresh_token } = this.state;
    return (
      <Switch>
        <Route exact path="/">
          <h1>home!</h1>
          <h2>Are you logged in? {isLoggedIn.toString().toUpperCase()}</h2>
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

        <Route path="/logout">
          <Logout
            setLoggedInStatus={this.setLoggedInStatus}
            isLoggedIn={isLoggedIn}
            access_token={access_token}
            refresh_token={refresh_token}
          />
        </Route>
      </Switch>
    );
  }
}

export default App;
