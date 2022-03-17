"""
import time
from dataManagerFaceapi import AzureFaceApi

f1 = AzureFaceApi()

v = f1.detect_face_src('capture/face-20220313-085222.jpg')

print(v)
"""








#this file is main-ubuntupc.py, but the contents is not.
#variables and modules should be instantiated by Smart Mirror UI Application's main.py.
import sys

#PIR motion sensor value
#raspberry pi's GPIO header must be imported as a python module to change this value
PIR = 0


#list of image file name which contain faces
face_file_list = []


#camera setup for ubuntu pc, maybe applicable for raspberry pi via usb
cap = cv2.VideoCapture(0)





class MirrorFaceDetect:
    def __init__(self):
        self.initTime = time.time()
    def detect_motion():
        self.stamp = time.time()
        if (cap.isOpened() == False):
            raise Exception("Unable to read camera source! Check if USB webcam is connected.  from " + sys.argv[0])
        while True:
            #check if motion sensor is on
            #module should update PIR variable
            #ex. PIR = 1 if GPIO.read(7) > 0 else 0
            if PIR == 0:
                time.sleep(1)
                continue
            if time.time() - self.stamp > 60:
                return {'exception': 'time exceeded'}
            #motion detected - capture image frame from camera src
            #capture the frame once
            ret, frame = cap.read()
            if ret == False:
                print("cannot capture image from camera source!")
                return {'exception': 'frame capture error'}
            
            detections = detectFaces(frame)
            self.appearance = 0
            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    self.appearance += 1
            #check whether face is detected or not
            if self.appearance > 0:
                #save 'frame' into file and call Face API and get emotion into Json format
                self.face_filename = "face-" + stamp + ".jpg"
    
    
    
    
#check if PIR sensor is on
while True:
    if PIR == 0:
        time.sleep(1)
        continue
    #motion detected - capture 
    


if __name__ == '__main__':
    main()


