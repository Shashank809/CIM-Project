import cv2
import pickle

width , height = 69 , 29

try:
      with open('ROI_picker','rb') as f:
         poslist = pickle.load(f)
except:
         poslist = []

def mouseClick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        poslist.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(poslist):
             x1, y1 = pos
             if x1 < x < x1 + width and y1 < y < y1 + height:
                  poslist.pop(i)

    with open('ROI_picker','wb') as f:
         pickle.dump(poslist, f)


while True:

    image = cv2.imread('before img.png')


    for pos in poslist:
            cv2.rectangle(image,pos,(pos[0] + width, pos[1] + height),(255,0,255),2)

      
    cv2.imshow("Image",image)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)