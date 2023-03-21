from .angle_calcs import Calculations
from .read_upload import readUpload 
import mediapipe as mp
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

class Curls():
    def __init__(self, read_upload, filename, pose) -> None:
        self.read_upload = read_upload(filename, pose)
        self.filename = filename
        self.calcs = Calculations()
        self.cap = self.read_upload.cap
        self.width = int(self.read_upload.get_frame_width())
        self.height = int(self.read_upload.get_frame_height())
        self.video_fps = self.read_upload.get_video_fps()
        self.get_timestamps = self.read_upload.get_timestamps()
        self.reps = 0 
        self.stage = ""
        self.hint = ""
        self.angle_list = []
        self.timeStamp_list = []

    def angle(self, results, image):
        if results.pose_landmarks is not None:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # Calculate angle
            sElbow_angle = round(self.calcs.calcAngle_3pts(shoulder, elbow, wrist),2)

            # Visualize angle
        
            cv2.putText(image, str(sElbow_angle), 
                           tuple(np.multiply(elbow, [self.width, self.height]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv2.LINE_AA
                                )
            
            
            # Reps counter logic.
            if sElbow_angle > 160:
                self.stage = "down"
            if sElbow_angle < 30 and self.stage =='down':
                self.stage="up"
                self.reps +=1
            else:
                self.hint=""
        else:
            landmarks = None

        # Render rep counter
        # Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        cv2.rectangle(image, (0,867), (355,940), (245,117,16), -1)
        
        # Rep data
        cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(self.reps), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'STAGE', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, self.stage, 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
    
    def visualize(self):
        # Output filename
        outdir, inputflnm = self.filename[:sys.argv[1].rfind(
            '/')+1], sys.argv[1][sys.argv[1].rfind('/')+1:]
        inflnm, inflext = inputflnm.split('.')
        out_filename = f'{outdir}{inflnm}_annotated.{inflext}'

        out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(
            'm', 'p', '4', 'v'), 30, (self.width, self.height))

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            image, results = self.read_upload.recolor_RGB()
            if image is None:
                break
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            self.angle(results, image)
            out.write(image)

        self.cap.release()
        out.release()
