import mediapipe as mp
import sys
from src.curls_utils import Curls
from src.read_upload import readUpload

##############################
# HOW TO RUN: python curl_PoseDetection.py <filename>
##############################

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = Curls(readUpload, sys.argv[1], pose) 

cap.visualize()