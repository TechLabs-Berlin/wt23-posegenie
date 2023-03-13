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

class Warrior():
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
        self.pose_orientation = "WAITING..."
        self.pose_color = (0,0,0)
        self.left_arm_correct = "WAITING..."
        self.right_arm_correct = "WITING..."
        self.right_color_rec = (0,0,0)
        self.left_color_rec = (0,0,0)
        self.leg_correction = "WAITING..."
        self.leg_color_rec = (0,0,0)
        self.leg_correction_angle = "WAITING..."
        self.leg_ang_color_rec = (0,0,0)

    def angle(self, results, image):
        if results.pose_landmarks is not None:
            landmarks = results.pose_landmarks.landmark

            # GET COORDINATES OF JOINTS
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            # CALCULATE SOME REQUIRED METRICS ANGLES

            left_elbow_angle = np.round(self.calcs.calcAngle_3pts(left_shoulder,left_elbow,left_wrist))
            left_elbow_angle_hor = np.round(self.calcs.calcAngle_Horizontal(left_elbow,left_wrist))
            left_knee_angle = np.round(self.calcs.calcAngle_3pts(left_hip, left_knee, left_ankle))
            left_knee_angle_ver = np.round(self.calcs.calcAngle_Horizontal(left_knee,left_ankle))
            left_hip_angle = np.round(self.calcs.calcAngle_3pts(left_shoulder,left_hip, left_knee))

            right_elbow_angle = np.round(self.calcs.calcAngle_3pts(right_shoulder,right_elbow,right_wrist))
            right_elbow_angle_hor = np.round(self.calcs.calcAngle_Horizontal(right_wrist,right_elbow))
            right_knee_angle = np.round(self.calcs.calcAngle_3pts(right_hip, right_knee, right_ankle))
            right_knee_angle_ver = np.round(self.calcs.calcAngle_Horizontal(right_knee,right_ankle))
            right_hip_angle = np.round(self.calcs.calcAngle_3pts(right_shoulder,right_hip, right_knee))

         
            # VISUALIZE LANDMARSK
            # LEFT ARM
            cv2.putText(image, str(left_elbow_angle),
                  tuple(np.multiply(left_elbow,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,155,255),2, cv2.LINE_AA
                  )
            cv2.putText(image, "HOR: " + str(left_elbow_angle_hor),
                  tuple(np.multiply(left_wrist,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,155,255),2, cv2.LINE_AA
                  )
      
            # RIGHT ARM
            cv2.putText(image, str(right_elbow_angle),
                  tuple(np.multiply(right_elbow,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
            cv2.putText(image, "HOR: " + str(right_elbow_angle_hor),
                  tuple(np.multiply(right_wrist,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
      
            # LEFT KNEE
            cv2.putText(image, str(left_knee_angle),
                  tuple(np.multiply(left_knee,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
            cv2.putText(image, "VER: " + str(left_knee_angle_ver),
                  tuple(np.multiply(left_ankle,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
      
            # RIGHT KNEE
            cv2.putText(image, str(right_knee_angle),
                  tuple(np.multiply(right_knee,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
            cv2.putText(image, "VER: " + str(right_knee_angle_ver),
                  tuple(np.multiply(right_ankle,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
      
            # HIPS
            cv2.putText(image, str(left_hip_angle),
                  tuple(np.multiply(left_hip,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
            cv2.putText(image, str(right_hip_angle),
                  tuple(np.multiply(right_hip,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
        
            # POSTURE CORRECTION BLOCK
      
            # DETECT POSTURE ORIENTATION: RIGHT OR LEFT
            # WARRIOR 2 IS AN ASYMMETRIC POSTURE, SO FIRST WE TRY TO DETECT ORIENTATION
            if ((left_knee_angle > 155 and left_knee_angle < 205) or (left_knee_angle > -25 and left_knee_angle < 25)) and ((right_knee_angle > 60 and right_knee_angle < 130)):
                    self.pose_orientation = "RIGHT WARRIOR 2"
                    self.pose_color = (0,255,0) # GREEN COLOR
            elif ((right_knee_angle > 155 and right_knee_angle < 205) or (right_knee_angle > -25 and right_knee_angle < 25)) and ((left_knee_angle > 60 and left_knee_angle < 130)):
                    self.pose_orientation = "LEFT WARRIOR 2"
                    self.pose_color = (0,255,0) # GREEN COLOR
            else:
                    self.pose_orientation = "UNKNOWN"
                    self.pose_color = (0,0,0)
      
            # BOTH ARMS SHOULD BE EXTENDED (WITH ANGLE AT ELBOW ~ 180 DEGREES)
            # BOTH ARMS SHOULD BE HORIZONTAL (WITH ANGLE FROM HORIZONTAL ~ 0)
            # CORRECTIONS LEFT ARM
            if left_elbow_angle_hor > 20:
                self.left_arm_correct = "LEFT ARM TOO LOW"
                self.left_color_rec = (255,0,0)
            elif left_elbow_angle_hor < -20:
                self.left_arm_correct = "LEFT ARM TOO HIGH"
                self.left_color_rec = (255,0,0)
            elif left_elbow_angle_hor < 20 and left_elbow_angle_hor > -20:
                self.left_arm_correct = "GOOD"
                self.left_color_rec = (0,255,0) # GREEN COLOR
            #CORRECTIONS RIGHT ARM
            if right_elbow_angle_hor > 20:
                self.right_arm_correct = "RIGHT ARM TOO HIGH"
                self.right_color_rec = (255,0,0)
            elif right_elbow_angle_hor < -20:
                self.right_arm_correct = "RIGHT ARM TOO LOW"
                self.right_color_rec = (255,0,0)
            elif right_elbow_angle_hor < 20 and right_elbow_angle_hor > -20:
                self.right_arm_correct = "GOOD"
                self.right_color_rec = (0,255,0)  # GREEN COLOR

            #CORRECTIONS LEGS AND HIPS
            #BENDED LEG: FORELEG ANGLE SHOULD BE VERTICAL, WITH ~90 DEEGREE FROM FLOOR
            #BENDED LEG: ANGLE BETWEEN FORELEG AND TIGHT SHOULD BE ~ 90 DEGREES
            #FLEXED LEG: ANGLE BETWEEN FORELEG AND TIGHT SHOULD BE ~180 DEGREES
            #FLEXED LEG: ANGLE BETWEEN CORE AND TIGHT AT HIP SHOULD BE ~ 135 DEGREES


            if self.pose_orientation == "RIGHT WARRIOR":
                if right_knee_angle_ver > 110 or right_knee_angle_ver < 70:
                    self.leg_correction = "FORELEG SHOULD BE 90 WITH FLOOR"
                    self.leg_color_rec = (255,0,0)
                elif right_knee_angle_ver < 110 and right_knee_angle_ver > 70:
                    self.leg_correction = "GOOD"
                    self.leg_color_rec = (0,255,0)
                if right_knee_angle > 130 or right_knee_angle < 60:
                    self.leg_correction_angle = "FORELEG AND TIGHT SHOULD BE ~ 90"
                    self.leg_ang_color_rec = (255,0,0)
                elif right_knee_angle < 130 and right_knee_angle > 60:
                    self.leg_correction_angle = "GOOD"
                    self.leg_ang_color_rec = (0,255,0)
      
            if self.pose_orientation == "LEFT WARRIOR":
                if left_knee_angle_ver > 110 or left_knee_angle_ver < 70:
                    self.leg_correction = "FORELEG SHOULD BE 90 WITH FLOOR"
                    self.leg_color_rec = (255,0,0)
                elif left_knee_angle_ver < 110 and left_knee_angle_ver > 70:
                    self.leg_correction = "GOOD"
                    self.leg_color_rec = (0,255,0)
                if left_knee_angle > 130 or left_knee_angle < 60:
                    self.leg_correction_angle = "FORELEG AND TIGHT SHOULD BE ~ 90"
                    self.leg_ang_color_rec = (255,0,0)
                elif left_knee_angle < 130 and left_knee_angle > 60:
                    self.leg_correction_angle = "GOOD"
                    self.leg_ang_color_rec = (0,255,0)

        else:
            landmarks = None


        # RENDERING OF CORRECTIONS
        #ARM CORRECTIONS MESSAGES
        cv2.putText(image, "HINT ARMS:", (10,20),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),1,cv2.LINE_AA)
        cv2.putText(image, self.left_arm_correct, (10,60),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, self.left_color_rec,2,cv2.LINE_AA)
        cv2.putText(image, self.right_arm_correct, (10,100),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, self.right_color_rec,2,cv2.LINE_AA)
        #LEG CORRECTIONS MESSAGES
        cv2.putText(image, "HINT BENDED LEG:", (10,370),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),1,cv2.LINE_AA)
        cv2.putText(image, self.leg_correction, (10,410),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, self.leg_color_rec,2,cv2.LINE_AA)
        cv2.putText(image, self.leg_correction_angle, (10,450),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, self.leg_ang_color_rec,2,cv2.LINE_AA)
  
        #POSE DETECTION
        cv2.putText(image, "POSE:", (450,20),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(image, self.pose_orientation, (450,60),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,self.pose_color,2,cv2.LINE_AA)


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

        angleTotalArray = np.array(self.angle_list)
        timeTotalArray  = np.array(self.timeStamp_list)

        #res = self.calcs.fit_sin(self.timeStamp_list, self.angle_list)
        #plt.plot(timeTotalArray, angleTotalArray, color="navy", label='FirstTrial', linewidth=2.0)
        #plt.plot(timeTotalArray, res["fitfunc"](timeTotalArray), "r-", label="y fit curve", linewidth=2)
        #plt.title('Lunge Progression (raw)')
        #plt.xlabel('Timestamp (sec)')
        #plt.ylabel('HipKneeAngle')
        #plt.show()  