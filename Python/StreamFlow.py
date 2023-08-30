import cv2 as cv
from cvzone.PoseModule import PoseDetector
import socket
import json

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
