import cv2
import pickle
import cvzone
import numpy as np

cap = cv2.VideoCapture('Carpark.mp4')

with open('ROI', 'rb') as f:
    poslist = pickle.load(f)

width, height = 69, 29  

def checkparkspace(imgprocessed, image):
    carCounter = 0

    for pos in poslist:
        x, y = pos
        imgcrop = imgprocessed[y:y+height, x:x+width]
        count = cv2.countNonZero(imgcrop)

        cvzone.putTextRect(image, str(count), (x, y+height-5),
                           scale=1, thickness=2, offset=2, colorR=(0,0,0))

        if count < 450:  
            color = (0, 255, 0)  
            thickness = 4
        else:
            color = (0, 0, 255) 
            thickness = 2
            carCounter += 1

        cv2.rectangle(image, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(image, f'Cars: {carCounter}/{len(poslist)}',
                       (50, 50), scale=2, thickness=3, offset=10, colorR=(0, 200, 0))

while True:
    success, image = cap.read()

    if not success:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    imgGray = clahe.apply(imgGray)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(
        imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 25, 16
    )
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkparkspace(imgDilate, image)

    
    cv2.imshow("Parking Lot", image)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
