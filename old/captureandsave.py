#keep capturing by 1 second until keyboard interrupt
#webcam must be connected to the host device
#refernce: https://steki.tistory.com/75
#refernce: https://colab.research.google.com/drive/1JDmzw0D7etsH3kCAmNIYOfIRvJU1N8qO?usp=sharing#scrollTo=UZp-xlhYI1SL
import requests
import sys
import os
import cv2
import time
import datetime
import numpy as np
import imutils

#os.system('python3 user_input.py')
#os.popen('python3 delay.py')
#starttime = time.time()

prototxt = 'model/deploy.prototxt'
model = 'model/res10_300x300_ssd_iter_140000.caffemodel'

cap = cv2.VideoCapture(0)
if (cap.isOpened() == False):
    print("Unable to read camera source!")

while True:
    starttime = time.time()
    ret, frame = cap.read()
    if ret == False:
        print("cannot capture image from camera source!")
        break
    cv2.imshow('frame',frame) # for debugging
    tm = datetime.datetime.now()
    stamp = f"{tm:%Y%m%d-%H%M%S}"
    #cv2.imshow('frame', frame)
    net = cv2.dnn.readNetFromCaffe(prototxt, model)
    image = imutils.resize(frame, width=400)
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    appearance = 0
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            appearance += 1
    print(f"appearance: {appearance}")
    endtime = time.time()
    print(f"elapsed time: {endtime - starttime}")
    if appearance > 0:
        cv2.imwrite("capture/face-" + stamp + ".jpg", frame)
        print("Detection completed at " + stamp + ", file successfully saved as capture/face-" + stamp + ".jpg")

cap.release()
cv2.destroyAllWindows()
print("Exiting program...")





# face api connection
