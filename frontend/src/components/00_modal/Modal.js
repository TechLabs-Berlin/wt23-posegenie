import "./modal.css";
import SignIn from "../00_modal/auth/SignIn";
import SignUp from "../00_modal/auth/SignUp";
import AuthDetails from "../00_modal/auth/AuthDetails";

function Modal({ isOpen, onClose }) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Modal Window</h2>
          <button onClick={onClose}>X</button>
        </div>
        <div className="modal-body">
          <p>It's a modal window.</p>
          <SignIn />
          <SignUp />
          <AuthDetails />
        </div>
      </div>
    </div>
  );
}

export default Modal;
