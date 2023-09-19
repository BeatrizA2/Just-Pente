import os
import cv2 as cv
from cvzone.PoseModule import PoseDetector
import numpy as np


def createFile(filepath, positionsList):
    with open(filepath, 'w') as f:
        f.writelines(["%s\n" % item for item in positionsList])

# Path to the directory containing video files
videos_folder = 'Videos/'

# List all files in the folder
video_files = [f for f in os.listdir(videos_folder) if f.endswith('.mp4')]

detector = PoseDetector()

# Create the "Positions files" folder if it doesn't exist
positions_folder = 'Positions files'
os.makedirs(positions_folder, exist_ok=True)

# Create the "Comparison files" folder if it doesn't exist
comparison_folder = 'Comparison files'
os.makedirs(comparison_folder, exist_ok=True)

for video_file in video_files:
    video_path = os.path.join(videos_folder, video_file)
    video = cv.VideoCapture(video_path)

    positionsList = []
    comparisonList = []

    while True:
        frameExist, img = video.read()

        if not frameExist:
            positions_filename = os.path.splitext(video_file)[0] + ".txt"

            positions_filepath = os.path.join(positions_folder, positions_filename)
            comparison_filepath = os.path.join(comparison_folder, positions_filename)

            createFile(positions_filepath, positionsList)
            createFile(comparison_filepath, comparisonList)
            break

        img = detector.findPose(img)
        landmarksList, boundingBox = detector.findPosition(img)

        # Verify if a person was detected
        if boundingBox:
            landmarkStr = ''
            lmStr = ''
            for lm in landmarksList:
                landmarkStr += f'{lm[1]},{img.shape[0] - lm[2]},{lm[3]},'
                lmStr += f'{lm[0]},{lm[1]},{lm[2]},{lm[3]},'


            positionsList.append(landmarkStr)
            comparisonList.append(lmStr)


        cv.imshow("Image", img)
        key = cv.waitKey(1)

        if key == ord('s'):
            positions_filename = os.path.splitext(video_file)[0] + ".txt"

            positions_filepath = os.path.join(positions_folder, positions_filename)
            comparison_filepath = os.path.join(comparison_folder, positions_filename)

            createFile(positions_filepath, positionsList)
            createFile(comparison_filepath, comparisonList)

    video.release()

cv.destroyAllWindows()
