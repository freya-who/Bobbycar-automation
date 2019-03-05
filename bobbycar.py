from objectDetection.detectSymbolRectangle import RectanglesDetector
from objectDetection.detectSymbolYOLO import SymbolDetectorYOLO
from gpioSteering.bobbycarDriver import BobbycarDriver
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2 as cv
import numpy as np

# Initialize the parameters
C_STANDARDSIZE = 160
C_SHOWSCREEN = False
    

def on_mouse_click (event, x, y, flags, frame):
    if event == cv.EVENT_LBUTTONUP:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        print("HSV Farbe")
        print(hsv[y,x])
        print("xy")
        print(x,y)
        
## set camera white balance to fixed value
#camera = picamera.PiCamera()
#camera.awb_mode = 'off'
#camera.awb_gains = 8,5
#camera.close()

def run_object_detection_loop(bobbyDriver):
    # created a *threaded* video stream, allow the camera sensor to warmup,
    # and start the FPS counter
    print("[INFO] sampling THREADED frames from webcam...")
    vs = WebcamVideoStream(src=0).start()
    fps = FPS().start()

    width = vs.stream.get(cv.CAP_PROP_FRAME_WIDTH)
    height = vs.stream.get(cv.CAP_PROP_FRAME_HEIGHT)

    if C_SHOWSCREEN:
        winName = 'Object Detection'
        cv.namedWindow(winName, cv.WINDOW_NORMAL)
        #cv.resizeWindow(winName, (int(width/2),int(height/2)))
        cv.resizeWindow(winName, (int(width),int(height)))

    symbolDetector = RectanglesDetector()
    #symbolDetector = SymbolDetectorYOLO()

    # loop over some frames...this time using the threaded stream
    while cv.waitKey(1) < 0:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        frame = vs.read()
    #    frame = imutils.resize(frame, width=400)
    #    g = camera.awb_gains
    #    print(g)
        symbolDetector.setImage(frame)
        symbolRec, symbolPos, symbolSize, frameDet = symbolDetector.detectSymbol()
        if symbolRec:
            print(symbolSize)
            print(symbolPos)
            symbolDetector.symbolRecognized = False
            if symbolPos[0] < width/2 - 100:
                steerAmount = 1 - (symbolPos[0] / (width/2 - 100))
                bobbyDriver.driveRight(steerAmount)
            elif symbolPos[0] > width/2 + 100:
                steerAmount = (symbolPos[0] - (width/2 + 100)) / (width - (width/2 + 100))
                bobbyDriver.driveLeft(steerAmount)
            else:
                bobbyDriver.driveStraight()
            
            if symbolSize <= C_STANDARDSIZE:
                bobbyDriver.accelerate()
            else:
                bobbyDriver.stop()
        else:
            bobbyDriver.stop()
            
        # displayed the frame with the object detection
        if C_SHOWSCREEN:
            cv.imshow(winName, frameDet)
            cv.setMouseCallback(winName, on_mouse_click, frameDet)
        
        if bobbyDriver.stopYet():
            print('Button Pressed again (off)')
            break
        
        # update the FPS counter
        fps.update()
     
    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
     
    # do a bit of cleanup
    if C_SHOWSCREEN:
        cv.destroyAllWindows()
    vs.stop()

# start the gpio control class
bobbyDriver = BobbycarDriver()

try:
    while True:
        if bobbyDriver.startYet():
            print('Button Pressed')
            run_object_detection_loop(bobbyDriver)
except KeyboardInterrupt:
    bobbyDriver.cleanup()
