import Step from "./Step";
function Steps() {
  return (
    <div className="steps wrapper">
      <Step number={"Step 1"} instruction={"Create an account"} />
      <Step number={"Step 2"} instruction={"Record and upload the video"} />
      <Step number={"Step 3"} instruction={"Check results"} />
    </div>
  );
}
export default Steps;
