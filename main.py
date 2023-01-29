import cv2
import numpy as np
import cvzone
import pickle



cap= cv2.VideoCapture('CarPark.mp4')

# loading the carparkpos as its already created
with open('carparkpos', 'rb') as f:
    poslist = pickle.load(f)
width, height = (157-50),(240-192)

def checkParkingSpace(imgPro):
    spaceCounter = 0
    for pos in poslist:

        x, y = pos
        # cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)
        cv2.imshow('Image', img)

        imgCrop = imgPro[y:y + height, x:x + width]
        cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y + height - 2), scale=1, thickness=2, offset=0, colorR=(0, 0, 255))
        if count < 500:
            color = (0, 255, 0)  # BGR
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    cvzone.putTextRect(img, f'FREE{str(spaceCounter)}/{len(poslist)}', (450, 50), scale=2, thickness=5, offset=20,colorR=(0, 200, 0))




while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # the whole statement was used to repeat the video again and again
    success, img = cap.read()

    # we will convert video to gray with following command
    imgGray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)

    # we use threshold method to find the edges as if the car is parked threre will me many edges if not there are quite less edges
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 25, 16) #255 is the maximum color limit, cv2.ADAPTIVE_THRESH_GAUSSIAN_C for edge detection, cv2.THRESH_BINARY_INV, 25, 16 block size
    imgMedium = cv2.medianBlur(imgThreshold,5)

    # we add dilation to make the image thicker.
    kernel = np.zeros((3,3), np.uint8) # defining the int
    imgDilate = cv2.dilate(imgMedium,kernel, iterations=1) # we can increase the thickness by increasing the iterations

    checkParkingSpace(imgDilate)
    for pos in poslist:  # since we have already marlked the spaces with rectanle will iterate through the same on video poslist is storing coorniates already
        x,y = pos




    cv2.imshow('video', img)
    # cv2.imshow('ImageBlur', imgBlur)
    # cv2.imshow('Threshold', imgThreshold)
    # cv2.imshow('ImageMedian', imgMedium)
    # cv2.imshow('ImageDilate', imgDilate)
    cv2.waitKey(1)
