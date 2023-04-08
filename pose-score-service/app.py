from flask import Flask, request, send_file, make_response
import zipfile
import mediapipe as mp
from utils import convert_to_mp4, annotated_filename
from config import videos_directory
import os
from pose_utils import Lunge
from curls_utils import Curls
from yoga_utils import Warrior
from chair_utils import Chair
from read_upload import readUpload

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route('/process_video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        # Get the uploaded file
        video_file = request.files['file']

        # Get the pose
        exercise = request.form.get('pose')

        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(min_detection_confidence=0.5,
                            min_tracking_confidence=0.5)

        # Create directory if does not exists
        if not os.path.exists(videos_directory):
            os.mkdir(videos_directory)

        # Uploads the video
        output_path = os.path.join(videos_directory, video_file.filename)
        video_file.save(output_path)

        # Process the video
        if exercise == "Lunges":
            lunge = Lunge(read_upload=readUpload,
                          filename=output_path, pose=pose)
            lunge.visualize()

        if exercise == "Curls":
            curls = Curls(read_upload=readUpload,
                          filename=output_path, pose=pose)
            curls.visualize()

        if exercise == "Warrior":
            warrior = Warrior(read_upload=readUpload,
                              filename=output_path, pose=pose)
            warrior.visualize()

        if exercise == "Chair":
            chair = Chair(read_upload=readUpload,
                              filename=output_path, pose=pose)
            chair.visualize()

        else:
            pass
        converted_video = convert_to_mp4(
            annotated_filename(video_file.filename))
        # image = f"uploaded_videos\{video_file.filename}.png"
        image = f"uploaded_videos/{video_file.filename}.png"

        # return send_file(converted_video, mimetype='video/mp4')

        if exercise == "Chair":
            files = [converted_video]
        else:
            files = [converted_video, image]
        # create a temporary file to store the zip archive
        zip_filename = 'temp.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zip:
            # add each file to the zip archive
            for file in files:
                zip.write(file, os.path.basename(file))
        # send the zip archive as the response
        return send_file(zip_filename, as_attachment=True, download_name=zip_filename)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
