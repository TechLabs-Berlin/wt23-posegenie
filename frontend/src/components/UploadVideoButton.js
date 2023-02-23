import React, { useRef } from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";

function UploadVideoButton() {
  const fileInputRef = useRef(null);

  const handleUpload = (event) => {
    const file = event.target.files[0];
    console.log("Selected file:", file);
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
        <input
          type="file"
          accept="video/*"
          ref={fileInputRef}
          style={{ display: "none" }}
          onChange={handleUpload}
        />
        <Button
          variant="outlined"
          size="medium"
          onClick={() => fileInputRef.current.click()}
          className="uploadBtn"
        >
          Upload Video
        </Button>
      </div>
    </Box>
  );
}
export default UploadVideoButton;
