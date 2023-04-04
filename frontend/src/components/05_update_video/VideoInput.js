import "./VideoInput.css";

function VideoInput({ onFileUpload, onSubmit }) {
  return (
    <div className="video-upload-container">
      <div className="video-upload-header">
        <h2 className="video-upload-title">Upload Your Video</h2>
        <p className="video-upload-description">
          To comply with our guidelines, ensure that you're fully in the frame
          while recording. <br /> Please keep the video under one minute length.
          <br />
          Supported formats: .mp4, .mov, .avi
        </p>
      </div>
      <div className="video-upload-input-container">
        <input
          type="file"
          id="video-upload"
          accept=".mp4, .mov, .avi"
          onChange={onFileUpload}
          className="video-upload-input"
        />
        <label htmlFor="video-upload" className="video-upload-label">
          Choose File
        </label>
      </div>
      <button onClick={onSubmit} className="video-upload-button">
        Upload
      </button>
    </div>
  );
}

export default VideoInput;
