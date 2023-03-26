import "./modal.css";
import SignIn from "../00_modal/auth/SignIn";
import SignUp from "../00_modal/auth/SignUp";
import AuthDetails from "../00_modal/auth/AuthDetails";
import { useState } from "react";

function Modal({ isOpen, onClose }) {
  const [isLoginForm, setIsLoginForm] = useState(true);

  const handleToggleForm = () => {
    setIsLoginForm(!isLoginForm);
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal">
      <div className="modal-content">
        <div className="modal-header">
          <button onClick={onClose}>x</button>
        </div>
        <div className="modal-body">
          {isLoginForm ? (
            <>
              <SignIn onClose={onClose} />
              <button onClick={handleToggleForm}>
                Don't have an account? Create an account
              </button>
            </>
          ) : (
            <>
              <SignUp onClose={onClose} />
              <button onClick={handleToggleForm}>
                Already have an account? Log in
              </button>
            </>
          )}
          <AuthDetails />
        </div>
      </div>
    </div>
  );
}

export default Modal;
