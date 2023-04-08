import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ButtonComponent.css";
import ModalFeedback from "../05_update_video/ModalFeedback";

function PosesButtonsGroup({ onButtonClicked, onModalClosed }) {
    const [selectedPose, setSelectedPose] = useState(null);
    const [poses, setPoses] = useState([]);

    useEffect(() => {
        axios.get("/poses").then((res) => {
            setPoses(res.data);
        });
    }, []);

    const handleButtonClick = (value) => {
        setSelectedPose(value);
        onButtonClicked(value.id);
    };

    const resetStates = () => {
        setSelectedPose(null);
    };

    const renderPoseComponent = () => {
        if (selectedPose) {
            try {
                const PoseComponent =
                    require(`./${selectedPose.componentName}Component`).default;
                return <PoseComponent />;
            } catch (error) {
                console.log(error);
                return null;
            }
        }
    };

    const handleModalClosed = () => {
        resetStates();
        onModalClosed();
    };

    const Buttons = () => {
        return poses.map((pose) => {
            const buttonStatus =
                selectedPose && selectedPose.id === pose.id
                    ? "active"
                    : "inactive";

            return (
                <button
                    key={pose.id}
                    onClick={() => handleButtonClick(pose)}
                    className={buttonStatus}
                >
                    {pose.label}
                </button>
            );
        });
    };

    return (
        <div className="wrapper">
            <div className="container">
                <h2 className="title-h2">Choose an exercise</h2>
                <div className="btn_container">
                    <Buttons />
                </div>
                {renderPoseComponent()}

                <ModalFeedback onModalClosed={handleModalClosed} />
            </div>
        </div>
    );
}

export default PosesButtonsGroup;
