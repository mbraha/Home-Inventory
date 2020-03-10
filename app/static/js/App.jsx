import React, { Component } from "react";
import { Switch, Route } from "react-router-dom";
import RegisterForm from "./comps/Register";
import LoginForm from "./comps/Login";

class App extends Component {
  state = {
    current_user: "",
    isLoggedIn: false
  };

  // componentDidMount() {
  //   //
  // }

  async silentRefresh() {
    // try to refresh token
    await fetch("http://127.0.0.1:5000/token/refresh", {
      method: "POST",
      credentials: "same-origin"
    });
  }

  setLoggedInStatus = (status, username) => {
    if (status.hasOwnProperty("error")) {
      console.log("status has error");
      this.setState({ isLoggedIn: false });
    } else {
      console.log("status", status);
      this.setState({
        isLoggedIn: true,
        current_user: username
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
