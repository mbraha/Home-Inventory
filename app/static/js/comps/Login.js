import React, { Component } from "react";
import { Button, Form } from "semantic-ui-react";
import { response_to_json } from "../utils";
import { Redirect } from "react-router-dom";

class LoginForm extends Component {
  constructor(props) {
    super(props);

    this.state = { username: "", password: "" };
  }

  handleChange = (e, { name, value }) => this.setState({ [name]: value });

  handleSubmit = async () => {
    console.log("Login handleSubmit");
    const query =
      "username=" + this.state.username + "&password=" + this.state.password;
    const response = await fetch("http://127.0.0.1:5000/login?" + query, {
      method: "POST",
      body: this.state
    });
    const status = await response_to_json(response);
    console.log("Login response", status, status.status);
    this.setState({ username: "", password: "" });
    this.props.setLoggedInStatus(status);
  };

  render() {
    // console.log("Register render props", this.props);
    const { username, password } = this.state;
    if (this.props.isLoggedIn) {
      console.log("redirecting away from Login");
      return <Redirect to="/" />;
    }
    return (
      <Form onSubmit={this.handleSubmit}>
        <Form.Input
          label="Username"
          placeholder="Username"
          name="username"
          value={username}
          width={6}
          onChange={this.handleChange}
        ></Form.Input>
        <Form.Input
          label="Password"
          placeholder="Password"
          name="password"
          width={6}
          value={password}
          type="password"
          onChange={this.handleChange}
        ></Form.Input>
        <Button type="submit">Submit</Button>
      </Form>
    );
  }
}

export default LoginForm;
