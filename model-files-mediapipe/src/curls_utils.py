# DEPRECATED!! - please use files in pose-score-service

from .angle_calcs import Calculations
from .read_upload import readUpload 
import mediapipe as mp
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
import scipy

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
        self.left_reps = 0 
        self.left_stage = ""
        self.right_reps = 0 
        self.right_stage = ""
        self.hint = ""
        self.angle_list = []
        self.timeStamp_list = []


    def angle(self, results, image):
        if results.pose_landmarks is not None:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates for left arm
            l_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            l_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            l_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # Get coordinates for right arm
            r_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            r_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            r_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            # Calculate angles for left arm
            l_angle = round(self.calcs.calcAngle_3pts(l_shoulder, l_elbow, l_wrist), 2)
            round_l_angle = round(self.calcs.calcAngle_3pts(l_shoulder, l_elbow, l_wrist))

            # Calculate angles for right arm
            r_angle = round(self.calcs.calcAngle_3pts(r_shoulder, r_elbow, r_wrist), 2)
            round_r_angle = round(self.calcs.calcAngle_3pts(r_shoulder, r_elbow, r_wrist))


            # Update angle lists
            self.angle_list.append(l_angle)
            self.angle_list.append(r_angle)
            self.timeStamp_list.append(round(float(self.read_upload.get_timestamps()) / 1000, 5))
            self.timeStamp_list.append(round(float(self.read_upload.get_timestamps()) / 1000, 5))
            

            # Visualize angles for both arms
            cv2.putText(image, f"L Angle: {round_l_angle}", tuple(np.multiply(l_elbow, [self.width, self.height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(image, f"R Angle: {round_r_angle}", tuple(np.multiply(r_elbow, [self.width, self.height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

            # Update reps and stage for left arm
            if l_angle > 160:
                self.left_stage = "L down"
            if l_angle < 30 and self.left_stage == 'L down':
                self.left_stage = "L up"
                self.left_reps += 1
            else:
                self.hint = ""

            # Update reps and stage for right arm
            if r_angle > 160:
                self.right_stage = "R down"
            if r_angle < 30 and self.right_stage == 'R down':
                self.right_stage = "R up"
                self.right_reps += 1
            else:
                self.hint = ""

        else:
           landmarks = None

        # Render rep counter
        # Setup status box
        box_width = 355 - 0 # Assuming the current coordinates in the code
        box_height, _ = cv2.getTextSize('RIGHT ARM STAGE', cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)

        cv2.rectangle(image, (0,0), (300,73), (245,117,16), -1)
        cv2.rectangle(image, (self.width - box_width, 0), (self.width, box_height[1] + 60), (245,117,16), -1)




        # Left arm rep data
        cv2.putText(image, 'LEFT ARM REPS', (5,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, f'{self.left_reps}', 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Left arm stage data
        cv2.putText(image, 'LEFT ARM STAGE', (150,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, f'{self.left_stage}', 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Right arm rep data
        cv2.putText(image, 'RIGHT ARM REPS', (self.width-150,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, f'{self.right_reps}', 
                    (self.width-300,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Right arm stage data
        cv2.putText(image, 'RIGHT ARM STAGE', (self.width-320,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, f'{self.right_stage}', 
                    (self.width-230,60), 
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






        
