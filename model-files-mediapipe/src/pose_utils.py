# DEPRECATED!! - please use files in pose-score-service

from .angle_calcs import Calculations
import mediapipe as mp
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

class Lunge():
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
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y] 

            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

            lHipKnee = [left_hip, left_knee]
            rHipKnee = [right_hip, right_knee]

            # Calculate angle
            lKnee_angle = np.round(self.calcs.calcAngle_3pts(left_hip, left_knee, left_ankle),2).astype(int)
            rKnee_angle = np.round(self.calcs.calcAngle_3pts(right_hip, right_knee, right_ankle),2).astype(int)
            back_angle = np.round(self.calcs.calcAngle_Horizontal(left_shoulder, left_hip),2).astype(int)

            # Knee & Ankle angle with the horizontal plane
            rKnee_trailing = np.round(self.calcs.calcAngle_Horizontal(right_knee, right_ankle),2).astype(int)
            lKnee_trailing = np.round(self.calcs.calcAngle_Horizontal(left_knee, left_ankle),2).astype(int)

            # lunge HipKnee & trailing HipKnee should be 90 deg
            hipKnee_angle = np.round(self.calcs.calcAngle_2lines(lHipKnee, rHipKnee)).astype(int)

            # Arrays for sinusoidal fitting
            self.angle_list.append(hipKnee_angle)
            self.timeStamp_list.append(round(float(self.read_upload.get_timestamps())/1000, 5))

            # Visualize angle
            cv2.putText(image, str(rKnee_angle), 
                           tuple(np.multiply(right_knee, [self.width, self.height]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2, cv2.LINE_AA
                                )
        
            cv2.putText(image, str(lKnee_angle), 
                           tuple(np.multiply(left_knee, [self.width, self.height]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2, cv2.LINE_AA
                                )
            
            cv2.putText(image, "KneeAnkle: "+str(lKnee_trailing), 
                           tuple(np.multiply(left_ankle, [self.width, self.height]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2, cv2.LINE_AA
                                )

            cv2.putText(image, "KneeAnkle: "+str(rKnee_trailing),
                           tuple(np.multiply(right_ankle, [self.width, self.height]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2, cv2.LINE_AA
                                )

            cv2.putText(image, "HipKnee: "+str(hipKnee_angle), 
                           tuple(np.multiply(left_hip, [self.width, self.height]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2, cv2.LINE_AA
                                )
            
            # Reps counter logic.
            if (lKnee_angle < 130 and (rKnee_trailing < -100) and back_angle > 75 and back_angle < 110 and hipKnee_angle > 60) or (rKnee_angle < 130 and lKnee_trailing < -100 and back_angle > 75 and back_angle < 110 and hipKnee_angle > 60):
                self.stage = "down"
            if (lKnee_angle > 130 and abs(rKnee_trailing) <= 150 and back_angle > 75 and back_angle < 110 and self.stage =='down') or (rKnee_angle > 130 and abs(lKnee_trailing) <= 160 and back_angle > 75 and back_angle < 110 and self.stage =='down'):
                self.stage="up"
                self.reps +=1
            if back_angle < 75 or back_angle > 110:
                self.hint = "Keep back straight"
            else:
                self.hint=""
        else:
            landmarks = None

        # Render rep counter
        # Setup status box
        cv2.rectangle(image, (0,0), (250,73), (0,0,0), -1)
        cv2.rectangle(image, (0,self.height-68), (380,self.height), (0,0,0), -1)
        
        # Rep data
        cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, str(self.reps), (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'STAGE', (90,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, self.stage, (90,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2, cv2.LINE_AA)
        
        # Hints & Feedback
        cv2.putText(image, 'HINT:', (15,self.height-56), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, self.hint, (15,self.height-13), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0,255,0), 2, cv2.LINE_AA)
        
        cv2.putText(image, "Back Angle: "+str(back_angle), 
                           (240,self.height-56), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA
                                )   
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
    
    def make_output_filename(self, file_path, suffix="_annotated"):
        # Output filename
        # FIXME: Replace forward slash with detection from a cross platform library
        outdir = self.filename[:self.filename.rfind('/')+1]
        inputflnm = self.filename[self.filename.rfind('/')+1:]
        
        inflnm, inflext = inputflnm.split('.')
        out_filename = f'{outdir}{inflnm}{suffix}.{inflext}'

        return out_filename


    def visualize(self):
        out_filename = self.make_output_filename(file_path=self.filename)


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

        angleTotalArray = np.array(self.angle_list)
        timeTotalArray  = np.array(self.timeStamp_list)

        res = self.calcs.fit_sin(self.timeStamp_list, self.angle_list)
        plt.plot(timeTotalArray, angleTotalArray, color="navy", label='FirstTrial', linewidth=2.0)
        plt.plot(timeTotalArray, res["fitfunc"](timeTotalArray), "r-", label="y fit curve", linewidth=2)
        plt.title('Lunge Progression (raw)')
        plt.xlabel('Timestamp (sec)')
        plt.ylabel('HipKneeAngle')
        plt.show()  