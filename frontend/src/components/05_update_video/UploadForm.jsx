import axios from 'axios'
import React, { useState } from "react";
import PosesButtonsGroup from "../BtnComponent/PosesButtonsGroup";
import "./uploadvideo.css";
import VideoInput from './VideoInput';
import ModalFeedback from './ModalFeedback';
import FormData from 'form-data'
function UploadForm() {
  const [activeButtonId, setActiveButtonId] = useState(null);
  const [file, setFile] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    
        if (activeButtonId) {
          const formData = new FormData();
          formData.append("pose", activeButtonId);
          formData.append("video", file);
          setIsUploading(true); // set isUploading to true before making the API call

        axios
            .post("/videos/upload", formData, {
                responseType: "arraybuffer",
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            })
            .then((res) => {
                const blob = new Blob([res.data]);
                const url = URL.createObjectURL(blob);
                setIsModalOpen(true);
                setIsUploading(false); // set isUploading to false when the API call is complete
                renderVideoPlayer(url);
            })
            .catch((error) => {
                console.error("Error uploading video: ", error);
                setIsUploading(false); // set isUploading to false if there's an error with the API call
            });
        }
}
    const renderVideoPlayer = (url) => {
        const video = document.createElement("video");
        video.src = url;
        video.controls = true;
        video.type = "video/mp4";

        // video.style.maxWidth = "50%";

        const videoContainer = document.createElement("div");
        videoContainer.className = "video_container";
        videoContainer.appendChild(video);

        const uploadButton = document.querySelector(".uploadBtn");
        uploadButton.parentNode.insertBefore(
            videoContainer,
            uploadButton.nextSibling
        );
    }

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  const handleCloseModal = () => {
    setVideoUrl(null);
    setIsModalOpen(false);
    setActiveButtonId(null);
    setFile(null);
  };


  return (
    <div>
      <PosesButtonsGroup onButtonClicked={setActiveButtonId} />
      <form onSubmit={handleSubmit}>
        {activeButtonId && (
          <VideoInput onFileUpload={handleFileUpload} onSubmit={() => setIsModalOpen(true)} />
        )}
      </form>
      <ModalFeedback isOpen={isModalOpen} onClose={handleCloseModal}>
        {videoUrl ? (
          <video src={videoUrl} controls type="video/mp4" className="video-player" />
        ) : (
          <div className="loading-spinner">
            <div className="spinner"></div>
          </div>
        )}
      </ModalFeedback>
    </div>
  );
  
  
}

export default UploadForm;
