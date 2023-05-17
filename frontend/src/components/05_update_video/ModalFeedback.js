import React, {useEffect, useState} from "react";
import "./ModalFeedback.css";

const getVideoDimensionsOf = (url) => {
  return new Promise(resolve => {
      // create the video element
      const video = document.createElement('video');

      // place a listener on it
      video.addEventListener( "loadedmetadata", function () {
          // retrieve dimensions
          const height = this.videoHeight;
          const width = this.videoWidth;

          // send back result
          resolve({height, width});
      }, false);

      // start download meta-datas
      video.src = url;
  });
}

const ModalFeedback = ({ isOpen, onClose, videoUrl, imageUrl }) => {
  const [dimensions, setDimensions] = useState(null);
  
  useEffect(() => {
    if(videoUrl) {
      const getVideoDimensions = async () => {
        const dimensions = await getVideoDimensionsOf(videoUrl);
        setDimensions(dimensions)
      }

      getVideoDimensions();
    }
    
  }, [videoUrl]);

  const handleCloseModal = () => {
    onClose();
  };

  if (!isOpen) return null;

  const feedbackContainerClass = `feedback-container ${!imageUrl ? 'feedback-container__no-image' : ''}`

  return (
    <div className="modal-overlay">
      <div className="modal-container">
        <div>
          <h2 className="results">Results: </h2>
        </div>
        {videoUrl ? (
          <div className={feedbackContainerClass}>
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
