import cv2 as cv
from cvzone.PoseModule import PoseDetector
import socket
import json

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

# Create a socket connection to Unity
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((unity_ip, unity_port))

def send_positions_to_unity(positions):
    try:
        # Convert the positions to a JSON string
        data = json.dumps(positions)

        # Send the data to Unity
        client_socket.sendall(data.encode())

        # Receive a response from Unity if needed
        response = client_socket.recv(1024)
        print("Received response:", response.decode())


    except Exception as e:
        print("Error:", e)



video = cv.VideoCapture(0)

detector = PoseDetector()
positionsList = []


while True:
    frameExist, img = video.read()

    if not frameExist:
        break

    img = detector.findPose(img)
    landmarksList, boundingBox = detector.findPosition(img)
    lmStr = ''

    for lm in landmarksList:
        lmStr += f'{lm[1]},{img.shape[0] - lm[2]},{lm[3]},'

    send_positions_to_unity(lmStr)


    cv.imshow("Image", img)
    key = cv.waitKey(1)

# Close the socket connection
client_socket.close()

# Create an array of landmarks from a csv file
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

# Both params are arrays of landmarks with same length
def compare_poses(landmarks1, landmarks2):
    distances = 0
    n_comparisons = 0

    for i in range(min(len(landmarks2), len(landmarks1))):

        for edge in CONTOURS_LANDMARKS:
            vector1 = (landmarks1[i][edge[0]][0] - landmarks1[i][edge[1]][0], landmarks1[i][edge[0]][1] - landmarks1[i][edge[1]][1])

            vector2 = (landmarks2[i][edge[0]][0] - landmarks2[i][edge[1]][0], landmarks2[i][edge[0]][1] - landmarks2[i][edge[1]][1])
            
            cos = np.dot(vector1, webcam) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))

            distances += cos

            n_comparisons += 1
    
    return np.round(float(distances / n_comparisons)) * 10
