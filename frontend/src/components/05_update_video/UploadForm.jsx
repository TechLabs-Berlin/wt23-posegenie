import axios from "axios";
import React, { useState } from "react";
import PosesButtonsGroup from "../BtnComponent/PosesButtonsGroup";

import VideoInput from "./VideoInput";
import ModalFeedback from "./ModalFeedback";
import FormData from "form-data";
function UploadForm() {
    const [activeButtonId, setActiveButtonId] = useState(null);
    const [file, setFile] = useState(null);
    const [videoUrl, setVideoUrl] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
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
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                })
                .then((res) => {
                    console.log(res.data);
                    setIsModalOpen(true);
                    setIsUploading(false); // set isUploading to false when the API call is complete
                    setVideoUrl(res.data.videoUrl);
                    setImageUrl(res.data.imageUrl);
                })
                .catch((error) => {
                    console.error("Error uploading video: ", error);
                    setIsUploading(false); // set isUploading to false if there's an error with the API call
                });
        }
    };

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
                    <VideoInput
                        onFileUpload={handleFileUpload}
                        onSubmit={() => setIsModalOpen(true)}
                    />
                )}
            </form>
            <ModalFeedback
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                videoUrl={videoUrl}
            >
                {videoUrl ? (
                    <video
                        src={videoUrl}
                        controls
                        type="video/mp4"
                        className="video-player"
                    />
                ) : (
                    <div className="waiting">
                        <div className="loading-spinner">
                            <p className="waiting-p">
                                Analyzing your workout, measuring your
                                movements, and calculating your performance.
                                Please wait while we gather the data to give you
                                personalized feedback and insights.
                            </p>

                            <div className="spinner"></div>
                        </div>
                    </div>
                )}
            </ModalFeedback>
            {imageUrl && <img src={imageUrl} alt="feedback" />}
        </div>
    );
}

export default UploadForm;
