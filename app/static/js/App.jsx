import React, { Component } from "react";
import { Switch, Route } from "react-router-dom";
import RegisterForm from "./comps/Register";
import LoginForm from "./comps/Login";
import { response_to_json } from "./utils";

class App extends Component {
  state = {
    current_user: "",
    isLoggedIn: false,
    access_token: null,
    refresh_token: null
  };

  async componentDidMount() {
    const refresh_token = localStorage.getItem("refresh_token");
    console.log("got token from storage", refresh_token);

    // Try and get a new access token
    const response = await fetch("http://127.0.0.1:5000/token/refresh", {
      method: "POST",
      headers: new Headers({ Authorization: "Bearer " + refresh_token })
    });
    const refresher = await response_to_json(response);
    console.log("App didMount refresher", refresher);
    if (refresher.hasOwnProperty("access_token")) {
      this.setState({ isLoggedIn: true, access_token: refresher });
    }
  }

  setLoggedInStatus = status => {
    if (status.hasOwnProperty("error")) {
      console.log("status has error");
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
    const { isLoggedIn } = this.state;
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
      </Switch>
    );
  }
}

export default App;
