import React, { Component } from "react";
import { Button, Form } from "semantic-ui-react";
import { Redirect } from "react-router-dom";

class LogoutForm extends Component {
  constructor(props) {
    super(props);
    super.endpoint = "logout";
  }
}

export default LogoutForm;
