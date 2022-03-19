#inference via Face API (this code requests to server for only one time)
#reference: Microsoft Azure official documentation
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
import cv2

starttime = time.time()


apikeys = {}

with open(os.path.join('assets', 'keys', 'apikeys.txt'), 'rt') as keyFile:
    content = list(map(lambda x: x.split(','), keyFile.readlines()))
    for keyname, keycontent in content:
        apikeys[keyname.strip()] = keycontent.strip()


applicationSettings = {}
defaultApplicationSettings = {
    'faceApiEndpointName': 'my-endpoint'
}

with open('settings.txt', 'rt') as settingsFile:
    content = list(map(lambda x: x.split(','), settingsFile.readlines()))

    for name, value in defaultApplicationSettings.items():  # copy default settings
        applicationSettings[name] = value

    for name, value in content:  # read settings from settings file
        applicationSettings[name.strip()] = value.strip()



KEY = apikeys['azureface']
ENDPOINT = 'https://' + applicationSettings['faceApiEndpointName'] + '.cognitiveservices.azure.com/'

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


image_path = 'capture/face-20220315-221249.jpg'
#image_name = os.path.basename(image_url)
frame = cv2.imread(image_path)
ret, buf = cv2.imencode('.jpg', frame)
stream = io.BytesIO(buf)
#
#official way to import stream image:
#   test_image_array = glob.glob('test-image-person-group.jpg')
#   stream = open(test_image_array[0], 'r+b')
#
detected_faces = face_client.face.detect_with_stream(image=stream, return_face_attributes=["emotion", "qualityForRecognition"], recognition_model='recognition_04', detection_model='detection_01')
if not detected_faces:
    raise Exception('No face detected from image {}'.format(image_name))

print('whole raw data from ', image_path, ':')
for face in detected_faces:
    print (face)
"""     output by tutorial code snippet"""
"""
        {
            'additional_properties': {}, 
            'face_id': '8f073ad5-072d-4d2c-b3da-xxxxxa9820ca', 
            'recognition_model': None, 
            'face_rectangle': <azure.cognitiveservices.vision.face.models._models_py3.FaceRectangle object at 0x7f0a592a0fa0>, 
            'face_landmarks': None, 
            'face_attributes': None
        }
"""
"""output by adding optional parameters in detect_with_streams"""
"""this may cause additional fee in Face API"""
"""
        {
            'additional_properties': {}, 
            'face_id': 'd0c4ac94-a6ff-4506-896b-xxxxxdf47fb7', 
            'recognition_model': None, 
            'face_rectangle': <azure.cognitiveservices.vision.face.models._models_py3.FaceRectangle object at 0x7f878e8aefd0>,
            'face_landmarks': None, 
            'face_attributes': <azure.cognitiveservices.vision.face.models._models_py3.FaceAttributes object at 0x7f878e8d0340>
        }
"""
"""
        {
            'additional_properties': {}, 
            'face_id': '591ad3d2-a40c-4c3b-b52f-xxxxx53071b9', 
            'recognition_model': None, 
            'face_rectangle': <azure.cognitiveservices.vision.face.models._models_py3.FaceRectangle object at 0x7f543cd512e0>, 
            'face_landmarks': None, 
            'face_attributes': <azure.cognitiveservices.vision.face.models._models_py3.FaceAttributes object at 0x7f543cd51370>
        }
        ------ for this inference, elapsed time: 0.6972
"""

print('Detected face ID from', image_path, ':')
for face in detected_faces:
    print (face.face_id)
    #output
    #8f073ad5-072d-4d2c-b3da-xxxxxa9820ca
print()
image_face_ID = detected_faces[0].face_id
print(f"image_face_ID: {image_face_ID}")

print("----")
print(detected_faces[0].face_attributes.emotion)
print(detected_faces[0].face_attributes.quality_for_recognition)
print(str(detected_faces[0].face_attributes.quality_for_recognition))
qfr = str(detected_faces[0].face_attributes.quality_for_recognition).split('.')
print(qfr)
print("----")
"""
        outputs
"""
"""
        smiling Karina (face-20220313-000128.jpg)
        {
            'additional_properties': {}, 
            'anger': 0.0, 
            'contempt': 0.001, 
            'disgust': 0.0, 
            'fear': 0.0, 
            'happiness': 0.606, 
            'neutral': 0.393, 
            'sadness': 0.0, 
            'surprise': 0.0
        }
        ------ for this inference, elapsed time: 0.6091
"""
"""
        surprising IU (face-20220313-085222.jpg)
        {
            'additional_properties': {}, 
            'anger': 0.0, 
            'contempt': 0.0, 
            'disgust': 0.0, 
            'fear': 0.007, 
            'happiness': 0.0, 
            'neutral': 0.0, 
            'sadness': 0.0, 
            'surprise': 0.993
        }
        QualityForRecognition.high
        ------ for this inference, elapsed time: 0.4496
"""

endtime = time.time()
print(f"elapsed time: {endtime - starttime}")


