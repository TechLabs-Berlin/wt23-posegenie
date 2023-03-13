import { React, useState } from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";

function UploadVideoButton() {
  const [file, setFile] = useState(null);

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append("video", file);

    fetch("/videos/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        const video = document.createElement("video");
        video.src = `http://localhost:4000/videos/${data.filePath}`;
        video.controls = true;

        const videoContainer = document.createElement("div");
        videoContainer.className = "video_container";
        videoContainer.appendChild(video);

        const uploadBtnContainer = document.querySelector(
          ".upload_btn_container"
        );
        uploadBtnContainer.parentNode.insertBefore(
          videoContainer,
          uploadBtnContainer.nextSibling
        );
      })
      .catch((error) => {
        console.error("Error uploading video: ", error);
      });
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        minHeight: "8vh",
      }}
    >
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
          <Button
            variant="outlined"
            size="medium"
            onClick={handleUpload}
            className="uploadBtn"
          >
            Upload Video
          </Button>
        </div>
      </div>
    </Box>
  );
}

export default UploadVideoButton;
