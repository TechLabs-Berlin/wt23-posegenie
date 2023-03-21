import axios from 'axios'
import React, {useState} from "react";
import PosesButtonsGroup from "../BtnComponent/PosesButtonsGroup";

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

        videoContainer.scrollIntoView({ behavior: "smooth" });
    };

const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
  };
return (
    <div>
      <PosesButtonsGroup onButtonClicked={setActiveButtonId} />
      <form onSubmit={handleSubmit}>
        {/* TODO: Extract video input to a separate component */}
        {activeButtonId && (

            <div className="uploadBtn_container">
            <div>
                <div>
                <h2>Upload the video</h2>
                </div>
                <input
                type="file"
                id="video-upload"
                accept=".mp4, .mov, .avi"
                onChange={handleFileUpload}
                />
            </div>
            <div className="upload_btn_container">
                <button onClick={handleSubmit} className="uploadBtn">
                Upload Video
                </button>
            </div>
            </div>
        )}
      </form>
    </div>
  );
}

export default UploadForm;
