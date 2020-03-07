import AuthForm from "./Auth";

class LoginForm extends AuthForm {
  constructor(props) {
    super(props);
    super.endpoint = "login";
  }
}

export default LoginForm;
