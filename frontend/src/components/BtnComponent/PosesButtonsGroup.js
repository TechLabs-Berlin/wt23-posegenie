import React, { useState, useEffect } from "react";
import axios from "axios";
import "./ButtonComponent.css";

function PosesButtonsGroup({ onButtonClicked }) {
    const [activeButton, setActiveButton] = useState(null);
    const [poses, setPoses] = useState([]);

    useEffect(() => {
        axios.get("/poses").then((res) => {
            setPoses(res.data);
        });
    }, []);

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
                {poses.map((button) => (
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
