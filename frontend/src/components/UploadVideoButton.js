import React, { useRef } from "react";
import { useState } from "react";
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
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
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
        <div>
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
