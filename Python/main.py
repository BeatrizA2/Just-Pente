import cv2 as cv
from cvzone.PoseModule import PoseDetector
import numpy as np

def createFile(positionsList):
    with open("Positions.txt", 'w') as f:
        f.writelines(["%s\n" % item for item in positionsList])

def extractPoses():
    video = cv.VideoCapture('Videos/cupid.mp4')

    detector = PoseDetector()
    positionsList = []

    while True:
        frameExist, img = video.read()

        if not frameExist:
            createFile(positionsList)
            break

        img = detector.findPose(img)
        landmarksList, boundingBox = detector.findPosition(img)

        #Verify if a person was detected
        if boundingBox:
            landmarkStr = ''
            for lm in landmarksList:
                landmarkStr += f'{lm[1]},{img.shape[0] - lm[2]},{lm[3]},'

            positionsList.append(landmarkStr)


        cv.imshow("Image", img)
        key = cv.waitKey(1)

        if key == ord('s'):
            createFile(positionsList)

def compare_pose_arrays(poses_file, webcam_poses):
    total_similarity = 0

    with open(poses_file, 'r') as file:
        itr = 0

        for line in file:
            line_str = line.strip().split(',')  # Split the line using commas and remove leading/trailing whitespace
            line_str = line_str[:-1]
            poses = []

            for i in range(0, len(line_str) - 1, 2):
                poses.append((float(line_str[i]), float(line_str[i + 1])))

            if (len(poses) == len(webcam_poses[itr])):
                total_similarity += calculate_pose_similarity(poses, webcam_poses[itr])

            itr += 1

    average_similarity = total_similarity / len(webcam_poses)
    return average_similarity

def calculate_pose_similarity(pose1, pose2):
    # Assuming pose1 and pose2 are arrays of keypoints
    total_distance = 0

    for i in range(len(pose1)):
        total_distance += euclidean_distance(pose1[i], pose2[i])

    similarity_score = 1 / (1 + total_distance)  # Inverse of the distance
    return similarity_score

def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def create_pose_arrays(path):
    arr = []

    with open(path, 'r') as file:
        for line in file:
            line_str = line.strip().split(',')  # Split the line using commas and remove leading/trailing whitespace
            line_str = line_str[:-1]
            poses = []

            for i in range(0, len(line_str) - 1, 2):
                poses.append((int(line_str[i]), int(line_str[i + 1])))

            arr.append(poses)

    return arr

print(compare_pose_arrays("Positions.txt", create_pose_arrays("Positions.txt")))