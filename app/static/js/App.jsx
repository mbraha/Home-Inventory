import React, { Component } from "react";
import { Switch, Route } from "react-router-dom";
import RegisterForm from "./comps/Register";

class App extends Component {
  render() {
    return (
      <Switch>
        <Route path="/register">
          <RegisterForm />
        </Route>
        <Route path="/">
          <h1>home!</h1>
        </Route>
      </Switch>
    );
  }
}

export default App;
