import "./App.css";
import Navbar from "./components/Navbar";
import Header from "./components/Header";
import Card from "./components/Card";
import UploadVideoButton from "./components/UploadVideoButton";
import Footer from "./components/Footer";
import AboutUs from "./components/AboutUs";

function App() {
  return (
    <div>
      <Navbar />
      <Header />
      <Card />
      <UploadVideoButton />
      <AboutUs />
      <Footer />
    </div>
  );
}

export default App;
