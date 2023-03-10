import cv2
import mediapipe as mp
import numpy as np
import math
import sys

##############################
# HOW TO RUN: python3 lunge.py <filename>
##############################

# readUpload
class readUpload:
    def __init__(self, filename, pose):
        self.filename = filename
        self.pose = pose
        self.cap = cv2.VideoCapture(self.filename)
        
    def recolor_RGB(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        if frame is None: 
            return("a")
        else:
            results = self.pose.process(frame)
            return image, results
    
    def calcAngle_3pts(self,a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
    
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
    
        if angle >180.0:
            angle = 360-angle
        return angle 
    
    def calcAngle_2lines(self,line1, line2):        
        d1 = (line1[1][0] - line1[0][0], line1[1][1] - line1[0][1])
        d2 = (line2[1][0] - line2[0][0], line2[1][1] - line2[0][1])
        # Compute dot product
        p = d1[0] * d2[0] + d1[1] * d2[1]
        # Compute norms
        n1 = math.sqrt(d1[0] * d1[0] + d1[1] * d1[1])
        n2 = math.sqrt(d2[0] * d2[0] + d2[1] * d2[1])
        # Compute angle
        ang = math.acos(p / (n1 * n2))
        # Convert to degrees if you want
        ang = math.degrees(ang)
        return ang

    def calcAngle_Horizontal(self,point1, point2):
        """ Calculate angle of a single line """
        x_diff = point2[0] - point1[0]
        y_diff = point2[1] - point1[1]
        return math.degrees(math.atan2(y_diff, x_diff))
    
# Pushup pose
class Pushup(readUpload):
    def __init__(self, filename, pose):
        super().__init__(filename, pose)
        self.reps = 0 
        self.stage = ""
        self.hint = ""

    def angle(self, results, image, frame_width, frame_height):
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
            lKnee_angle = round(self.calcAngle_3pts(left_hip, left_knee, left_ankle),2)
            rKnee_angle = round(self.calcAngle_3pts(right_hip, right_knee, right_ankle),2)
            back_angle = round(self.calcAngle_Horizontal(left_shoulder, left_hip),2)

            # Knee & Ankle angle with the horizontal plane
            rKnee_trailing = round(self.calcAngle_Horizontal(right_knee, right_ankle),2)
            lKnee_trailing = round(self.calcAngle_Horizontal(left_knee, left_ankle),2)

            # lunge HipKnee & trailing HipKnee should be 90 deg
            hipKnee_angle = self.calcAngle_2lines(lHipKnee, rHipKnee)

        # Visualize angles
            # cv2.putText(image, str(rKnee_angle), 
            #                tuple(np.multiply(right_knee, [frame_width, frame_height]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
            #                     )
        
            cv2.putText(image, str(hipKnee_angle), 
                           tuple(np.multiply(left_ankle, [frame_width, frame_height]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv2.LINE_AA
                                )
            
            # cv2.putText(image, str(back_angle), 
            #                tuple(np.multiply(right_hip, [frame_width, frame_height]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
            #                     )
            
        # Reps counter logic
            if (lKnee_angle < 100 and (abs(rKnee_trailing) > 160 or abs(rKnee_trailing) < 10) and back_angle > 75 and back_angle < 110) or (rKnee_angle < 100 and (abs(lKnee_trailing) > 160 or abs(lKnee_trailing) < 10) and back_angle > 75 and back_angle < 110 and hipKnee_angle > 90): #and knee_angle > 50 and knee_angle < 140:
                self.stage = "down"
            if (lKnee_angle > 160 and abs(rKnee_trailing) <= 160 and back_angle > 75 and back_angle < 110 and self.stage =='down') or (rKnee_angle > 160 and abs(lKnee_trailing) <= 160 and back_angle > 75 and back_angle < 110 and hipKnee_angle > 90 and self.stage =='down'):
                self.stage="up"
                self.reps +=1
                print(self.reps)
            if back_angle < 75 or back_angle > 110:
                self.hint = "Keep back straight"
            else:
                self.hint=""
        else:
            landmarks = None

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
        
        # Hints & Feedback
        cv2.putText(image, 'HINT:', (15,879), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, self.hint, 
                    (15,917), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0,255,0), 2, cv2.LINE_AA)
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )
        
    def visualize(self):
        if self.cap.isOpened() == False:
            print("Error opening video stream or file")
            raise TypeError
        
        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        
        outdir, inputflnm = self.filename[:sys.argv[1].rfind(
            '/')+1], sys.argv[1][sys.argv[1].rfind('/')+1:]
        inflnm, inflext = inputflnm.split('.')
        out_filename = f'{outdir}{inflnm}_annotated.{inflext}'

        out = cv2.VideoWriter(out_filename, cv2.VideoWriter_fourcc(
            'm', 'p', '4', 'v'), 30, (frame_width, frame_height))

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            #frame=cv2.flip(frame,1)
            image, results = self.recolor_RGB(frame)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            self.angle(results, image, frame_width, frame_height)
            out.write(image)

        self.cap.release()
        out.release()
        cv2.destroyAllWindows()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = Pushup(sys.argv[1], pose) 
cap.visualize()

