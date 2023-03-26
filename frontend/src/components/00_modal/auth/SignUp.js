import { createUserWithEmailAndPassword } from "firebase/auth";
import React, { useState } from "react";
import { auth } from "./firebase";

const SignUp = ({ onClose }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const signUp = (e) => {
    e.preventDefault();
    if (password.length < 6) {
      setPasswordError("Password should contain at least 6 characters");
      return;
    }
    createUserWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        console.log(userCredential);
        onClose();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
    setPasswordError("");
  };

  return (
    <div className="sign-up-container">
      <form onSubmit={signUp}>
        <h1 className="auth-title">Create Account</h1>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={handleEmailChange}
        ></input>
        <input
          type="password"
          placeholder="Enter your password"
          autoComplete="off"
          value={password}
          onChange={handlePasswordChange}
        ></input>
        {passwordError && <p className="error-auth">{passwordError}</p>}
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
};

export default SignUp;
