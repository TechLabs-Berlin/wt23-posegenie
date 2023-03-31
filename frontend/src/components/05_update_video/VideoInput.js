function VideoInput({ onFileUpload, onSubmit }) {
  return (
    <div className="uploadBtn_container">
      <div>
        <div className="upload">
          <h2 className="title-h2">Upload the video</h2>
        </div>
        <input
          type="file"
          id="video-upload"
          accept=".mp4, .mov, .avi"
          onChange={onFileUpload}
        />
      </div>
      <div className="upload_btn_container">
        <button onClick={onSubmit} className="uploadBtn">
          Upload Video
        </button>
      </div>
    </div>
  );
}

export default VideoInput;
