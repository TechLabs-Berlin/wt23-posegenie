import React, { useState } from "react";
import "./ButtonComponent.css";
import WarriorComponent from "./WarriorComponent";
import LungesComponent from "./LungesComponent";

function PosesButtonsGroup({ onButtonClicked }) {
  const [activeButton, setActiveButton] = useState(null);
  const [selectedPose, setSelectedPose] = useState(null);
  // TODO: get poses from the backend
  const buttons = [
    { id: "lunges", label: "Lunges" },
    { id: "warrior", label: "Warrior" },
  ];

  const handleButtonClick = (value) => {
    setActiveButton(value);
    onButtonClicked(value);
    setSelectedPose(value);
  };

  const renderPoseComponent = () => {
    if (selectedPose === "lunges") {
      return <LungesComponent />;
    } else if (selectedPose === "warrior") {
      return <WarriorComponent />;
    }
    return null;
  };

  return (
    <div className="container">
      <div>
        <h2>Choose an exercise</h2>
      </div>
      <div className="btn_container">
        {buttons.map((button) => (
          <button
            key={button.id}
            onClick={() => handleButtonClick(button.id)}
            className={activeButton === button.id ? "active" : ""}
          >
            {button.label}
          </button>
        ))}
      </div>
      {renderPoseComponent()}
    </div>
  );
}

export default PosesButtonsGroup;
