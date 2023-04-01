import "./header.css";
import liftingWoman from "./woman_lifting_bw.png";

function Head() {
  return (
    <div className="wrapper">
      <div className="head">
        <div className="nav"></div>
        <h1 className="title">pose</h1>
        <h1 className="title highlight">Genie</h1>

        <img className="head-img" src={liftingWoman} alt="woman lifting" />
      </div>
    </div>
  );
}
export default Head;
