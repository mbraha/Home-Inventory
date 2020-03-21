import React from "react";
import { Container } from "semantic-ui-react";
import Header from "./Header";

export default props => {
  return (
    <Container>
      <Header
        setLoggedInStatus={props.setLoggedInStatus}
        isLoggedIn={props.isLoggedIn}
      />
      {props.children}
    </Container>
  );
};
