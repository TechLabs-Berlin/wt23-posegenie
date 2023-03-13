import "./header.css";
import headerImage from "./man_header.png";

function Head() {
  return (
    <div className="wrapper">
      <div className="head">
        <div className="nav"></div>
        <h1 className="title">pose</h1>
        <h1 className="title highlight">Genie</h1>
        <img className="head-img" src={headerImage} alt="man" />
      </div>
    </div>
  );
}
export default Head;
