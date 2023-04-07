Are you tired of suffering from poor posture and feeling frustrated with incorrect exercise form? These issues can cause a range of health problems and limit your performance. Not to mention, it can be difficult to determine if you’re executing exercises properly or which muscles should be targeted. This can lead to muscle imbalances, reduced workout effectiveness, and even painful injuries.

Thankfully, there’s a high-tech solution that will leave you feeling confident and energized during your workouts. Introducing PoseGenie - the all-in-one workout assistant that uses advanced human pose estimation technology to detect your exercise and provide you with valuable feedback and customized suggestions to enhance your performance. This incredible tool offers exercise metrics and helps you optimize your workouts by engaging the correct muscles, allowing you to quantify your progress and achieve your goals.

Say goodbye to frustrating workouts and hello to your new personal trainer - PoseGenie!

&nbsp;

# All tracks: initial phase
This section outlines the common discussion points that involved all track members at the initial stage:

-Which poses/exercises to implement, why and how

-How to learn the mechanics of the poses/exercises

-Which human pose estimation model to use

-Webapp or mobile app

-No UX designer team member in the team: how to proceed

-Realtime detection or prerecorded video

-To what extent the assistance/feedback/suggestions can be provided to the user in general

-To what extent the assistance/feedback/suggestions can be provided to the user in our MVP

-Audio feedback or written feedback

-A final report or an analysis on the fly

-A rep counter tool

-Which ML/DL models can be used on the data obtained from the user

-Trimming videos, detecting when the exercise starts


# 👩 Data Science and 🤖 Artificial Intelligence tracks: common points
Most of the time in our project phase, AI and DS teams worked together and this section outlines the common tasks of AI and DS.

- DS: Esma B. Boydas, Naiara Fernandez
- AI: Rashmi C. Dsouza, Ignatio C. Hidayat
- Tech Stack:Jupyter Notebook, Python, Mediapipe, Pandas, NumPy, Matplotlib, Scikit-learn

### Learning about 3D human pose estimation
At the initial stage of the project we have started to look into the dynamics of 3D human pose estimation models in Python. We have gathered important sources outlining the capabilities and uses of different computer vision models, such as the links below:

-A comprehensive guide to Human Pose Estimation:
https://www.v7labs.com/blog/human-pose-estimation-guide

-Human Pose Estimation Technology Capabilities and use cases:
https://mobidev.biz/blog/human-pose-estimation-technology-guide

-3D Human Pose Estimation Experiments and Analysis:
https://www.kdnuggets.com/2020/08/3d-human-pose-estimation-experiments-analysis.html

-An easy guide for pose estimation with MediaPipe:
https://medium.com/mlearning-ai/an-easy-guide-for-pose-estimation-with-googles-mediapipe-a7962de0e944

-Squat analyzer with MediaPipe:
https://learnopencv.com/ai-fitness-trainer-using-mediapipe/

-Deadlift analyzer I:
https://saketshirsath.github.io/cv.github.io/

-Deadlift analyzer II:
https://github.com/SravB/Computer-Vision-Weightlifting-Coach

-Deep Learning approaches for workout repetition counting and validation:
https://www.sciencedirect.com/science/article/abs/pii/S016786552100324X#!

-Yoga Pose Estimation and Feedback Generation using Deep Learning:
https://www.hindawi.com/journals/cin/2022/4311350/

-Validity of an artificial intelligence, human pose estimation model for measuring single-leg squat kinematics:
https://pubmed.ncbi.nlm.nih.gov/36198251/

After taken a quick look at these resources, we have discussed the potential capabilities of our MVP from a python-backend perspective. 

### Decision of the AI-model
We have started testing the Mediapipe landmarks. Everyone in these two teams made use of real-life examples and observed the motion detection. To test the limitations, we have also resorted to videos in which the human body parts moved out of frame. We have discussed the detection confidence and used different thresholds to check the best setting in terms of computational cost vs. accuracy. The consensus was to proceed with mediapipe since it provides a collection of pre-built components that can be easily customized, combined, and extended to develop computer vision and ML models.

(The picture from the ppt showing examples of the tests)

### Implementation phase
We have implemented common calculator functions which would be regularly used by means of all exercises. Angle calculations are the most crucial steps in pose detection, and we resorted to different techniques to calculate them, such as angle between two lines (4 landmark points) vs between three points (3 landmarks).

We distinguished between *dynamic exercises* that are based on repeats and counts, (e.g. lunges, curls) and *static exercises* that require holding a position for a certain time (e.g. yoga poses). Depending on the specific exercise, different data analysis approach was taken. Each exercise is implemented  as a separate class.

## Static Exercises

### Class Warrior (Warrior 2 yoga pose)

#### Data Analysis

To analyze Warrior 2 pose, 10 different indicative angles, calculated from the Mediapipe landmarks, are used: angles at elbows, knees and hips (6 angles), and angles arms and legs from horizontal (4 angles).

Given Warrior 2 pose is an asymmetric pose, user can be facing right or left, it first required a preliminary analysis on the leg position to determine if the user is performing a left or right warrior. Then, angles are analized to check if they are within predefined ranges for the pose to be considered "detected", if yes a timer is started. To implement the timer, CV2 timestamps of video frames are used, which gives approximate duration. In addition, feedback is given to users to get their angles closer to the "optimal" expected angles and to "improve" their pose.

All indicative angles and calculations are internally stored in Numpy Arrays and Python lists, then at the end of video they are converted to Pandas DataFrame for final analysis and graph plotting with MatplotLib.

#### Machine Learning Model

The initial approach described above, relies on "hard-coded" angle ranges to detect the pose. But this would have been a limitation if we wanted to easily expand the app to many more yoga poses (ideally an entire yoga flow sequence).

A basic Machine Learning (ML) model was implemented to detect additional poses. For the training of the ML model, >300 images downloaded from internet are used. The ML model data preparation and training is done in a Jupyter notebook, where from each image, 10 indicative angles are stored as features with a label (pose name). The ML model was trained with SciKitLearn, using Decision Trees, Random Forest, and SVC (linear and rbc kernel) models. Trained models are saved and can be loaded in the main python app. At the moment of submission, few poses were contained in the model, mountain pose, tree pose, and warrior 1 and 2 poses. A similar approach, but using Deep Learning algorithms is implemented in the different class "Chair" pose.

Right now, feedback is only given for Warrior 2 pose. Ideally, the app, would detect any of the poses within the ML model, and would provide also feedback to the app user. One caveat of a model trained with arbitrary images downloaded from the internet is that, the images do not necesarily represent an optimally-performed yoga pose, but instead provides a broad range of angles for pose detection in the app. Ideally two different set of images would be used to train two different models: 1) a broad range of arbitrary images representing of all levels of performers to detect the pose in the app (as implemented right now). 2) A second set of images with the poses performed by advanced practitioner, coaches, or instructurs, for a model used as a benchmark to provide feedback to user.


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





