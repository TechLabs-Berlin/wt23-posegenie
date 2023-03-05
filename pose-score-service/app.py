from flask import Flask, request, send_file, render_template,Response

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route('/process_video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        # Get the uploaded file
        video_file = request.files['file']

        # Save the file
        video_file.save('uploaded_videos/' + video_file.filename)
        # processed_video_bytes = video_file.content[::-1]
        # return Response(processed_video_bytes, mimetype='video/mp4')

        # Return the saved file for download
        return send_file('uploaded_videos/' + video_file.filename,
                         as_attachment=True,
                         attachment_filename=video_file.filename
                         )
        # success_message = 'video uploaded to flask successfully!'
        # print(success_message)
        # return success_message

    # Render the HTML form
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
