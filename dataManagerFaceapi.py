import os
import requests
import json

import asyncio
import io
import glob
import sys
import time
import uuid
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
import cv2


# Reading required apikeys
#
# Note:
#   API keys is at file named 'assets/keys/apikeys.txt'
#   Make your own CSV file for API keys or just manually generate the 'apikeys' dictionary
#
# Included Keys:
#   - openweathermap
#   - azureface

apikeys = {}

with open(os.path.join('assets', 'keys', 'apikeys.txt'), 'rt') as keyFile:
    content = list(map(lambda x: x.split(','), keyFile.readlines()))
    for keyname, keycontent in content:
        apikeys[keyname.strip()] = keycontent.strip()


# Reading settings file
#
# Note:
#   Read UI application settings from settings.txt

applicationSettings = {}
defaultApplicationSettings = {
    'lat': '37.56779',  # latitude of Seoul, Korea
    'lon': '126.97765',  # longitude of Seoul, Korea
    'faceApiEndpointName': 'my-endpoint', 
}

with open('settings.txt', 'rt') as settingsFile:
    content = list(map(lambda x: x.split(','), settingsFile.readlines()))

    for name, value in defaultApplicationSettings.items():  # copy default settings
        applicationSettings[name] = value

    for name, value in content:  # read settings from settings file
        applicationSettings[name.strip()] = value.strip()


# Azure Face API
#
# Note:
#   Module for inferencing facial emotion and reliability from image source
#   gets image and returns probability of emotions
#   API link: https://docs.microsoft.com/ko-kr/azure/cognitive-services/face/
#   Copied and made a small modification from official documentation 
#   https://docs.microsoft.com/ko-kr/azure/cognitive-services/face/quickstarts/client-libraries?tabs=visual-studio&pivots=programming-language-python

class AzureFaceApi:
    def __init__(self):
        self.endpoint = 'https://' + applicationSettings['faceApiEndpointName'] + '.cognitiveservices.azure.com/'
        self.apikey = apikeys['azureface']
        self.face_client = FaceClient(self.endpoint, CognitiveServicesCredentials(self.apikey))

    def detect_face_src(self, image_path):
        # initialize variable in Json format, to return exception string
        j = json.loads('{}')
        #URL = f'http://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.apikey}&lang=kr&units=metric'
        #response = requests.get(URL)
        frame = cv2.imread(image_path)
        _, buf = cv2.imencode('.jpg', frame) # ret
        stream = io.BytesIO(buf)
        detected_faces = self.face_client.face.detect_with_stream(
            image=stream, 
            return_face_attributes=["emotion", "qualityForRecognition"], 
            recognition_model='recognition_04', 
            detection_model='detection_01'
        )
        if not detected_faces:
            msg = {'exception': 'No face detected from image'}
            j.update(msg)
            return j
            #raise Exception('No face detected from image {}'.format(image_name))
        
        #separate string for request "qualityForRecognition"
        qfr = str(detected_faces[0].face_attributes.quality_for_recognition).split('.')
        
        # if quality of output inference is not (high, medium), it is not reliable.
        if qfr[1] != 'high' and qfr[1] != 'medium':
            msg = {'exception': 'output emotion probabilities are not reliable'}
            j.update(msg)
            return j
        
        #unpacking floating point number for request "emotion"
        ret = {}
        ret['anger']        = detected_faces[0].face_attributes.emotion.anger
        ret['contempt']     = detected_faces[0].face_attributes.emotion.contempt
        ret['disgust']      = detected_faces[0].face_attributes.emotion.disgust
        ret['fear']         = detected_faces[0].face_attributes.emotion.fear
        ret['happiness']    = detected_faces[0].face_attributes.emotion.happiness
        ret['neutral']      = detected_faces[0].face_attributes.emotion.neutral
        ret['sadness']      = detected_faces[0].face_attributes.emotion.sadness
        ret['surprise']     = detected_faces[0].face_attributes.emotion.surprise
        j.update(ret)
        return j
        #sample return - json (python dictionary object)
        #please check in main.py that parses properly
        """
                {
                    'anger': 0.0, 
                    'contempt': 0.0, 
                    'disgust': 0.0, 
                    'fear': 0.0, 
                    'happiness': 0.0, 
                    'neutral': 0.0, 
                    'sadness': 0.0, 
                    'surprise': 0.993, 
                    'QualityForRecognition': 'high'
                }
        """


