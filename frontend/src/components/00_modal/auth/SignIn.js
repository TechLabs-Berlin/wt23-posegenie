import { signInWithEmailAndPassword } from "firebase/auth";
import React, { useState } from "react";
import { auth } from "./firebase";

const SignIn = ({ onClose }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const signIn = (e) => {
    e.preventDefault();
    if (password.length < 6) {
      setErrorMessage("Password must be at least 6 characters long.");
      return;
    }
    signInWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        console.log(userCredential);
        onClose();
      })
      .catch((error) => {
        console.log(error);
        if (error.code === "auth/user-not-found") {
          setErrorMessage("User not found.");
        } else {
          setErrorMessage("Invalid email or password.");
        }
      });
  };

  return (
    <div className="sign-in-container">
      <form onSubmit={signIn}>
        <h1 className="auth-title">Log In to your Account</h1>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        ></input>
        <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        ></input>
        {errorMessage && <p className="error-auth">{errorMessage}</p>}
        <button type="submit" onClick={onClose}>
          Log In
        </button>
      </form>
    </div>
  );
};

export default SignIn;
