import "./footer.css";

function Footer() {
  return (
    <div className="footer-container ">
      <div className="footer-content wrapper">
        <p className="footer-text">poseGenie</p>
        <p className="footer-text">
          &copy; TechLabs Berlin {new Date().getFullYear()}
        </p>
      </div>
    </div>
  );
}

export default Footer;
