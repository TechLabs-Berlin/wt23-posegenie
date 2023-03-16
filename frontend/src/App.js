import "./css/App.css";
import "./css/dark.css";
import "./css/light.css";

import React, { useState } from "react";

import Head from "./components/01_header/Head";
import Quote from "./components/02_quote/Quote";
import Steps from "./components/03_steps/Steps";
import StartButton from "./components/04_start_btn/StartButton";
import UploadVideoButton from "./components/05_update_video/UploadVideoButton";
import Footer from "./components/06_footer/Footer";

import Modal from "./components/00_modal/Modal";

function App() {
  //MODAL WINDOW

  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  //MODE

  const [isLightkMode, setisLightkMode] = useState(false);

  function toggleTheme() {
    setisLightkMode(!isLightkMode);
  }
  return (
    <div className="body">
      <div className={isLightkMode ? "light-mode" : "dark-mode"}>
        <div className="top_bar wrapper">
          <button onClick={toggleTheme}>
            {isLightkMode ? "Dark Mode" : "Light Mode"}
          </button>
          {/* <button>Sign in</button> */}
          <div>
            {!isModalOpen && (
              <button onClick={handleOpenModal}>Open Modal</button>
            )}
            <Modal isOpen={isModalOpen} onClose={handleCloseModal} />
          </div>
        </div>
        <Head />
        <Quote />
        <div className="steps wrapper">
          <Steps number={"Step 1"} instruction={"Create an account"} />
          <Steps
            number={"Step 2"}
            instruction={"Record and upload the video"}
          />
          <Steps number={"Step 3"} instruction={"Check results"} />
        </div>
        <StartButton />
        <UploadVideoButton />
        <Footer />
      </div>
    </div>
  );
}

export default App;
