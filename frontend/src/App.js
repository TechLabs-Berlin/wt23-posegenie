import "./css/App.css";
import "./css/dark.css";
import "./css/light.css";
import React, { useState } from "react";

import Head from "./components/01_header/Head";
import Quote from "./components/02_quote/Quote";
import Steps from "./components/03_steps/Steps";
import StartButton from "./components/StartButton";
import Footer from "./components/05_footer/Footer";

// import Navbar from "./components/Navbar";
// import Header from "./components/Header";
// import Card from "./components/Card";
// import UploadVideoButton from "./components/UploadVideoButton";
// import Footer from "./components/Footer";
// import AboutUs from "./components/AboutUs";

// import SignIn from "./components/auth/SignIn";
// import SignUp from "./components/auth/SignUp";
// import AuthDetails from "./components/auth/AuthDetails";

function App() {
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
          <button>Sign in</button>
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
        <Footer />
        {/* <Navbar />

        <div className="user-auth">
          <SignIn />
          <SignUp />
          <AuthDetails />
        </div>

        <Header />
        <Card />
        <UploadVideoButton />
        <AboutUs />
        <Footer /> */}
      </div>
    </div>
  );
}

export default App;
