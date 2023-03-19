import "./css/App.css";
import "./css/dark.css";
import "./css/light.css";

import React, { useState, useEffect } from "react";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../src/components/00_modal/auth/firebase";
import { signOut } from "firebase/auth";

import Head from "./components/01_header/Head";
import Quote from "./components/02_quote/Quote";
import Steps from "./components/03_steps/Steps";
import StartButton from "./components/04_start_btn/StartButton";
import UploadVideoButton from "./components/05_update_video/UploadVideoButton";
import Footer from "./components/06_footer/Footer";

import Modal from "./components/00_modal/Modal";

import ButtonComponent from "./components/BtnComponent/ButtonComponent";

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLightkMode, setisLightkMode] = useState(false);
  const [authUser, setAuthUser] = useState(null);

  useEffect(() => {
    const listen = onAuthStateChanged(auth, (user) => {
      if (user) {
        setAuthUser(user);
      } else {
        setAuthUser(null);
      }
    });

    return () => {
      listen();
    };
  }, []);

  const toggleTheme = () => {
    setisLightkMode(!isLightkMode);
  };

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const userSignOut = () => {
    signOut(auth)
      .then(() => {
        console.log("sign out successful");
      })
      .catch((error) => console.log(error));
  };

  return (
    <div className="body">
      <div className={isLightkMode ? "light-mode" : "dark-mode"}>
        <div className="top_bar wrapper">
          <button onClick={toggleTheme}>
            {isLightkMode ? "Dark Mode" : "Light Mode"}
          </button>
          {authUser ? (
            <>
              {/* <p>{`Signed In as ${authUser.email}`}</p> */}
              <button onClick={userSignOut}>Sign Out</button>
            </>
          ) : (
            <button onClick={handleOpenModal}>Account</button>
          )}
          <Modal isOpen={isModalOpen} onClose={handleCloseModal} />
        </div>

        <Head />
        <Quote />
        <Steps />
        {authUser ? (
          <>
            <ButtonComponent />
            <UploadVideoButton />
          </>
        ) : (
          <StartButton handleOpenModal={handleOpenModal} />
        )}
        <Footer />
      </div>
    </div>
  );
}

export default App;
