import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../utils/axios";
import { ToastContainer, toast } from 'react-toastify';
import { loginRoute } from "../utils/APIRoutes";

function Register() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const notify = (text, status) => {
    if (status === 200 || status === 201) toast.success(`${text}`)
    if (status === 400 || status === 401 || status === 403 || status === 404 || status === 500 || status === 503) toast.error(`${text}`)
  }
  // function generatePassword() {
  //   var length = 20,
  //     charset =
  //       "!@#$%^&*()_+=<,>.?/|{}[]~`abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
  //     retVal = "";
  //   for (var i = 0, n = charset.length; i < length; ++i) {
  //     retVal += charset.charAt(Math.floor(Math.random() * n));
  //   }
  //   setPassword(retVal);
  // }

  function LoginSubmit() {
    if (
      email.trim() &&
      password.trim()
    ) {
      const reqBody = {
        email: email,
        password: password,
      };
      API.post(loginRoute, reqBody)
        .then((res) => {
          localStorage.setItem(process.env.REACT_APP_LOCALHOST_KEY, JSON.stringify( res.data))
          notify(`Success`, res.status)
          setTimeout(() => {
            navigate("/")
          }, 5500)
        })
        .catch(err => {notify(err.response?.data?.message, err.response?.status); console.log(err)})
    }
  }
  return (
    <div id="wrapper" className="wrapper-full ">
      <ToastContainer />
      <div className="main-container container">
        <ul className="breadcrumb">
          <li>
            <Link to="/">
              <i className="fa fa-home"></i>
            </Link>
          </li>
          <li>
            <Link to="/register">Register</Link>
          </li>
        </ul>

        <div className="row">
          <div id="content" className="col-sm-12">
            <h2 className="title">Login Account</h2>

            <div className="form-horizontal account-register clearfix">
              <fieldset id="account">
                <div className="form-group required">
                  <label
                    className="col-sm-2 control-label"
                    htmlFor="input-email"
                  >
                    E-Mail
                  </label>
                  <div className="col-sm-10">
                    <input
                      type="email"
                      name="email"
                      placeholder="E-Mail"
                      id="input-email"
                      className="form-control"
                      onChange={({ target }) => setEmail(target.value)}
                    />
                  </div>
                </div>   
             
              </fieldset>
              <fieldset>
                <legend>Your Password</legend>
                <div className="form-group required">
                  <label
                    className="col-sm-2 control-label"
                    htmlFor="input-password"
                  >
                    Password
                  </label>
                  <div className="col-sm-10">
                    <input
                      type="password"
                      name="password"
                      placeholder="Password"
                      id="input-password"
                      className="form-control"
                      onChange={({ target }) => setPassword(target.value)}
                    />
                  </div>
                </div>
              </fieldset>

              <div className="buttons">
                <div className="pull-right d-flex">
                  <p>
                    If you already have an account with us, please login at the{" "}
                    <Link to="/login">login page</Link>.
                  </p>
                  <button
                    type="submit"
                    defaultValue="Continue"
                    className="btn btn-primary"
                    onClick={() => {
                      LoginSubmit();
                      notify();
                    }}
                  >
                    Login
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;
