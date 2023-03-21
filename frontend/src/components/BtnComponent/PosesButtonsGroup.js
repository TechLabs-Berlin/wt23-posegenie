import React, { useState } from "react";
import "./ButtonComponent.css";

function PosesButtonsGroup({ onButtonClicked }) {
    const [activeButton, setActiveButton] = useState(null);
    // TODO: get poses from the backend
    const buttons = [
        { id: "lunges", label: "Lunges" },
        { id: "warrior", label: "Warrior" },
    ];

    const handleButtonClick = (value) => {
        setActiveButton(value);
        onButtonClicked(value);
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
        </div>
    );
}

export default PosesButtonsGroup;
