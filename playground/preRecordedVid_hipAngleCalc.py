import cv2
import mediapipe as mp
import numpy as np
import sys

#################################################
#################################################

def calcAngle_3pts(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle >180.0:
        angle = 360-angle

    return angle


#################################################
#################################################


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(sys.argv[1])

if cap.isOpened() == False:
    print("Error opening video stream or file")
    raise TypeError

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

outdir, inputflnm = sys.argv[1][:sys.argv[1].rfind(
    '/')+1], sys.argv[1][sys.argv[1].rfind('/')+1:]
inflnm, inflext = inputflnm.split('.')
out_filename = f'{outdir}{inflnm}_annotated.{inflext}'
#out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(
#    'M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(
    'm', 'p', '4', 'v'), 10, (frame_width, frame_height))

while cap.isOpened():
    ret, image = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    try:
        landmarks = results.pose_landmarks.landmark

        # Get coordinates
        # I ll make it a one-liner soon
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        # Calculate angle
        angleRight = calcAngle_3pts(left_hip, right_hip, right_knee)
        angleLeft = calcAngle_3pts(right_hip, left_hip, left_knee)

        #Add a rectangle

        # Visualize angle
        #locationAngle = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y)
        cv2.putText(image, str(np.round(angleRight, 2)),
                           tuple(np.multiply(right_hip, [frame_width, frame_height]).astype(int)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
        cv2.putText(image, str(np.round(angleLeft, 2)),
                           tuple(np.multiply(left_hip, [frame_width, frame_height]).astype(int)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

    except:
        pass

    #cv2.rectangle(image, (0,0), (frame_width/5, frame_height/5), (0,0,0), -1)
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, mp_drawing.DrawingSpec(color=(255,255,255), thickness=3, circle_radius=3), mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2))
    out.write(image)

pose.close()
cap.release()
out.release()
