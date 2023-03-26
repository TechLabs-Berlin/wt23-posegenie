import "./header.css";
// import headerImage from "./man_header.png";
// import headerImage2 from "./WomanLifter2_without_shade.png";
// import yogaMan from "./yoga_man-red.png";
import liftingWoman from "./woman_lifting_bw.png";

function Head() {
  return (
    <div className="wrapper">
      <div className="head">
        <div className="nav"></div>
        <h1 className="title">pose</h1>
        <h1 className="title highlight">Genie</h1>
        {/* <img className="head-img" src={headerImage} alt="man" /> */}
        {/* <img className="head-img man-yoga" src={yogaMan} alt="man yoga" /> */}
        <img
          className="head-img woman-lift"
          src={liftingWoman}
          alt="woman lifting"
        />
      </div>
    </div>
  );
}
export default Head;
