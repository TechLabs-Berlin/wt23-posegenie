# **poseGenie: AI powered form-feedback tool in fitness and yoga **

Are you tired of suffering from poor posture and feeling frustrated with incorrect exercise form? These issues can cause a range of health problems and limit your performance. Not to mention, it can be difficult to determine if you’re executing exercises properly or which muscles should be targeted. This can lead to muscle imbalances, reduced workout effectiveness, and even painful injuries.

Thankfully, there’s a high-tech solution that will leave you feeling confident and energized during your workouts. Introducing PoseGenie - the all-in-one workout assistant that uses advanced human pose estimation technology to detect your exercise and provide you with valuable feedback and customized suggestions to enhance your performance. This incredible tool offers exercise metrics and helps you optimize your workouts by engaging the correct muscles, allowing you to quantify your progress and achieve your goals.

Say goodbye to frustrating workouts and hello to your new personal trainer & workout optimizer - PoseGenie!

_This project was carried out as part of TechLabs in Berlin (winter term 2023)_

&nbsp;

# All tracks: initial phase
This section outlines the common discussion points that involved all track members at the planning phase:

- Which poses/exercises to implement, why and how

- How to learn the mechanics of the poses/exercises

- Which human pose estimation model to use

- Webapp or mobile app

- No UX designer team member in the team: how to proceed

- Realtime detection or prerecorded video

- To what extent the assistance/feedback/suggestions can be provided to the user in general

- To what extent the assistance/feedback/suggestions can be provided to the user in our MVP

- Audio feedback or written feedback

- A final report or an analysis on the fly

- A rep counter tool

- Which ML/DL models can be used on the data obtained from the user

- Trimming videos, detecting when the exercise starts


# 👩 Data Science and 🤖 Artificial Intelligence tracks: common points
Most of the time in our project phase, AI and DS teams worked together and this section outlines the common tasks of AI and DS.

- DS: Esma B. Boydas, Naiara Fernandez
- AI: Rashmi C. Dsouza, Ignatio C. Hidayat
- Tech Stack:Jupyter Notebook, Python, Mediapipe, Pandas, NumPy, Matplotlib, Scikit-learn

### Learning about 3D human pose estimation
At the initial stage of the project we have started to look into the dynamics of 3D human pose estimation models in Python. We have gathered important sources outlining the capabilities and uses of different computer vision models, such as the links below:

- A comprehensive guide to Human Pose Estimation:
https://www.v7labs.com/blog/human-pose-estimation-guide

- Human Pose Estimation Technology Capabilities and use cases:
https://mobidev.biz/blog/human-pose-estimation-technology-guide

- 3D Human Pose Estimation Experiments and Analysis:
https://www.kdnuggets.com/2020/08/3d-human-pose-estimation-experiments-analysis.html

- An easy guide for pose estimation with MediaPipe:
https://medium.com/mlearning-ai/an-easy-guide-for-pose-estimation-with-googles-mediapipe-a7962de0e944

- Squat analyzer with MediaPipe:
https://learnopencv.com/ai-fitness-trainer-using-mediapipe/

- Deadlift analyzer I:
https://saketshirsath.github.io/cv.github.io/

- Deadlift analyzer II:
https://github.com/SravB/Computer-Vision-Weightlifting-Coach

- Deep Learning approaches for workout repetition counting and validation:
https://www.sciencedirect.com/science/article/abs/pii/S016786552100324X#!

- Yoga Pose Estimation and Feedback Generation using Deep Learning:
https://www.hindawi.com/journals/cin/2022/4311350/

- Validity of an artificial intelligence, human pose estimation model for measuring single-leg squat kinematics:
https://pubmed.ncbi.nlm.nih.gov/36198251/

After taken a quick look at these resources, we have discussed the potential capabilities of our MVP from a python-backend perspective. 

### Decision of the AI-model
We have started testing the Mediapipe landmarks. Everyone in these two teams made use of real-life examples and observed the motion detection. To test the limitations, we have also resorted to videos in which the human body parts moved out of frame. We have discussed the detection confidence and used different thresholds to check the best setting in terms of computational cost vs. accuracy. The consensus was to proceed with mediapipe since it provides a collection of pre-built components that can be easily customized, combined, and extended to develop computer vision and ML models.

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

### Class Chair (Chair pose)

#### AI - Neural Net Model to Predict Stationary Poses

Similar to the machine learning model above, instead of hard-coding the angles to detect whether the desired pose is achieved, we utilized Deep Learning using Neural Networks to make pose detection more polished and refined. We have trained it for detecting 5 yoga poses, of which only one i.e the Chair pose is currently implemented in the app. Implementations of the 4 other poses will be done in the future.

#### Data

For the prediction models, there are pictures readily available online and we separated them into train and test folders, specifically using Lawrence Moroney’s Yoga Pose Classification datasets which are computer generated 300x300 full color images in 5 different poses, using Daz3D, were used. This image set contains all the five poses For further information: https://laurencemoroney.com/2021/08/23/yogapose-dataset.html. We used MoveNet, a TensorFlow Lite model, for human pose estimation. The model detects key points on a person's body and their movements in a video. We preprocessed the input images to detect the key points, and save those keypoints in CSV files using OpenCV and NumPy libraries. 

To preprocess the images, we used a Preprocessor class that takes the input folder of images and the output path for CSV files. It processes each pose class in the folder and writes the landmark coordinates to its CSV file. It also checks for invalid images and ignores them, skips images with scores below the threshold, and generates an error message for them. Finally, it merges all CSV files for each class into a single CSV file with a label, class name, and pose coordinates.

Once we had the CSV files with the key points, we use them to train a deep learning model to classify different poses. This model was able to identify different movements based on the keypoints extracted from the input video.


#### Model

For the model, we built a neural network using keras. The model uses 3 dense layers (2 used for input and output) and 2 dropout layers and achieved a perfect accuracy score on both training and validation sets which had 1513 and 878 images respectively, each having 5 classes. 

Alternatively, we tried adding a convolutional and max-pooling layer on top of the original model. Convolutional layers are a type of layer that are commonly used in Deep Learning models for image processing tasks. These layers operate on small regions of the input image, called kernels or filters, and extract local features such as edges, shapes, and textures. By applying multiple convolutional layers in a network, we can learn more complex and abstract features of the image hierarchy. Since the inputs we are passing into the model are one-dimensional arrays containing the landmark keypoints, a one-dimensional convolutional layer was used. 

The result of this layers might be that the extracted features include information about the position, orientation, and movement of the different joints, as well as more abstract features such as the overall pose of the person and the context in which the pose occurs.

Pooling layers operate on the output of convolutional layers by reducing the spatial resolution of the feature maps. The most common pooling operation is Max-Pooling, which selects the maximum activation value within a small window of pixels. Pooling helps to reduce the number of parameters in the network, prevent overfitting, and increase the computational efficiency of the model.

We experimented with adding a convolutional and max-pooling layer on top of the model. However, it had slightly less accuracy than the original model. The optimizer we used was adam, a popular optimizer that uses adaptive learning rates to update the weights of the neural network during training.

#### Original Model 
![Untitled](https://user-images.githubusercontent.com/50834160/230712925-01290a20-2213-4bac-81a0-670a7561fc9c.png)
![Untitled](https://user-images.githubusercontent.com/50834160/230713121-3786f375-171b-428d-b343-23c78a9b483c.png)

Accuracy: 0.9977194666862488

Loss: 0.004214226733893156

#### Original Model (with 1 Convolutional Layer & 1 MaxPooling Layer)
![output](https://user-images.githubusercontent.com/50834160/230713201-2475cb4a-7d6e-4671-81dd-32cf95c4d5de.png)
![output](https://user-images.githubusercontent.com/50834160/230713209-51f71d3d-d266-4e6a-b178-e9e5d8d6ede6.png)

Accuracy: 0.998859703540802

Loss: 0.008410756476223469

#### Original Model (with 2 Convolutional Layers & 2 MaxPooling Layers)

Accuracy: 0.9965792298316956

Loss: 0.015103639103472233

Through this experiment, adding convolutional and pooling layers to a neural network may not always improve its performance. The reason for this could be due to various factors such as the complexity of the dataset, with ours being very simple, the size of the network, the number of training examples, and the hyperparameters used in the model.

The neural network part of the project was heavily inspired by https://github.com/harshbhatt7585/YogaIntelliJ.

## Dynamic Exercises

Dynamic exercises involves repetitions and a higher degree of movement, which adds another layer of complexity regarding the landmark detection, data collection, and post-processing of the user exercise. For this purpose, we have resorted to detecting & recording & processing the most important landmarks for the exercise.

### Class Lunge (Lunges)

*How does this work?* For instance, a lunge exercise is a lower body exercise that involves stepping forward or backward with one leg and bending both knees to lower the body. The key points for this dynamic exercise are thus the upper legs, which should be actively detected by the detection model. We call it *the hip-knee angle* and record it progressively throughout the exercise.

*What comes after recording the key landmarks?* Following the detection and storing the important angles, we apply an initial parameter-free sinusoidal fit as the repetitive move resembles a sine wave. After fitting, there are three important parameters come into play:

- val_minmax: the difference between the maximum and minimum angle reached during the exercise
- val_amp: the amplitude of the sine wave calculated after sinusoidal fitting
- val_time: the period calculated after sinusoidal fitting

Based on these parameters, the feedback is generated in three parts and plotted by matplotlib along with the 2D graphs involving the measurements:

- Definition: This part explains the concept of the hip-knee angle and how it can be analyzed to assess the user's form during the lunge exercise.
- Analysis: This part provides a detailed analysis of the user's performance during the exercise, including their range of motion (val_minmax), consistency of movements (val_amp), and timing per rep (val_time). The workout assistant also provides specific comments and feedback based on these parameters.
- Feedback: This part provides specific feedback to the user based on their performance, including suggestions for improvement and areas to focus on during future workouts.

### Class Curls (Bicep Curls)

For Bicep curls, it works exactly like how the lunge exercise part of the project. However, during a bicep curl exercise, the key points of focus are the biceps, which need to be actively detected by the detection model. This is done by monitoring the angle of the elbow joint during the exercise. 

&nbsp;

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

As the frontend developer, I used my React knowledges to create an intuitive and engaging responsive interface for the application. I implemented several features to enhance user experience, including:

### 🌓 Dark mode by default:

I made dark mode the default viewing option in recognition of its growing popularity. However, I also provided users with the option to switch to light mode for their comfort and convenience.

&nbsp;

### 🖥 Modal windows:

I used modal windows for two purposes: user authentication and displaying feedback on user workouts. This allowed for secure and seamless login, as well as a non-intrusive way for users to track their progress.

&nbsp;

### 🔌 Connecting with Backend:

My primary responsibility was to ensure the frontend displayed data correctly from the backend. I collaborated with Andrey to optimize communication between the frontend and NodeJS server, requiring an understanding of API requests and responses.

&nbsp;

### 🔒 Firebase:

I implemented user authentication via Firebase to ensure secure and reliable protection of users' personal information and data. This allowed for smooth login and logout and user verification.

&nbsp;

### 👩‍👧‍👦 Teamwork:

I worked closely with the backend developer to ensure successful project completion. This included merging changes to the GitHub repository and optimizing the codebase for a successful MVP.

&nbsp;





