# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 09:24:04 2019

@author: frefra
"""

import cv2
import numpy as np
import imutils

# dedine constants
C_LOWERLIMITBLUE = np.array([100,90,90])
C_UPPERLIMITBLUE = np.array([125,255,225])

C_LOWERLIMITRED1 = np.array([0,90,90])
C_UPPERLIMITRED1 = np.array([10,255,225])

C_LOWERLIMITRED2 = np.array([165,90,90])
C_UPPERLIMITRED2 = np.array([179,255,225])

C_MINWIDTH = 30
C_MINHEIGHT = 30


class RectangleShape:
    def __init__(self, contour, cX, cY, width, height):
        self.contour = contour
        self.cX = cX
        self.cY = cY
        self.width = width
        self.height = height
        self.upperLimit = cY + height//2
        self.lowerLimit = cY - height//2

class RectanglesDetector:
    def __init__(self, image = np.array([])):
        
        # define names corresponding to number of lines for a shape
        self.shapeNames = ['unidentified', 'line', 'two lines', 'triangle', 'rectangle', 'pentagon', 'circle']
        
        self.symbolRecognized = False        
        self.symbolCenter = [0,0]        
        self.symbolHeight = 0
        
        if image.size != 0:
            self.image = image
            self.hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            self.redImage = self.getRedImage()
            self.blueImage = self.getBlueImage()
        else:
            self.image = np.array([])
            self.hsvImage = np.array([])
            self.redImage = np.array([])
            self.blueImage = np.array([])
    
    def setImage(self, image):
        self.image = image
        self.hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        self.blueImage = self.getRedImage()
        self.redImage = self.getBlueImage()
        
    def detectSymbol(self):
        
        if self.image.size != 0:
            # find rectangles in redImage and collect bounding boxes and centers
            cnts = cv2.findContours(self.redImage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            
            # loop over the red contours and collect red rectangles
            redRectangles = []
            for c in cnts:
                # compute the center of the contour, then detect the name of the
                # shape using only the contour
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cX = int((M["m10"] / M["m00"]))
                    cY = int((M["m01"] / M["m00"]))
                else:
                    if len(c) == 1:
                        cX, cY = c[0][0]
                    else:
                        cX, cY = 0, 0
            
                shapeNumberLines, w, h = self.detectShape(c)
                
                # if shape is rectangle (4) or pentageon (5), store in list for red rectangles
                if ( 4 <= shapeNumberLines < 6 ) and (w>C_MINWIDTH) and (h>C_MINHEIGHT):
                    cv2.drawContours(self.image, [c], -1, (0, 0, 255), 2)
                    cv2.putText(self.image, self.shapeNames[shapeNumberLines], (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    #                cv2.putText(self.image, str(cX)+', '+str(cY), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    redRectangles.append(RectangleShape(c,cX,cY,w,h))
                    
                    
            # find rectangles in blueImage and collect bounding boxes and centers
            cntsBlue = cv2.findContours(self.blueImage.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cntsBlue = imutils.grab_contours(cntsBlue)
            
            # loop over the blue contours
            for cBlue in cntsBlue:
                # compute the center of the contour, then detect the name of the
                # shape using only the contour
                M = cv2.moments(cBlue)
                if M["m00"] != 0:
                    cX = int((M["m10"] / M["m00"]))
                    cY = int((M["m01"] / M["m00"]))
                else:
                    if len(cBlue) == 1:
                        cX, cY = cBlue[0][0]
                    else:
                        cX, cY = 0, 0
                
                shapeNumberLines, w, h = self.detectShape(cBlue)
                
                # if shape is rectangle, check if red rectangle above
                if ( 4 <= shapeNumberLines < 6 ) and (w>C_MINWIDTH) and (h>C_MINHEIGHT):
                    cv2.drawContours(self.image, [cBlue], -1, (255, 0, 0), 2)
                    cv2.putText(self.image, self.shapeNames[shapeNumberLines], (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    #                cv2.putText(self.image, str(cX)+', '+str(cY), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    blueLowerLimit = cY-h//2
                    for rr in redRectangles:
                        # is above or below?
                        if (rr.cX <= cX+30) and (rr.cX >= cX-30):
                            # is directly above?
                            if (rr.upperLimit >= blueLowerLimit-30) and (rr.upperLimit <= blueLowerLimit+30):
                                # rr roughly above blue rectangle
                                # draw contour around both
                                cv2.drawContours(self.image, [cBlue], -1, (0, 255, 0), 2)
                                cv2.drawContours(self.image, [rr.contour], -1, (0, 255, 0), 2)
                                (xb,yb,wb,hb) = cv2.boundingRect(np.concatenate((cBlue,rr.contour), axis=0))
                                self.symbolCenter = [xb+wb//2, yb+hb//2]
                                self.symbolHeight = hb
                                cv2.rectangle(self.image,(xb,yb),(xb+wb,yb+hb),(255,255,255),2)
                                self.symbolRecognized = True
            
            return self.symbolRecognized, self.symbolCenter, self.symbolHeight, self.image
        else:
            print('No image set, set image in constructor or using setImage method')
            # still return image? to prevent further errors (imshow trying to display missing image)
            return np.array([0,0]).astype(np.uint8)
        
    def detectShape(self, c):
        # initialize the shape name and approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        
        shapeNumberLines = len(approx)
        (x, y, w, h) = cv2.boundingRect(approx)

        return shapeNumberLines, w, h

    def getRedImage(self):
        # red wraps around H = 180 (H = 0...180, S, V = 0...255)
        mask = cv2.inRange(self.hsvImage, C_LOWERLIMITRED1, C_UPPERLIMITRED1) | cv2.inRange(self.hsvImage, C_LOWERLIMITRED2, C_UPPERLIMITRED2)
#        res = cv2.bitwise_and(self.image,self.image, mask= mask)
#        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(mask, (17, 17), 0)
        redImg = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

        return redImg

    def getBlueImage(self):
        mask = cv2.inRange(self.hsvImage, C_LOWERLIMITBLUE, C_UPPERLIMITBLUE)
#        res = cv2.bitwise_and(self.image,self.image, mask= mask)
#        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(mask, (17, 17), 0)
        blueImg = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
        
        return blueImg
    
    

    
    
    
    