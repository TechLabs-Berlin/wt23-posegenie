from flask import Flask, request, send_file
from hipkneeangle import hipknee
from utils import convert_to_mp4, annotated_filename
from config import videos_directory
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route('/process_video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        # Get the uploaded file
        video_file = request.files['file']
        # Create directory if does not exists
        if not os.path.exists(videos_directory):
            os.mkdir(videos_directory)
            
        # Uploads the video
        output_path = os.path.join(videos_directory, video_file.filename)
        video_file.save(output_path)
        
        # Process the video
        hipknee(output_path)
        converted_video = convert_to_mp4(annotated_filename(video_file.filename))
        return send_file(converted_video, mimetype='video/mp4')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
