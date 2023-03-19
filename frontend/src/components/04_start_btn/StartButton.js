import "./startbtn.css";

function StartButton({ handleOpenModal }) {
  return (
    <div className="start-btn-box">
      <button className="start-btn" onClick={handleOpenModal}>
        Start now
      </button>
    </div>
  );
}
export default StartButton;
