# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 14:09:29 2019

@author: frefra
"""
# import the necessary packages
from detectSymbolRectangle import RectanglesDetector
from detectSymbolYOLO import SymbolDetectorYOLO
from bobbycarDriver import BobbycarDriver
import imutils
import cv2
import glob
from time import sleep

C_STANDARDSIZE = 100

#todo: fuzzy logic line follower seperate class? or function?
#todo: handle case that more than one symbol returned

def on_mouse_click (event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONUP:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print("HSV Farbe")
        print(hsv[x,y])
        print("xy")
        print(x,x)

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
frameList = []
imageFiles = glob.glob('D:/OneDrive - Dentsply Sirona/Python Skripte/alle/bc/images/*.jpg')
for imageFile in imageFiles:
    frameList.append(cv2.imread(imageFile))

rd = RectanglesDetector()
bobbyDriver = BobbycarDriver()

# for frame loop
for frame in frameList:
#    resized = imutils.resize(image, width=1000)
    #resized = cv2.fastNlMeansDenoisingColored(resized, None, 5, 5, 7, 21) #denoising SLOW!
#    ratio = image.shape[0] / float(resized.shape[0])
    rd.setImage(frame)
    symbolRec, symbolPos, symbolSize, imageDet = rd.detectRectangles()
    if symbolRec:
        print(symbolSize)
        print(symbolPos)
    cv2.imshow("Image", imageDet)
    cv2.setMouseCallback("Image", on_mouse_click, imageDet)
    cv2.waitKey(1000)
    
cv2.waitKey(0)
