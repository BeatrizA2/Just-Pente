import cv2 as cv
from cvzone.PoseModule import PoseDetector
import numpy as np


webcam = cv.VideoCapture(0)


detector = PoseDetector()

def create_pose_arrays(path):
    arr = []

    with open(path, 'r') as file:
        for line in file:
            line_str = line.strip().split(',')  # Split the line using commas and remove leading/trailing whitespace
            line_str = line_str[:-1]
            poses = []

            for i in range(0, len(line_str) - 1, 3):
                poses.append([int(line_str[i]), int(line_str[i + 1]), int(line_str[i + 2])])

            arr.append(poses)

    return arr

def calculate_pose_similarity(pose1, pose2):
    # Assuming pose1 and pose2 are arrays of keypoints
    total_distance = 0

    for i in range(len(pose1)):
        total_distance += euclidean_distance_3d(pose1[i], pose2[i])

    similarity_score = 1 / (1 + total_distance)  # Inverse of the distance
    return similarity_score

def euclidean_distance_3d(p1, p2):
    return np.sqrt((p1[1] - p2[0])**2 + (p1[2] - p2[1])**2 + (p1[3] - p2[2])**2)


dance = input('Type the name of the music you would like to dance to:')

video = cv.VideoCapture(f'Videos/{dance}.mp4')


video_poses_arr = create_pose_arrays(f'Comparison files/{dance}.txt')
counter = 0

while True:
    if counter > len(video_poses_arr):
        break

    frameExist, img = webcam.read()
    videoFrameExist, video_frame = video.read()

    if not frameExist or not videoFrameExist:
        break

    img = detector.findPose(img)
    img = cv.resize(img, (300, 300))
    video_frame = cv.resize(video_frame, (300, 300))
    landmarksList, boundingBox = detector.findPosition(img)


    #Verify if a person was detected
    if boundingBox:
        score = calculate_pose_similarity(landmarksList, video_poses_arr[counter])
        cv.putText(video_frame, str(score)[0], (50, 100), cv.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)



    #cv.imshow("Image", img)

    combined_frame = np.hstack((img, video_frame))

    # Display combined frames
    cv.imshow('Combined Feed', combined_frame)
    key = cv.waitKey(1)
    counter += 1

