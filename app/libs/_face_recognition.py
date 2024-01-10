import face_recognition
import cv2
import os
from app.configs._app import APP_ENV
from pyinstrument import Profiler
import numpy as np

import psutil
memory_usage = psutil.virtual_memory().used
cpu_usage = psutil.cpu_percent()

def detect_face(image):
    # Monitor performce code of code
    if 'production' != APP_ENV:
        profiler = Profiler()
        profiler.start()

    image_file = os.path.abspath(image)
    image = face_recognition.load_image_file(image_file)

    # Detect face locations
    face_locations = face_recognition.face_locations(image)

    # Extract face landmarks (68 points for each face)
    face_landmarks_list = face_recognition.face_landmarks(image, face_locations)

    # Create a copy of the image to draw on
    image_with_landmarks = image.copy()

    # Iterate through each face and its landmarks
    for face_landmarks in face_landmarks_list:
        # Draw a line for each facial feature
        for facial_feature in face_landmarks.keys():
            for point in face_landmarks[facial_feature]:
                cv2.circle(image_with_landmarks, point, 2, (0, 255, 0), -1)  # Green points

    # Display the image with landmarks
    cv2.imshow("Image with Landmarks", image_with_landmarks)

    # Stop monitor performce code of code
    if 'development' == APP_ENV:
        profiler.stop()
        profiler.print()

        _memory_usage = psutil.virtual_memory().used
        _cpu_usage = psutil.cpu_percent()

        print(str(abs(memory_usage - _memory_usage)) + " Byte(s)")
        print(str(abs(cpu_usage - _cpu_usage)) + '%')

    # cv2.waitKey(0)