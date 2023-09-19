import cv2 as cv
from cvzone.PoseModule import PoseDetector
import socket
import json
import numpy as np

CONTOURS_LANDMARKS = [
    # https://developers.google.com/mediapipe/solutions/vision/pose_landmarker/
    (7,8),
    (12,11),
    (12, 14),
    (14,16),
    (11, 13),
    (13, 15),
    (24, 23),
    (24, 26),
    (26, 28),
    (23, 25),
    (25, 27)
]

# Unity settings
unity_ip = '127.0.0.1'
unity_port = 25001
frame_counter = 0


# Create a socket for receiving button text from Unity
button_text_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
button_text_socket.bind(("127.0.0.1", 25002))
button_text_socket.listen(1)

# Accept a connection and receive the button text from Unity
button_text_connection, addr = button_text_socket.accept()
button_text = button_text_connection.recv(1024).decode()
button_text_connection.close()

# Create an array of landmarks from a csv file
def create_pose_arrays(path):
    arr = []

    with open(path, 'r') as file:
        for line in file:
            line_str = line.strip().split(',')  # Split the line using commas and remove leading/trailing whitespace
            line_str = line_str[:-1]
            poses = []

            for i in range(0, len(line_str) - 1, 4):
                poses.append([int(line_str[i]), int(line_str[i + 1]), int(line_str[i + 2]), int(line_str[i + 3])])

            arr.append(poses)

    return arr

# Both params are arrays of landmarks with same length
def compare_poses(landmarks1, landmarks2):
    print(f"land1: {landmarks1}")
    print(f"land2: {landmarks2}")
    distances = 0
    n_comparisons = 0

    for i in range(min(len(landmarks2), len(landmarks1))):

        for edge in CONTOURS_LANDMARKS:
            vector1 = (landmarks1[i][edge[0]][0] - landmarks1[i][edge[1]][0], landmarks1[i][edge[0]][1] - landmarks1[i][edge[1]][1])

            vector2 = (landmarks2[i][edge[0]][0] - landmarks2[i][edge[1]][0], landmarks2[i][edge[0]][1] - landmarks2[i][edge[1]][1])
            
            cos = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

            distances += cos

            n_comparisons += 1
    
    return np.round(float(distances / n_comparisons) * 10)

video = cv.VideoCapture(0)

detector = PoseDetector()
positionsList = []

# Espera até que o texto do botão seja recebido
while not button_text:
    pass

reference_landmarks = create_pose_arrays(f'Comparison files/{button_text}.txt')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((unity_ip, unity_port))

while True:
    frameExist, img = video.read()

    if not frameExist or frame_counter > len(reference_landmarks):
        break

    img = detector.findPose(img)
    landmarksList, boundingBox = detector.findPosition(img)

    # Compare the poses and get the comparison value
    comparison_value = compare_poses(landmarksList, reference_landmarks[frame_counter])
    frame_counter += 1

    # Send the comparison value to Unity
    try:
        # Create a dictionary to hold the comparison value
        data = {"comparisonValue": comparison_value}

        # Convert the data to a JSON string
        data_str = json.dumps(data)

        # Send the JSON data to Unity
        client_socket.sendall(data_str.encode())

        # Receive a response from Unity if needed
        response = client_socket.recv(1024)
        print("Received response:", response.decode())

    except Exception as e:
        print("Error:", e)

    #cv.imshow("Image", img)
    key = cv.waitKey(1)

# Close the socket connections
client_socket.close()
button_text_socket.close()
