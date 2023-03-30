import React from "react";
import "./ModalFeedback.css";

function ModalFeedback({ isOpen, onClose, children, videoUrl }) {
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
        {videoUrl ? (
          <video
            src={videoUrl}
            controls
            type="video/mp4"
            className="video-player"
          />
        ) : (
          <div className="loading-spinner">
            <div className="spinner"></div>
          </div>
        )}
        <button className="close-button" onClick={handleCloseModal}>
          Close
        </button>
      </div>
    </div>
  );
}

export default ModalFeedback;
