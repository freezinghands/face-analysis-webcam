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


prototxt = 'model/deploy.prototxt'
model = 'model/res10_300x300_ssd_iter_140000.caffemodel'


def detect_face_local(image_path):
    start = time.time()
    image = cv2.imread(image_path)
    image = imutils.resize(image, width=400)
    net = cv2.dnn.readNetFromCaffe(prototxt, model)
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    appearance = 0
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            appearance += 1
    print(f"[detect_face_local] appearance: {appearance}")
    end = time.time()
    print(f"[detect_face_local] elapsed time: {end - start}")

print("--------1--------")
detect_face_local('capture/face-20220313-000128.jpg')
print()
print("--------2--------")
detect_face_local('capture/face-20220313-085222.jpg')
print()
print("--------3--------")
detect_face_local('capture/face-20220315-221250.jpg')
print()
