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
import json




#---------------------------------------------------
# this part is for local face detection
# function 'detect_faces' perform DNN with 
import cv2
import imutils
#DNN model source path which will be used in cv2.dnn
prototxt = 'model/deploy.prototxt'
model = 'model/res10_300x300_ssd_iter_140000.caffemodel'

def detect_faces(frame):
	net = cv2.dnn.readNetFromCaffe(prototxt, model) # does it need outside of this function? please help me out..

	image = imutils.resize(frame, width=400)
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    return detections
#---------------------------------------------------







#PIR motion sensor value
#raspberry pi's GPIO header must be imported as a python module to change this value
PIR = 0


#list of image file name which contain faces
face_file_list = []


#camera setup for ubuntu pc, maybe applicable for raspberry pi via usb
cap = cv2.VideoCapture(0)










class MirrorFaceDetect:
    def __init__(self):
        self.face_api = AzureFaceApi()
    def detect_motion():
        # initialize variable in Json format, to return exception string
        j = json.loads('{}')
        
        # mark time stamp to save energy
        # camera running time does not exceed 60 seconds
        self.stamp = time.time()
        
        # check if camera(usb webcam) is connected
        if (cap.isOpened() == False):
            raise Exception("Unable to read camera source! Check if USB webcam is connected.  from " + sys.argv[0])
        while True:
            # check if motion sensor is on
            # if motion sensor is off, wait until motion sensor is on
            # module should update PIR variable
            # FOR EXAMPLE) 
            # PIR = 1 if GPIO.read(7) > 0 else 0
            if PIR == 0:
                time.sleep(1)
                continue
            if time.time() - self.stamp > 60:
                msg = {'exception': 'time exceeded'}
                j.update(msg)
                return j
            #motion detected - capture image frame from camera src
            #capture the frame once
            ret, frame = cap.read()
            if ret == False:
                print("cannot capture image from camera source!")
                msg = {'exception': 'frame capture error'}
                j.update(msg)
                return j
            
            # Do the actions if motion sensor is on
            detections = detect_faces(frame)
            self.appearance = 0
            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    self.appearance += 1
            
            #check whether face is detected or not
            if self.appearance <= 0:
                print("No face found on camera source.")
                continue
            
            #save 'frame' image into Jpeg file 
            self.face_filename = "face-" + stamp + ".jpg"
            cv2.imwrite("capture/" + self.face_filename, frame)
            
            #Calling Face API and get emotion value in Json Format
            return self.face_api.detect_face_src('capture/' + self.face_filename)
    
    
    
    
#check if PIR sensor is on
while True:
    if PIR == 0:
        time.sleep(1)
        continue
    #motion detected - capture 
    


if __name__ == '__main__':
    main()






