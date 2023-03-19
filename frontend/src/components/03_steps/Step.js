import "./steps.css";
function Step({ number, instruction }) {
  return (
    <div className="step-card">
      <p className="step-title">{number}</p>
      <p className="step-instr">{instruction}</p>
    </div>
  );
}
export default Step;
