# Bobbycar-automation
Bobbycar automation in python using YOLO on a Raspberry Pi 3 B+

The program is meant to run on a Raspberry Pi with a camera, mounted on a Bobbycar, to fully automate driving by following a detected object in the webcam image using YOLO.
The goal is to use one of the objects that is used in the pre-trained "Tiny YOLOv3" (see coco.names for the list), tape an image of that object on the back of a person and to then let the Bobbycar follow that person. A combination of two objects might be used to avoid accidental recognition.

The logic behind the project can later be applied to other automation tasks, e.g. steering a robotic arm automatically using a camera and Raspberry Pi.

The file `webcamObjectDetection.py` is an object detector for a camera stream.

The file `bobbycar.py` is the main script that calls the specific object detection and the steering with GPIOS.

`bobbycarDriver.py` controls the GPIOS using pigpio.

`detectSymbolYOLO.py` is the object detector using YOLO.

`detectSymbolRectangle.py` is the object detector using rectangles, it detects if there is a (printout of a) red rectangle on top of a blue rectangle somewhere in the frame.
This is the currently used method as it is significantly faster than YOLO (5-6fps vs. <1fps).

You can switch betweem them by using either:
```
symbolDetector = RectanglesDetector()
```
or 
```
symbolDetector = SymbolDetectorYOLO()
```
in `bobbycar.py`.



# Sources
I used [YOLO](https://pjreddie.com/darknet/yolo/) with the pretrained model "Tiny YOLOv3" for this project.

[This tutorial](https://www.arunponnusamy.com/yolo-object-detection-opencv-python.html) got me started on running YOLO using python and opencv, which also goes over installing python (not necessary on Raspberry Pi, as the normal Raspbian has python installed by default), installing numpy and installing opencv.

[This](https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/) helped me to include threading, which didnt't increade fps, but made the image analysis real time. Before, there was an 8 second delay due to the buffer not being cleared.

I also used another tutorial to get me started on the webcam code, I will add the website later as I can't find it at the moment.

[This tutorial](https://www.pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/) was used to try and get a speed increase on the Pi.


# Installation
The aforementioned [tutorial](https://www.arunponnusamy.com/yolo-object-detection-opencv-python.html) descibes how to install the necessary dependencies.

To install opencv on the Raspberry however, a few more packages need to be installed, here are the instructions needed to install opencv on the Raspberry Pi:

```
pip install opencv-python
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4
sudo apt-get install python3-pyqt5
sudo apt-get install libqt4-test

```

If upon (re)start the camera module doesn't work (nothing found with `ls /dev/video*
`), you have to run:
```
sudo modprobe bcm2835-v4l2
```

To start the pigpio service to control the servos run 
```
sudo pigpiod
```


# Current status

For now I have switched to a simpler Rectangle Detector, so the Bobbycar will be following a printout of a red rectangle above a blue rectangle.

I also tried circle detection using Hugh transformation but finding the right parameters is tricky and so dependent on the surroundings that it isn't a feasible approach in this case.

<s>At the moment the project reaches only roughly 1fps with YOLO, however, using threading, this is at least roughly real time and not delayed. Before threading, the delay was about 8 seconds.

I tried to increase the speed by compiling opencv myself with ARM NEON and VFPV3 options enabled (see `Sources` for tutorial), but it seems opencv 4.0.0 is already compiled with those options, because there was no increase in FPS.</s>


# To Do
* Fix white balance in pi camera to reliably detect blue and red rectangles
* Speed control depending on size of object in frame
* Connect servos and motor on Bobbycar
* Figure out logistics: make the script start when button is pressed (no screen during normal usage), implement a logger, make `sudo modprobe bcm2835-v4l2` and `sudo pigpiod` run when button is pressed, before script is started, disable all `imshow` functionality
* Make YOLO detection faster (5fps would be good) - HOW?
* Maybe to improve ease-of-use use circle detection (not using Hugh Transform though, that is a massive pain to get the parameters right...) and paint some spheres red and blue, relatively small, put them on a keychain and carry those around. Probably easier than keeping a printout of rectangles taped to your back...
