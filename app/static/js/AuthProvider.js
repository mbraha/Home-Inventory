import React, { Component } from "react";
import { get_new_access_token } from "./utils";

const AuthContext = React.createContext();

class AuthProvider extends Component {
  state = {
    current_user: "nobody",
    isLoggedIn: false,
    access_token: null,
    refresh_token: null,
    timer_id: null
  };

  async componentDidMount() {
    console.log("AuthProvider componentDidMount");
    const refresh_token = localStorage.getItem("refresh_token");
    const current_user = localStorage.getItem("current_user");
    console.log("got token from storage", refresh_token);
    if (refresh_token === null) {
      // User needs to register/login
      this.setState({
        current_user
      });
    } else {
      // Try and get a new access token
      const new_access_token_result = await get_new_access_token(refresh_token);
      console.log("AuthProvider didMount new_token", new_access_token_result);
      if (
        new_access_token_result &&
        new_access_token_result.hasOwnProperty("access_token")
      ) {
        this.setState({
          isLoggedIn: true,
          access_token: new_access_token_result.access_token,
          refresh_token: refresh_token
        });
      } else if (new_access_token_result == 401) {
        // Refresh token revoked, failed to get access
        this.setState({
          refresh_token: null
        });
      }
      const timer_id = setInterval(() => this.silentRefresh(), 1000 * 60 * 14);
      this.setState({ timer_id: timer_id, current_user: current_user });
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

  setLoggedInStatus = (status, username) => {
    console.log("setting log in status");
    if (status.hasOwnProperty("error")) {
      console.log("status has error");
      this.setState({ isLoggedIn: false });
    } else if (status.hasOwnProperty("revoked")) {
      localStorage.removeItem("refresh_token");
      this.setState({ isLoggedIn: false });
    } else {
      // console.log("status", status);
      localStorage.setItem("refresh_token", status.refresh_token);
      localStorage.setItem("current_user", username);
      this.setState({
        isLoggedIn: true,
        access_token: status.access_token,
        refresh_token: status.refresh_token,
        current_user: username
      });
    }
  };

  render() {
    // TODO: this.props.children necessary?
    console.log("AuthProvider render state", this.state);
    return (
      <AuthContext.Provider
        value={{ state: this.state, setLoggedInStatus: this.setLoggedInStatus }}
      >
        {this.props.children}
      </AuthContext.Provider>
    );
  }
}

export { AuthProvider, AuthContext };
