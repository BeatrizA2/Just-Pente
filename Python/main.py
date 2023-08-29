import cv2 as cv
from cvzone.PoseModule import PoseDetector

def createFile(positionsList):
    with open("Positions.txt", 'w') as f:
        f.writelines(["%s\n" % item for item in positionsList])


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