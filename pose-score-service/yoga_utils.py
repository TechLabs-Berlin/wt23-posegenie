from angle_calcs import Calculations
import mediapipe as mp
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC
import pickle

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


## SVC WITH RBF KERNEL CLASSIFIER
file1 = "yoga_poses_svc.model"
file2 = "yoga_poses_svc.labels"

loaded_model = pickle.load(open(file1, 'rb'))
loaded_labels = pickle.load(open(file2, 'rb'))
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

        #VARIABLES USING TO ANNOTATE VIDEO
        self.pose_orientation = "WAITING..."
        self.pose_color = (0,0,0)
        self.left_arm_correct = "WAITING..."
        self.right_arm_correct = "WAITING..."
        self.right_color_rec = (0,0,0)
        self.left_color_rec = (0,0,0)
        self.leg_correction = "WAITING..."
        self.leg_color_rec = (0,0,0)
        self.leg_correction_angle = "WAITING..."
        self.leg_ang_color_rec = (0,0,0)
        self.pose_ml_certain = "NOT DETECTED"
        self.pose_ml_certain_color = (0,0,0)

        #STORING FOR ANGLE ANALYZING
        self.left_arm_angle_list = []
        self.right_arm_angle_list = []
        self.left_knee_angle_list = []
        self.left_knee_ver_list = []
        self.right_knee_angle_list = []
        self.right_knee_ver_list =[]

        self.pose_list = []

        self.timestamps_list = [0.0]
        self.time_left_warrior = [0.0]
        self.time_right_warrior = [0.0]

    def angle(self, results, image):
        if results.pose_landmarks is not None:
            landmarks = results.pose_landmarks.landmark

            timestamps_now = self.cap.get(cv2.CAP_PROP_POS_MSEC)
            self.timestamps_list.append(timestamps_now)

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
            # ANGLE FROM HORIZONTALS ARE POSITIVE CLOCKWISE, SO REQUIRES MINOR ADJUST TO BE CONSISTENT FOR SYMMETRY

            left_elbow_angle = np.round(self.calcs.calcAngle_3pts(left_shoulder,left_elbow,left_wrist)).astype(int)
            #left_elbow_angle_hor = np.round(self.calcs.calcAngle_Horizontal(left_elbow,left_wrist)).astype(int)
            left_elbow_angle_hor = np.round(-self.calcs.calcAngle_Horizontal(left_elbow,left_wrist)).astype(int) #sign changed to be consistent for symmetry
            left_knee_angle = np.round(self.calcs.calcAngle_3pts(left_hip, left_knee, left_ankle)).astype(int)
            left_knee_angle_ver = np.round(self.calcs.calcAngle_Horizontal(left_knee,left_ankle)).astype(int)
            left_hip_angle = np.round(self.calcs.calcAngle_3pts(left_shoulder,left_hip, left_knee)).astype(int)

            right_elbow_angle = np.round(self.calcs.calcAngle_3pts(right_shoulder,right_elbow,right_wrist)).astype(int)
            right_elbow_angle_hor = np.round(self.calcs.calcAngle_Horizontal(right_wrist,right_elbow)).astype(int)
            right_knee_angle = np.round(self.calcs.calcAngle_3pts(right_hip, right_knee, right_ankle)).astype(int)
            right_knee_angle_ver = np.round(180-self.calcs.calcAngle_Horizontal(right_knee,right_ankle)).astype(int) #changed to be consistent for symmetry
            #right_knee_angle_ver = np.round(self.calcs.calcAngle_Horizontal(right_knee,right_ankle)).astype(int)
            right_hip_angle = np.round(self.calcs.calcAngle_3pts(right_shoulder,right_hip, right_knee)).astype(int)
            
            markers0 = left_elbow_angle, left_elbow_angle_hor, left_knee_angle, left_knee_angle_ver, left_hip_angle, right_elbow_angle, right_elbow_angle_hor, right_knee_angle, right_knee_angle_ver, right_hip_angle
      
            #=============================================
            # GET ML PREDICTION
            #=============================================
            predict_label = (loaded_model.predict(np.array(markers0).reshape(1, -1)))
            pose_ml_detected = loaded_labels[predict_label[0]].upper()
            probabilities = loaded_model.predict_proba(np.array(markers0).reshape(1, -1))
            #probabilities.max()

            if probabilities.max()>0.60:
                self.pose_ml_certain = pose_ml_detected
                self.pose_ml_certain_color = (0,255,0)
            else:
                self.pose_ml_certain = "LOW PROB"
                self.pose_ml_certain_color = (0,0,0)
            #===============================================
            #===============================================  
         
            # VISUALIZE LANDMARSK
            # LEFT ARM
            cv2.putText(image, str(left_elbow_angle),
                  tuple(np.multiply(left_elbow,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
            cv2.putText(image, "HOR: " + str(left_elbow_angle_hor),
                  tuple(np.multiply(left_wrist,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
      
            # RIGHT ARM
            cv2.putText(image, str(right_elbow_angle),
                  tuple(np.multiply(right_elbow,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
            cv2.putText(image, "HOR: " + str(right_elbow_angle_hor),
                  tuple(np.multiply(right_wrist,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
      
            # LEFT KNEE
            cv2.putText(image, str(left_knee_angle),
                  tuple(np.multiply(left_knee,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
            cv2.putText(image, "VER: " + str(left_knee_angle_ver),
                  tuple(np.multiply(left_ankle,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
      
            # RIGHT KNEE
            cv2.putText(image, str(right_knee_angle),
                  tuple(np.multiply(right_knee,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
            cv2.putText(image, "VER: " + str(right_knee_angle_ver),
                  tuple(np.multiply(right_ankle,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
      
            # HIPS
            cv2.putText(image, str(left_hip_angle),
                  tuple(np.multiply(left_hip,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
            cv2.putText(image, str(right_hip_angle),
                  tuple(np.multiply(right_hip,[self.width, self.height]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
        
            # ============================================================
            # PRELIMINARY POSTURE DETECTION
            # ============================================================

            # FIRST, DETECT POSTURE ORIENTATION: RIGHT OR LEFT
            # WARRIOR 2 IS AN ASYMMETRIC POSTURE, SO FIRST WE TRY TO DETECT ORIENTATION
            # CHECK THREE INDICATORS:
            #1: back leg is extended with angle between hip-knee-angle ~ 180 (range 150 - 210)
            #2: front leg is bended with angle between hip-knee-angle ~ 90 (range 70-150)
            #3: arms are extended and horizontal, angle with horizontal within 45 degrees (-45 to 45)
            if ((left_knee_angle > 150 and left_knee_angle < 210)) and ((right_knee_angle > 70 and right_knee_angle < 150) and (left_knee_angle_ver<75)) and (right_elbow_angle_hor < 45 and right_elbow_angle_hor > -45) and  (left_elbow_angle_hor < 45 and left_elbow_angle_hor > -45):
                    self.pose_orientation = "RIGHT WARRIOR 2"
                    self.pose_color = (0,255,0) # GREEN COLOR
            elif ((right_knee_angle > 150 and right_knee_angle < 210)) and ((left_knee_angle > 70 and left_knee_angle < 150) and (right_knee_angle_ver<75)) and (right_elbow_angle_hor < 45 and right_elbow_angle_hor > -45) and  (left_elbow_angle_hor < 45 and left_elbow_angle_hor > -45):
                    self.pose_orientation = "LEFT WARRIOR 2"
                    self.pose_color = (0,255,0) # GREEN COLOR
            else:
                    self.pose_orientation = "UNKNOWN"
                    self.pose_color = (0,0,0)

            if self.pose_orientation == "LEFT WARRIOR 2":
                time_left_warrior_now = self.timestamps_list[-1]-self.timestamps_list[-2]
                self.time_left_warrior.append(time_left_warrior_now)
                total_time = (np.round(np.sum(self.time_left_warrior)/1000,1))

            elif self.pose_orientation == "RIGHT WARRIOR 2":
                time_right_warrior_now = self.timestamps_list[-1]-self.timestamps_list[-2]
                self.time_right_warrior.append(time_right_warrior_now)
                total_time = (np.round(np.sum(self.time_right_warrior)/1000,1))
            else:
                total_time = 0

            # ==================================================
            # STORE AND EXPAND LISTS
            # ==================================================
            
            self.left_arm_angle_list.append((left_elbow_angle_hor))
            self.right_arm_angle_list.append((right_elbow_angle_hor))

            self.left_knee_angle_list.append(left_knee_angle)
            self.left_knee_ver_list.append(left_knee_angle_ver)
            self.right_knee_angle_list.append(right_knee_angle)
            self.right_knee_ver_list.append(right_knee_angle_ver)


            self.pose_list.append(self.pose_orientation)

            self.timeStamp_list.append(round(float(self.read_upload.get_timestamps())/1000, 5))
      
            # ==============================================================
            # POSTURE CORRECTION BLOCK
            # ==============================================================


            # BOTH ARMS SHOULD BE EXTENDED (WITH ANGLE AT ELBOW ~ 180 DEGREES)
            # BOTH ARMS SHOULD BE HORIZONTAL (WITH ANGLE FROM HORIZONTAL ~ 0)
            if (self.pose_orientation == "LEFT WARRIOR 2") or (self.pose_orientation == "RIGHT WARRIOR 2"):
                # CORRECTIONS LEFT ARM
                if left_elbow_angle_hor > 20:
                    self.left_arm_correct = "LEFT ARM TOO HIGH"
                    self.left_color_rec = (255,0,0)
                elif left_elbow_angle_hor < -20:
                    self.left_arm_correct = "LEFT ARM TOO LOW"
                    self.left_color_rec = (255,0,0)
                elif left_elbow_angle_hor <= 20 and left_elbow_angle_hor >= -20:
                    self.left_arm_correct = "GOOD"
                    self.left_color_rec = (0,255,0) # GREEN COLOR
                #CORRECTIONS RIGHT ARM
                if right_elbow_angle_hor > 20:
                    self.right_arm_correct = "RIGHT ARM TOO HIGH"
                    self.right_color_rec = (255,0,0)
                elif right_elbow_angle_hor < -20:
                    self.right_arm_correct = "RIGHT ARM TOO LOW"
                    self.right_color_rec = (255,0,0)
                elif right_elbow_angle_hor <= 20 and right_elbow_angle_hor >= -20:
                    self.right_arm_correct = "GOOD"
                    self.right_color_rec = (0,255,0)  # GREEN COLOR
            else:
                self.left_arm_correct = "WAITING..."
                self.left_color_rec = (0,0,0)
                self.right_arm_correct = "WAITING..."
                self.right_color_rec = (0,0,0)     

            #CORRECTIONS LEGS AND HIPS
            #BENDED LEG: FORELEG ANGLE SHOULD BE VERTICAL, WITH ~90 DEEGREE FROM FLOOR
            #BENDED LEG: ANGLE BETWEEN FORELEG AND TIGHT SHOULD BE ~ 90 DEGREES
            #FLEXED LEG: ANGLE BETWEEN FORELEG AND TIGHT SHOULD BE ~180 DEGREES
            #FLEXED LEG: ANGLE BETWEEN CORE AND TIGHT AT HIP SHOULD BE ~ 135 DEGREES


            if self.pose_orientation == "RIGHT WARRIOR 2":
                if right_knee_angle_ver > 110 or right_knee_angle_ver < 70:
                    self.leg_correction = "FORELEG SHOULD BE VERTICAL"
                    self.leg_color_rec = (255,0,0)
                elif right_knee_angle_ver <= 110 and right_knee_angle_ver >= 70:
                    self.leg_correction = "GOOD"
                    self.leg_color_rec = (0,255,0)
                if right_knee_angle > 140 or right_knee_angle < 60:
                    self.leg_correction_angle = "ANGLE SHOULD BE ~115"
                    self.leg_ang_color_rec = (255,0,0)
                elif right_knee_angle <= 140 and right_knee_angle >= 60:
                    self.leg_correction_angle = "GOOD"
                    self.leg_ang_color_rec = (0,255,0)
      
            elif self.pose_orientation == "LEFT WARRIOR 2":
                if left_knee_angle_ver > 110 or left_knee_angle_ver < 70:
                    self.leg_correction = "FORELEG SHOULD BE VERTICAL"
                    self.leg_color_rec = (255,0,0)
                elif left_knee_angle_ver <= 110 and left_knee_angle_ver >= 70:
                    self.leg_correction = "GOOD"
                    self.leg_color_rec = (0,255,0)
                if left_knee_angle > 140 or left_knee_angle < 60:
                    self.leg_correction_angle = "ANGLE SHOULD BE ~115"
                    self.leg_ang_color_rec = (255,0,0)
                elif left_knee_angle <= 140 and left_knee_angle >= 60:
                    self.leg_correction_angle = "GOOD"
                    self.leg_ang_color_rec = (0,255,0)
            else:
                self.leg_correction = "WAITING..."
                self.leg_correction_angle = "WAITING..."
                self.leg_color_rec = (0,0,0)
                self.leg_ang_color_rec = (0,0,0)     

        else:
            landmarks = None


        # RENDERING OF CORRECTIONS
        #ARM CORRECTIONS MESSAGES
        cv2.putText(image, "HINT ARMS:", (10,20),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(image, self.left_arm_correct, (10,60),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, self.left_color_rec,2,cv2.LINE_AA)
        cv2.putText(image, self.right_arm_correct, (10,100),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, self.right_color_rec,2,cv2.LINE_AA)
        #LEG CORRECTIONS MESSAGES
        cv2.putText(image, "HINT FRONT LEG:", (10,200),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(image, self.leg_correction, (10,240),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, self.leg_color_rec,2,cv2.LINE_AA)
        cv2.putText(image, self.leg_correction_angle, (10,280),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, self.leg_ang_color_rec,2,cv2.LINE_AA)
  
        #POSE DETECTION
        cv2.putText(image, "POSE:", (350,20),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(image, self.pose_orientation, (350,60),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,self.pose_color,2,cv2.LINE_AA)
        #IN POSE timestamps_calc_now
        cv2.putText(image, "TIME IN POSE: " + str(total_time) + " secs", (350,100),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),2,cv2.LINE_AA)


        #ML MODEL DETECTION
        cv2.putText(image, "ML DETECTION (BETA)", (650,20),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(image, self.pose_ml_certain + " (PROB: " + np.round((probabilities.max()),2).astype(str) + ")", (650,60),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,self.pose_ml_certain_color,2,cv2.LINE_AA)

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))
    
    def make_output_filename(self, file_path, suffix="_annotated"):
        print(f"out: {self.filename}")
        # Output filename
        # FIXME: Replace forward slash with detection from a cross platform library
        outdir = self.filename[:self.filename.rfind('/')+1]
        inputflnm = self.filename[self.filename.rfind('/')+1:]
        
        inflnm, inflext = inputflnm.split('.')
        out_filename = f'{outdir}{inflnm}{suffix}.{inflext}'

        return out_filename


    def visualize(self):
        out_filename = self.make_output_filename(self.filename)

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


        timeTotalArray  = np.array(self.timeStamp_list)

        df_pose = pd.DataFrame(self.pose_list, columns=["Pose"])
        df=pd.concat([df_pose, pd.Series(self.left_arm_angle_list), pd.Series(self.right_arm_angle_list), pd.Series(self.left_knee_angle_list),pd.Series(self.right_knee_angle_list), pd.Series(self.left_knee_ver_list),pd.Series(self.right_knee_ver_list)],axis=1).rename(columns={0:"left arm", 1:"right arm", 2:"left knee ang", 3:"right knee ang", 4:"left knee ver",5:"right knee ver"})
        
        # FILTER DATA FOR IMPLEMENTED POSES: Warrior 2
        df["Pose Code"] = pd.Categorical(df["Pose"],ordered=True, categories=["UNKNOWN", "LEFT WARRIOR 2", "RIGHT WARRIOR 2"]).codes
        filt_pose1 = df["Pose Code"] == 1 # LEFT WARRIOR 2
        filt_pose2 = df["Pose Code"] == 2 # RIGHT WARRIOR 2


        # PLOT DATA FOR IMPLEMENTED POSES: Warrior 2

        # close/clear existing plt plot in case opening after other exercises
        plt.close()

        plt.rcParams['figure.figsize'] = [18, 6]
        plt.rcParams['figure.dpi'] = 100 # 200 e.g. is really fine, but slower

        #ARMS
        expected_arm_angle = 0
        range = 30

        plt.plot(timeTotalArray, df["left arm"], color="gray",  linestyle='dashed', linewidth=0.50)
        plt.plot(timeTotalArray, df["right arm"], color="gray",  linestyle='dashed',  linewidth=0.50)
        plt.plot(timeTotalArray, timeTotalArray*expected_arm_angle, color="green",  linestyle='dashed', linewidth=2)
        plt.plot(timeTotalArray, timeTotalArray*0+range,color="black",  linestyle='dashed',linewidth=0.50)
        plt.plot(timeTotalArray, timeTotalArray*0-range, color="black",  linestyle='dashed',linewidth=0.50)

        plt.scatter(timeTotalArray[filt_pose1], df["left arm"][filt_pose1],8, color="blue")
        plt.scatter(timeTotalArray[filt_pose1], df["right arm"][filt_pose1],8, color="black")

        plt.scatter(timeTotalArray[filt_pose2], df["left arm"][filt_pose2],8, color="blue")
        plt.scatter(timeTotalArray[filt_pose2], df["right arm"][filt_pose2],8, color="black")

        plt.fill_between(timeTotalArray, expected_arm_angle-range, expected_arm_angle+range, alpha=0.10, color="green")
        plt.fill_between(timeTotalArray, expected_arm_angle-range*2/3, expected_arm_angle+range*2/3, alpha=0.10, color="green")
        plt.fill_between(timeTotalArray, expected_arm_angle-range*1/3, expected_arm_angle+range*1/3, alpha=0.10, color="green")

        #FRONT LEG ANGLE
        front_leg_ang_expect = 115
        front_leg_ang_expect_range = 45  # Detection limit

        plt.plot(timeTotalArray, df["left knee ang"], color="gray",  linestyle='dashed', linewidth=0.50)
        plt.plot(timeTotalArray, df["right knee ang"], color="gray",  linestyle='dashed', linewidth=0.50)
        plt.plot(timeTotalArray, timeTotalArray*0+front_leg_ang_expect, color="green",  linestyle='dashed', linewidth=2)
        plt.plot(timeTotalArray, timeTotalArray*0+front_leg_ang_expect+front_leg_ang_expect_range, color="gray",  linestyle='dashed', linewidth=0.5)

        # FRONT LEG LEFT WARRIOR
        plt.scatter(timeTotalArray[filt_pose1], df["left knee ang"][filt_pose1],8, color="black")
        # FRONT LEG RIGHT WARRIOR
        plt.scatter(timeTotalArray[filt_pose2], df["right knee ang"][filt_pose2],8, color="black")

        plt.fill_between(timeTotalArray, front_leg_ang_expect, front_leg_ang_expect+front_leg_ang_expect_range, alpha=0.10, color="green")
        plt.fill_between(timeTotalArray, front_leg_ang_expect, front_leg_ang_expect+front_leg_ang_expect_range*2/3, alpha=0.10, color="green")
        plt.fill_between(timeTotalArray, front_leg_ang_expect, front_leg_ang_expect+front_leg_ang_expect_range*1/3, alpha=0.10, color="green")

        back_leg_ver_expect = 45
        back_leg_ver_expect_range = 30 #detection limit

        plt.plot(timeTotalArray, df["left knee ver"], color="gray",  linestyle='dashed', linewidth=0.5)
        plt.plot(timeTotalArray, df["right knee ver"], color="gray",  linestyle='dashed',  linewidth=0.5)
        plt.plot(timeTotalArray, timeTotalArray*0+ back_leg_ver_expect , color="green",  linestyle='dashed',  label='Front Leg Bend = 90', linewidth=2)
        plt.plot(timeTotalArray, timeTotalArray*0+ back_leg_ver_expect + back_leg_ver_expect_range, color="gray",  linestyle='dashed', linewidth=0.5)

        # BACK LEG LEFT WARRIOR
        plt.scatter(timeTotalArray[filt_pose1], df["right knee ver"][filt_pose1],8,color="black")
        # BACK LEG LEFT WARRIOR
        plt.scatter(timeTotalArray[filt_pose2], df["left knee ver"][filt_pose2],8,color="black")


        plt.fill_between(timeTotalArray, back_leg_ver_expect, back_leg_ver_expect+back_leg_ver_expect_range, alpha=0.10, color="green")
        plt.fill_between(timeTotalArray, back_leg_ver_expect, back_leg_ver_expect+(back_leg_ver_expect_range)*2/3, alpha=0.10, color="green")
        plt.fill_between(timeTotalArray, back_leg_ver_expect, back_leg_ver_expect+(back_leg_ver_expect_range)*1/3, alpha=0.10, color="green")

        try:
            plt.axvspan(timeTotalArray[filt_pose1].min(), timeTotalArray[filt_pose1].max() , color='gray', alpha=0.25)
            plt.text(timeTotalArray[filt_pose1].min(),165,"DETECTED POSE:")
            plt.text(timeTotalArray[filt_pose1].min(),155,df[filt_pose1]["Pose"].iloc[0],fontweight='bold')
            pose1_count =np.sum(np.diff(timeTotalArray[filt_pose1]))
            time_string1 = " Total time spent in correct Left Warrior 2 pose is " + str(pose1_count.astype(int)) + " seconds, which is " + str(((pose1_count/max(timeTotalArray))*100).astype(int)) + "% of total video time"
            plt.text(0,-110,time_string1,fontsize=15, color="black")
        except:
            pass
        
        try:
            plt.axvspan(timeTotalArray[filt_pose2].min(), timeTotalArray[filt_pose2].max() , color='gray', alpha=0.25)
            plt.text(timeTotalArray[filt_pose2].min(),165,"DETECTED POSE:")
            plt.text(timeTotalArray[filt_pose2].min(),155,df[filt_pose2]["Pose"].iloc[0],fontweight='bold')
            pose2_count = np.sum(np.diff(timeTotalArray[filt_pose2]))
            time_string2 = " Total time spent in correct Right Warrior 2 pose is " + str(pose2_count.astype(int)) + " seconds, which is " + str(((pose2_count/max(timeTotalArray))*100).astype(int)) + "% of total video time"
            plt.text(0,-130,time_string2 ,fontsize=15, color="black")
        except:
            pass

        plt.text(0,front_leg_ang_expect+4," advanced", fontsize=9)
        plt.text(0,front_leg_ang_expect+17," intermediate",fontsize=9)
        plt.text(0,front_leg_ang_expect+32," beginner",fontsize=9)

        plt.text(0,back_leg_ver_expect+3," advanced", fontsize=9)
        plt.text(0,back_leg_ver_expect+13," intermediate",fontsize=9)
        plt.text(0,back_leg_ver_expect+22," beginner",fontsize=9)

        plt.text(0,expected_arm_angle+4," advanced", fontsize=9)
        plt.text(0,expected_arm_angle+13," intermediate",fontsize=9)
        plt.text(0,expected_arm_angle+23," beginner",fontsize=9)
        plt.text(0,expected_arm_angle-6," advanced", fontsize=9)
        plt.text(0,expected_arm_angle-16," intermediate",fontsize=9)
        plt.text(0,expected_arm_angle-26," beginner",fontsize=9)


        plt.text(0,-46," LEFT ARM IN BLUE",fontsize=10, color="blue")

        plt.annotate("FRONT LEG ANGLE\nOptimal = 115°", xy=(0,115),xycoords="data",
             xytext=(-0.12,0.7325), textcoords='axes fraction', fontsize = 10,
            va='center', ha='left',
            arrowprops=dict(facecolor='black', shrink=0.00, width=1))

        plt.annotate("BACK LEG ANGLE\nOptimal = 45°", xy=(0,45),xycoords="data",
             xytext=(-0.12,0.423), textcoords='axes fraction', fontsize = 10,
            va='center', ha='left',
            arrowprops=dict(facecolor='black', shrink=0.00, width=1))

        plt.annotate("ARMS ANGLE\nOptimal = 0°", xy=(0,0),xycoords="data",
             xytext=(-0.12,0.225), textcoords='axes fraction', fontsize = 10,
            va='center', ha='left',
            arrowprops=dict(facecolor='black', shrink=0.00, width=1))


        plt.ylim(-50,175)
        plt.xlim(0,max(timeTotalArray))

        plt.title("WARRIOR 2: Legs & Arms Angle Progression", fontsize = 15)
        plt.xlabel("Time [seconds]",fontsize = 15)


        plt.savefig(f"{self.filename}.png",  bbox_inches="tight") 
