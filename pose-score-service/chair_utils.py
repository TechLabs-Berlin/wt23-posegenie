from body_parts import BodyPart, Person, Point, Rectangle, KeyPoint, person_from_keypoints_with_scores, Category
from movenet import Movenet
from preprocess import PoseEstimator,get_center_point,get_pose_size,normalize_pose_landmarks,landmarks_to_embedding,preprocess_data
from sklearn.model_selection import train_test_split
import csv
import tensorflow as tf
import pandas as pd
from typing import Dict, List
import os
from angle_calcs import Calculations
import mediapipe as mp
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
import scipy


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
plt.switch_backend('Agg')

class Chair():
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

        else:
            landmarks = None

        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(
                                      color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

    # Load the saved model
    model = tf.keras.models.load_model('model.h5', compile=False)

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

            # Make prediction with machine learning model
            estimator = PoseEstimator(detection_threshold=0.1)
            landmark_df = estimator.estimate(image)
            df = preprocess_data(landmark_df)
            prediction = self.model.predict(df)
            # get index of predicted class with highest probability
            pred_class = np.argmax(prediction)
            pred_class_prob = prediction[0][pred_class]
            print(pred_class_prob)

            # Draw prediction on image
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            thickness = 2
            color = (0, 255, 0)
            if pred_class_prob >= 0.98:
                # print predicted class
                text = f'Prediction: {pred_class}'
            else:
                text = 'Prediction is not confident enough'
            # text = f'Prediction: {pred_class}'
            org = (50, 50)
            image = cv2.putText(image, text, org, font,
                                fontScale, color, thickness, cv2.LINE_AA)

            self.angle(results, image)
            out.write(image)

        self.cap.release()
        out.release()
