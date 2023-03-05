import "./App.css";
import Navbar from "./components/Navbar";
import Header from "./components/Header";
import Card from "./components/Card";
import UploadVideoButton from "./components/UploadVideoButton";
import Footer from "./components/Footer";
import AboutUs from "./components/AboutUs";

import SignIn from "./components/auth/SignIn";
import SignUp from "./components/auth/SignUp";
import AuthDetails from "./components/auth/AuthDetails";

function App() {
  return (
    <div>
      <Navbar />

      <div className="user-auth">
        <SignIn />
        <SignUp />
        <AuthDetails />
      </div>

      <Header />
      <Card />
      <UploadVideoButton />
      <AboutUs />
      <Footer />
    </div>
  );
}

export default App;
