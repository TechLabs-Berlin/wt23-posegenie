import "./uploadvideo.css";
import axios from "axios";

import { React, useState } from "react";

function UploadVideoButton() {
  const [file, setFile] = useState(null);

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

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

        videoContainer.scrollIntoView({ behavior: "smooth" });
    };

    const handleUpload = () => {
        const formData = new FormData();
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
    };


  return (
    <div className="uploadBtn_container">
      <div>
        <input
          type="file"
          id="video-upload"
          accept=".mp4, .mov, .avi"
          onChange={handleFileUpload}
        />
      </div>
      <div className="upload_btn_container">
        <button onClick={handleUpload} className="uploadBtn">
          Upload Video
        </button>
      </div>
    </div>
  );
}

export default UploadVideoButton;
