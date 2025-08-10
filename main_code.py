import cv2
import pickle
import cvzone
import numpy as np

with open('ROI_picker','rb') as f:
         poslist = pickle.load(f)

width , height = 69 , 29

def checkparkspace(imgprocessed):
         
         #spaceCounter = 0
         carCounter = 0

         for pos in poslist:
            x, y = pos

            imgcrop = imgprocessed[y:y+height,x:x+width]
            #cv2.imshow(str(x*y),imgcrop)
            count = cv2.countNonZero(imgcrop)
            cvzone.putTextRect(image,str(count),(x,y+height-3),scale = 1, thickness=2, offset=0)

            if count < 330:
                   color = (0,255,0)
                   thickness = 4
                   #spaceCounter +=1
            
            else:
                   color = (0,0,255)
                   thickness = 2
                   carCounter +=1

            cv2.rectangle(image,pos,(pos[0] + width, pos[1] + height),color,thickness)
        
         cvzone.putTextRect(image,f'Cars: {carCounter}/{len(poslist)}',(60, 30),scale = 2, thickness=3, offset=20, colorR=(0,200,0))


while True:
        image = cv2.imread('before img.png')
        
        imgGray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY_INV,25,16)
        #cv2.imshow("Threshold",imgThreshold)
        imgMedian = cv2.medianBlur(imgThreshold,5)

        kernel = np.ones((3,3), np.int8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        checkparkspace(imgDilate)

        cv2.imshow("Image",image)
        cv2.waitKey(1)
