from flask import Flask, request, send_file, render_template
import os
from hipkneeangle import hipknee


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route('/process_video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        # Get the uploaded file
        video_file = request.files['file']

        # To check if directory exists, if not create it
        directory = "uploaded_videos"  # Replace with the directory you want to create

        if not os.path.exists(directory):
            os.mkdir(directory)

        # Save the file
        video_file.save('uploaded_videos/' + video_file.filename)
        # processed_video_bytes = video_file.content[::-1]
        # return Response(processed_video_bytes, mimetype='video/mp4')

        hipknee('uploaded_videos/' + video_file.filename)


        # Set the new filename
        new_filename = video_file.filename.split('.')[0] + '_annotated.mp4'

        # Return the processed file for download with the new filename
        return send_file('uploaded_videos/' + new_filename,
                         download_name=new_filename,
                         as_attachment=True)
        # success_message = 'video uploaded to flask successfully!'
        # print(success_message)
        # return success_message

    # Render the HTML form
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
