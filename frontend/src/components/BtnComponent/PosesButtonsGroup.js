import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ButtonComponent.css";
import WarriorComponent from "./WarriorComponent";
import LungesComponent from "./LungesComponent";
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
        onButtonClicked(value);
    };

    const resetStates = () => {
        setSelectedPose(null);
    };

    const renderPoseComponent = () => {
        if (selectedPose === "lunges") {
            return <LungesComponent />;
        } else if (selectedPose === "warrior") {
            return <WarriorComponent />;
        }
        return null;
    };

    const handleModalClosed = () => {
        resetStates();
        onModalClosed();
    };

    return (
        <div className="container">
            <div>
                <h2>Choose an exercise</h2>
            </div>
            <div className="btn_container">
                {poses.map((button) => (
                    <button
                        key={button.id}
                        onClick={() => handleButtonClick(button.id)}
                        className={selectedPose === button.id ? "active" : ""}
                    >
                        {button.label}
                    </button>
                ))}
            </div>
            {renderPoseComponent()}

            <ModalFeedback onModalClosed={handleModalClosed} />
        </div>
    );
}

export default PosesButtonsGroup;
