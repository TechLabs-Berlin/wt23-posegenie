import React from "react";
import "./ModalFeedback.css";

function ModalFeedback({ isOpen, onClose, children }) {
  const handleCloseModal = () => {
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="modal-container">
      <div className="modal-content">
        <div>
          <h2>Results: </h2>
        </div>
        {children}
        <button className="close-button" onClick={handleCloseModal}>
          Close
        </button>
      </div>
    </div>
  );
}

export default ModalFeedback;
