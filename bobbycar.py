from detectSymbolRectangle import RectanglesDetector
from detectSymbolYOLO import SymbolDetectorYOLO
from bobbycarDriver import BobbycarDriver
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2 as cv
import numpy as np

# Initialize the parameters
C_STANDARDSIZE = 100

# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

winName = 'Object Detection'
cv.namedWindow(winName, cv.WINDOW_NORMAL)

symbolDetector = RectanglesDetector()
#symbolDetector = SymbolDetectorYOLO()

#bobbyDriver = BobbycarDriver()

# loop over some frames...this time using the threaded stream
while cv.waitKey(1) < 0:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
#    frame = imutils.resize(frame, width=400)
    
    symbolDetector.setImage(frame)
    symbolRec, symbolPos, symbolSize, frameDet = symbolDetector.detectSymbol()
    if symbolRec:
        print(symbolSize)
        print(symbolPos)
#        if symbolPos[0] < 300:
#            bobbyDriver.driveLeft(0.5)
#        else:
#            bobbyDriver.driveRight(0.5)
        
    # check to see if the frame should be displayed to our screen
    cv.imshow(winName, frameDet)
    
    # update the FPS counter
    fps.update()
 
# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
 
# do a bit of cleanup
cv.destroyAllWindows()
vs.stop()
