import "./AboutUs.css";
function AboutUs() {
  return (
    <div className="wrapper aboutus">
      <p className="aboutus-p">
        Poor posture and incorrect exercise form are common problems that can
        result in a range of health issues and performance problems. Individuals
        may not be aware of proper exercise form or which muscles should be
        engaged during exercises, leading to muscle imbalances, reduced
        effectiveness of workouts, and even injury.
      </p>

      <p className="aboutus-p">
        PoseGenie offers an{" "}
        <span className="about-highloght">
          all-in-one AI-powered workout assistant
        </span>{" "}
        that provides users with real-time feedback and suggestions for
        performing exercises correctly. Utilizing advanced human pose estimation
        technology, PoseGenie is able to{" "}
        <span className="about-highloght">detect exercise performance</span> and{" "}
        <span className="about-highloght">
          offer personalized recommendations
        </span>
        .
      </p>
      <p className="aboutus-p">
        By using PoseGenie, you can optimize your workouts, minimize the risk of
        injury, and achieve your fitness goals with greater ease and efficiency.
        The comprehensive and personalized feedback offered by this innovative
        tool makes it a valuable asset to anyone looking to improve their
        exercise routine and overall health.
      </p>
    </div>
  );
}
export default AboutUs;
