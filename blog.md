# 🕸 Web Development

## ⚙ Backend

The first major decision regarding the development of the App was choosing between:

- Render the feedback of the AI model live to the user
- Process a uploaded video and send it back to the user with the annotations
  <!-- -->
  For a real-time solution, we would face some major challenges such as Browser and server limitations regarding both processing power and machine learning models. Also, we would have to transcribe Python models into JavaScript for rendering in real time. This solution was really not ideal considering the time frame available and skill level of the team. So, we opted for the uploaded video solution.
  <!-- -->
  With the upload feature in mind, we came up with the following dataflow structure.

### 🔁 Dataflow

<img src="https://i.ibb.co/B4DFtgZ/Flowchart.png" alt="Flowchart" border="0">

The idea behind the structure was to separate the responsibility as follows:

- **React frontend**: handles the video upload and the user authentication. Sends the video and the pose selected to NodeJS backend via HTML Form API POST request. Awaits the response from the NodeJS server to render the processed video back to the user.
- **NodeJS backend**: receives POST request in `/videos/upload` route with the video and sends it to Flask backend, also via HTML Form API POST request. Awaits the response from the Flask server.
- **Flask backend**: receives POST request in `/process_video` route with the video and pose chosen, process it with a specific function for each pose, saves the output and sends the feedback video along with the annonations as a response to the NodeJS server.

### 🎞 Video Transfer

One of the challenges of the backend development was learning how to properly send video data from one server to another. I had to learn about:

- Binary Large Objects (BLOB)
- Encoding and Decoding data
- File MIME types
- Types of video encoding

My biggest frustration which I spent lots of hours trying to fix was discovering that `cv2` video library saves a video which can be rendered by Media Players but can't be rendered by browsers without proper treatment. Imagine my confusion when the video played perfectly in my computer but would not play in the browser. Really!  
<br>
After many hours trying to figure things out, I discovered the video should be properly converted to _.mp4_ before being sent to the frontend. So, we had to use `moviepy` library to do the conversion before sending back the video, which also made the processing time longer.  
&nbsp;

### 📗 Database

We did setup a functioning **MongoDB Atlas** database to persist user data, however, it was not used for MVP because we were short on time to provide a more numerical feedback to the user and also we needed that additional Firebase knowledge to merge the information. The code which connects to the database is commented, but it connects normally if the _.env_ file with the credentials is provided.  
&nbsp;

### 👩‍👧‍👦 Teamwork

Since our solution required a lot of API requests, I had to make sure all the calls and responses worked perfectly from server to server, so naturally I had to help coding in all three servers (React, Node and Flask). Fortunately I did have some background in those languages and frameworks. Also, since I was aware of all the code going, I was in charge of reviewing the pull requests and merging to the _main_ branch of the GitHub repository.  
&nbsp;

&nbsp;

## Frontend

As the frontend developer, I used my React knowledges to create an intuitive and engaging interface for the application. I implemented several features to enhance user experience, including:

### 🌓 Dark mode by default:

I made dark mode the default viewing option in recognition of its growing popularity. However, I also provided users with the option to switch to light mode for their comfort and convenience.

&nbsp;

### 🖥 Modal windows:

I used modal windows for two purposes: user authentication and displaying feedback on user workouts. This allowed for secure and seamless login, as well as a non-intrusive way for users to track their progress.

&nbsp;

### 🔌 Connecting with Backend:

my primary responsibility was to ensure the frontend displayed data correctly from the backend. I collaborated with Andrey to optimize communication between the frontend and NodeJS server, requiring an understanding of API requests and responses.

&nbsp;

### 🔒 Firebase:

I implemented user authentication via Firebase to ensure secure and reliable protection of users' personal information and data. This allowed for smooth login and logout and user verification.

&nbsp;

### 👩‍👧‍👦 Teamwork:

I worked closely with the backend developer to ensure successful project completion. This included merging changes to the GitHub repository and optimizing the codebase for a successful MVP.

&nbsp;
