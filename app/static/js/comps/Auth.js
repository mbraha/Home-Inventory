import React, { Component } from "react";
import { Button, Form } from "semantic-ui-react";
import { response_to_json } from "../utils";
import { Redirect } from "react-router-dom";

class AuthForm extends Component {
  constructor(props) {
    super(props);
    this.endpoint = "";

    this.state = { username: "", password: "" };
  }

  handleChange = (e, { name, value }) => this.setState({ [name]: value });

  handleSubmit = async () => {
    // TODO: Strip trailing whitespace
    console.log("handleSubmit", this.endpoint);
    const { username, password } = this.state;
    const query = "username=" + username + "&password=" + password;
    const response = await fetch(
      "http://127.0.0.1:5000/" + this.endpoint + "?" + query,
      {
        method: "POST",
        body: this.state
      }
    );
    const status = await response_to_json(response);
    console.log("response", status, status.status);
    this.setState({ username: "", password: "" });
    this.props.setLoggedInStatus(status, username);
  };

  render() {
    // console.log("Register render props", this.props);
    const { username, password } = this.state;
    if (this.props.isLoggedIn) {
      console.log("redirecting away from register");
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

export default AuthForm;
