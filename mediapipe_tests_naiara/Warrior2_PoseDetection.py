# WARRIOR 2 POSE DETECTION SCRIPT
# by Naiara Fernandez
# 
# Open the camera feed and shows Mediapipe Landmarks on top of image
# Detects orientation of Warrior 2 pose, right or left position
# Detects missalignements of arms, and bended leg

#pip install mediapipe opencv-python math numpy

############################################################
# IMPORT REQUIRED MODULES
############################################################


import cv2
import mediapipe as mp
import numpy as np
import math
import time
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


############################################################
# DEFINE FUNCTIONS BLOCK
############################################################
# Not all of these functions are used at the moment

#FROM YOUTUBE TUTORIAL (WORKS BETTER)
def calculate_angle(a,b,c):
    a = np.array(a) #First
    b = np.array(b) #Mid
    c = np.array(c) #End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle 

#FROM MR.POSE
def angle(point1, point2, point3):
    if (point1==(0,0) or point2==(0,0) or point3==(0,0)):
        return 0
    
    numerator = point2[1] * (point1[0] - point3[0]) + point1[1] * \
                (point3[0] - point2[0]) + point3[1] * (point2[0] - point1[0])
    denominator = (point2[0] - point1[0]) * (point1[0] - point3[0]) + \
                (point2[1] - point1[1]) * (point1[1] - point3[1])
    try:
        ang = math.atan(numerator/denominator)
        ang = ang * 180 / math.pi
        if ang < 0:
            ang = 180 + ang
        return ang
    except:
        return 90.0


def angle_of_singleline(point1, point2):
    """ Calculate angle of a single line """
    x_diff = point2[0] - point1[0]
    y_diff = point2[1] - point1[1]
    return math.degrees(math.atan2(y_diff, x_diff))


def dist_xy(point1, point2):
    """ Euclidean distance between two points point1, point2 """
    diff_point1 = (point1[0] - point2[0]) ** 2
    diff_point2 = (point1[1] - point2[1]) ** 2
    return (diff_point1 + diff_point2) ** 0.5


def point_position(point, line_pt_1, line_pt_2):
    """
    Left or Right position of the point from a line
    """
    value = (line_pt_2[0] - line_pt_1[0]) * (point[1] - line_pt_1[1]) - \
                (line_pt_2[1] - line_pt_1[1]) * (point[0] - line_pt_1[0])
    if value >= 0:
        return "left"
    return "right"
#########################################################################
# END FUNCTION DEFINITION BLOC
#########################################################################


#########################################################################
# MAIN BLOCK OF CODE
#########################################################################
# START VIDEO CAPTURE FOR LIVE FEED
cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    ret, frame = cap.read()

    # Recolor image
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image.flags.writeable = False
    # Make detection
    results = pose.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    cv2.namedWindow("Mediapipe Feed", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Mediapipe Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    #DEFINE INITIAL VARIABLES FOR POSTURE DETECTION MESSAGES AND COLORS
    pose_orientation = "WAITING..."
    left_arm_correct = "WAITING..."
    right_arm_correct = "WITING..."
    right_color_rec = (0,0,0)
    left_color_rec = (0,0,0)
    leg_correction = "WAITING..."
    leg_color_rec = (0,0,0)
    leg_correction_angle = "WAITING..."
    leg_ang_color_rec = (0,0,0)

    
    try:

      # EXTRACT MEDIAPIPE LANDMARKS
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

      left_elbow_angle = np.round(calculate_angle(left_shoulder,left_elbow,left_wrist))
      left_elbow_angle_hor = np.round(angle_of_singleline(left_elbow,left_wrist))
      left_knee_angle = np.round(calculate_angle(left_hip, left_knee, left_ankle))
      left_knee_angle_ver = np.round(angle_of_singleline(left_knee,left_ankle))
      left_hip_angle = np.round(calculate_angle(left_shoulder,left_hip, left_knee))

      right_elbow_angle = np.round(calculate_angle(right_shoulder,right_elbow,right_wrist))
      right_elbow_angle_hor = np.round(angle_of_singleline(right_wrist,right_elbow))
      right_knee_angle = np.round(calculate_angle(right_hip, right_knee, right_ankle))
      right_knee_angle_ver = np.round(angle_of_singleline(right_knee,right_ankle))
      right_hip_angle = np.round(calculate_angle(right_shoulder,right_hip, right_knee))
      
    
      
      # VISUALIZE LANDMARSK
      # LEFT ARM
      cv2.putText(image, str(left_elbow_angle),
                  tuple(np.multiply(left_elbow,[640,480]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,155,255),2, cv2.LINE_AA
                  )
      cv2.putText(image, "HOR: " + str(left_elbow_angle_hor),
                  tuple(np.multiply(left_wrist,[640,480]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,155,255),2, cv2.LINE_AA
                  )
      
      # RIGHT ARM
      cv2.putText(image, str(right_elbow_angle),
                  tuple(np.multiply(right_elbow,[640,480]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
      cv2.putText(image, "HOR: " + str(right_elbow_angle_hor),
                  tuple(np.multiply(right_wrist,[640,480]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
      
      # LEFT KNEE
      cv2.putText(image, str(left_knee_angle),
                  tuple(np.multiply(left_knee,[640,480]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
      cv2.putText(image, "VER: " + str(left_knee_angle_ver),
                  tuple(np.multiply(left_ankle,[640,480]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
      
      # RIGHT KNEE
      cv2.putText(image, str(right_knee_angle),
                  tuple(np.multiply(right_knee,[640,480]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
      cv2.putText(image, "VER: " + str(right_knee_angle_ver),
                  tuple(np.multiply(right_ankle,[640,480]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2, cv2.LINE_AA
                  )
      
      # HIPS
      cv2.putText(image, str(left_hip_angle),
                  tuple(np.multiply(left_hip,[640,480]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
      cv2.putText(image, str(right_hip_angle),
                  tuple(np.multiply(right_hip,[640,480]).astype(int)),
                  cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),2, cv2.LINE_AA
                  )
      

      # POSTURE CORRECTION BLOCK
      
      # DETECT POSTURE ORIENTATION: RIGHT OR LEFT
      # WARRIOR 2 IS AN ASYMMETRIC POSTURE, SO FIRST WE TRY TO DETECT ORIENTATION
      if ((left_knee_angle > 155 and left_knee_angle < 205) or (left_knee_angle > -25 and left_knee_angle < 25)) and ((right_knee_angle > 60 and right_knee_angle < 130)):
        pose_orientation = "RIGHT WARRIOR"
      elif ((right_knee_angle > 155 and right_knee_angle < 205) or (right_knee_angle > -25 and right_knee_angle < 25)) and ((left_knee_angle > 60 and left_knee_angle < 130)):
        pose_orientation = "LEFT WARRIOR"
      else:
        pose_orientation = "UNKNOWN"
      
      # BOTH ARMS SHOULD BE EXTENDED (WITH ANGLE AT ELBOW ~ 180 DEGREES)
      # BOTH ARMS SHOULD BE HORIZONTAL (WITH ANGLE FROM HORIZONTAL ~ 0)
      # CORRECTIONS LEFT ARM
      if left_elbow_angle_hor > 15:
        left_arm_correct = "LEFT ARM TOO LOW"
        left_color_rec = (255,0,0)
      elif left_elbow_angle_hor < -15:
        left_arm_correct = "LEFT ARM TOO HIGH"
        left_color_rec = (255,0,0)
      elif left_elbow_angle_hor < 15 and left_elbow_angle_hor > -15:
        left_arm_correct = "GOOD"
        left_color_rec = (0,255,0) # GREEN COLOR
      #CORRECTIONS RIGHT ARM
      if right_elbow_angle_hor > 15:
        right_arm_correct = "RIGHT ARM TOO HIGH"
        right_color_rec = (255,0,0)
      elif right_elbow_angle_hor < -15:
        right_arm_correct = "RIGHT ARM TOO LOW"
        right_color_rec = (255,0,0)
      elif right_elbow_angle_hor < 15 and right_elbow_angle_hor > -15:
        right_arm_correct = "GOOD"
        right_color_rec = (0,255,0)  # GREEN COLOR

      #CORRECTIONS LEGS AND HIPS
      #BENDED LEG: FORELEG ANGLE SHOULD BE VERTICAL, WITH ~90 DEEGREE FROM FLOOR
      #BENDED LEG: ANGLE BETWEEN FORELEG AND TIGHT SHOULD BE ~ 90 DEGREES
      #FLEXED LEG: ANGLE BETWEEN FORELEG AND TIGHT SHOULD BE ~180 DEGREES
      #FLEXED LEG: ANGLE BETWEEN CORE AND TIGHT AT HIP SHOULD BE ~ 135 DEGREES


      if pose_orientation == "RIGHT WARRIOR":
        if right_knee_angle_ver > 110 or right_knee_angle_ver < 70:
          leg_correction = "FORELEG SHOULD BE 90 WITH FLOOR"
          leg_color_rec = (255,0,0)
        elif right_knee_angle_ver < 100 and right_knee_angle_ver > 80:
          leg_correction = "GOOD"
          leg_color_rec = (0,255,0)
        if right_knee_angle > 100 or right_knee_angle < 80:
          leg_correction_angle = "FORE LEG AND TIGHT SHOULD BE AT 90"
          leg_ang_color_rec = (255,0,0)
        elif right_knee_angle < 100 and right_knee_angle > 80:
          leg_correction_angle = "GOOD"
          leg_ang_color_rec = (0,255,0)
      
      if pose_orientation == "LEFT WARRIOR":
        if left_knee_angle_ver > 110 or left_knee_angle_ver < 70:
          leg_correction = "FORELEG SHOULD BE 90 WITH FLOOR"
          leg_color_rec = (255,0,0)
        elif left_knee_angle_ver < 100 and left_knee_angle_ver > 80:
          leg_correction = "GOOD"
          leg_color_rec = (0,255,0)
        if left_knee_angle > 120 or left_knee_angle < 70:
          leg_correction_angle = "FORELEG AND TIGHT SHOULD BE AT 90"
          leg_ang_color_rec = (255,0,0)
        elif left_knee_angle < 120 and left_knee_angle > 70:
          leg_correction_angle = "GOOD"
          leg_ang_color_rec = (0,255,0)

    
      # POSE HOLDING COUNTER
      if right_arm_correct == "GOOD" and left_arm_correct == "GOOD" and leg_correction == "GOOD" and leg_correction_angle == "GOOD":
         check = right



      #print(landmarks)
    except:
      pass
    
    #ARM CORRECTIONS MESSAGES
    cv2.putText(image, "HINT ARMS:", (10,20),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),1,cv2.LINE_AA)
    cv2.putText(image, left_arm_correct, (10,60),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, left_color_rec,2,cv2.LINE_AA)
    cv2.putText(image, right_arm_correct, (10,100),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, right_color_rec,2,cv2.LINE_AA)
    #LEG CORRECTIONS MESSAGES
    cv2.putText(image, "HINT BENDED LEG:", (10,370),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),1,cv2.LINE_AA)
    cv2.putText(image, leg_correction, (10,410),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, leg_color_rec,2,cv2.LINE_AA)
    cv2.putText(image, leg_correction_angle, (10,450),
                cv2.FONT_HERSHEY_SIMPLEX,0.75, leg_ang_color_rec,2,cv2.LINE_AA)
  
  

    #POSE DETECTION
    cv2.putText(image, "POSE:", (450,20),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),1,cv2.LINE_AA)
    cv2.putText(image, pose_orientation, (450,60),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,0),1,cv2.LINE_AA)
    
    #Setup Orientation box

    # Render detections
    mp_drawing.draw_landmarks(image, results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245,117,66),thickness=2, circle_radius=2),
                              mp_drawing.DrawingSpec(color=(245,66,230),thickness=2, circle_radius=2)
                              )


    #print(results)


  
    cv2.imshow("Mediapipe Feed", image)

    if cv2.waitKey(10) & 0xFF == ord("q"):
      break

  cap.release()
  cv2.destroyAllWindows()