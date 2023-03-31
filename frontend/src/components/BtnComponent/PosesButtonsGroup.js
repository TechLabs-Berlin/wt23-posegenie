import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ButtonComponent.css";
import WarriorComponent from "./WarriorComponent";
import LungesComponent from "./LungesComponent";
import CurlsComponent from "./CurlsComponent";
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
    if (selectedPose === "Lunges") {
      return <LungesComponent />;
    } else if (selectedPose === "Warrior") {
      return <WarriorComponent />;
    } else if (selectedPose === "Curls") {
      return <CurlsComponent />;
    }
    return null;
  };

  const handleModalClosed = () => {
    resetStates();
    onModalClosed();
  };

  return (
    <div className="wrapper">
      <div className="container">
        <h2 className="title-h2">Choose an exercise</h2>
        <div className="btn_container">
          {poses.map((button) => (
            <button
              key={button.id}
              onClick={() => handleButtonClick(button.id)}
              className={selectedPose === button.id ? "active" : "inactive"}
            >
              {button.label}
            </button>
          ))}
        </div>
        {renderPoseComponent()}

        <ModalFeedback onModalClosed={handleModalClosed} />
      </div>
    </div>
  );
}

export default PosesButtonsGroup;
