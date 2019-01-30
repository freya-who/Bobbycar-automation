# Bobbycar-automation
Bobbycar automation in python using YOLO on a Raspberry Pi 3 B+

The program is meant to run on a Raspberry Pi with a camera, mounted on a Bobbycar, to fully automate driving by following a detected object in the webcam image using YOLO.
The goal is to use one of the objects that is used in the pre-trained "Tiny YOLOv3" (see coco.names for the list), tape an image of that object on the back of a person and to then let the Bobbycar follow that person. A combination of two objects might be used to avoid accidental recognition.

The logic behind the project can later be applied to other automation tasks, e.g. steering a robotic arm automatically using a camera and Raspberry Pi.

# Sources
I used [YOLO](https://pjreddie.com/darknet/yolo/) with the pretrained model "Tiny YOLOv3" for this project.

[This tutorial](https://www.arunponnusamy.com/yolo-object-detection-opencv-python.html) got me started on running YOLO using python and opencv, which also goes over installing python (not necessary on Raspberry Pi, as the normal Raspbian has python installed by default), installing numpy and installing opencv.

[This](https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/) helped me to include threading, which didnt't increade fps, but made the image analysis real time. Before, there was an 8 second delay due to the buffer not being cleared.

I also used another tutorial to get me started on the webcam code, I will add the website later as I can't find it at the moment.

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


# Current status
At the moment the project reaches only roughly 1fps, however, using threading, this is at least real time and not delayed.

People and other objects are detected in the webcam video stream, however, no motors or servos are being controled using this information yet.

# To Do
* Decide on one or two objects to recognize, print out images to test detection
* Connect and control servos and motor on Bobbycar
* Make detection faster (5fps would be good)
