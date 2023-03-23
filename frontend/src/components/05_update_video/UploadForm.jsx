import axios from 'axios'
import React, {useState} from "react";
import PosesButtonsGroup from "../BtnComponent/PosesButtonsGroup";
import "./uploadvideo.css";
import VideoInput from './VideoInput';

function UploadForm() {
  const [activeButtonId, setActiveButtonId] = useState(null);
  const [file, setFile] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    
    if (activeButtonId) {
      const formData = new FormData();
      formData.append("pose", activeButtonId);
      formData.append("video", file);

      axios
        .post("/videos/upload", formData, {
          responseType: "arraybuffer",
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          console.log(res);
          const blob = new Blob([res.data]);
          const url = URL.createObjectURL(blob);
          renderVideoPlayer(url);
        })
        .catch((error) => {
          console.error("Error uploading video: ", error);
        });
    }
  };

  const renderVideoPlayer = (url) => {
    const video = document.createElement("video");
    video.src = url;
    video.controls = true;
    video.type = "video/mp4";
    const videoContainer = document.createElement("div");
    videoContainer.className = "video_container";
    videoContainer.appendChild(video);

    const uploadButton = document.querySelector(".uploadBtn");
    uploadButton.parentNode.insertBefore(
      videoContainer,
      uploadButton.nextSibling
    );
    videoContainer.scrollIntoView({ behavior: "smooth" });
  };

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  return (
    <div>
      <PosesButtonsGroup onButtonClicked={setActiveButtonId} />
      <form onSubmit={handleSubmit}>
        {activeButtonId && (
          <VideoInput onFileUpload={handleFileUpload} onSubmit={handleSubmit} />
        )}
      </form>
    </div>
  );
}

export default UploadForm;
