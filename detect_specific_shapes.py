# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 09:49:55 2019

@author: frefra
"""
# import the necessary packages
from rectanglesdetector import RectanglesDetector
import imutils
import cv2
from timeit import default_timer as timer

def on_mouse_click (event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONUP:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print("HSV Farbe")
        print(hsv[y,x])
        print("xy")
        print(y,x)

start = timer()
# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread("redblueNoise.jpg")
image = imutils.resize(image, width=1200)
resized = imutils.resize(image, width=1000)
ratio = image.shape[0] / float(resized.shape[0])

# denoising
#resized = cv2.fastNlMeansDenoisingColored(resized, None, 5, 5, 7, 21)

rd = RectanglesDetector()
#rd = RectanglesDetector(resized)

imageDet = rd.detectRectangles()

end = timer()
print(end - start)

# show the output image
cv2.imshow("Image", imageDet)

#cv2.setMouseCallback("Image", on_mouse_click, imageDet)
cv2.waitKey(0)