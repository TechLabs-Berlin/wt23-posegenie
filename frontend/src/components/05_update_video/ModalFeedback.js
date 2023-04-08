import React from "react";
import "./ModalFeedback.css";

function ModalFeedback({ isOpen, onClose, videoUrl, imageUrl }) {
  const handleCloseModal = () => {
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <div>
          <h2 className="results">Results: </h2>
        </div>
        {videoUrl ? (
          <div>
            <video
              src={videoUrl}
              controls
              type="video/mp4"
              className="video-player"
            />
            <div className="image-container">
              <img src={imageUrl} className="image-feedback" />
            </div>
          </div>
        ) : (
          <div className="loading-container">
            <div className="loading-spinner">
              <h3>
                Analyzing your workout and measuring your movements.
                <br /> Please wait while we gather the data to give you <br />
                personalized feedback and insights.
              </h3>
              <div className="spinner"></div>
            </div>
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
