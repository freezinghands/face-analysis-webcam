# You need to set variable like below
# export GOOGLE_APPLICATION_CREDENTIALS="/home/jy-ubuntu/jyMUSIC/neural-cable-344014-52d1da893e58.json"
# JSON file should be placed in.
# Google service account should be set. For more information visit https://cloud.google.com/docs/authentication/getting-started 
import io
from google.cloud import vision
import time

def detect_faces(path):
    """Detects faces in an image."""
    #client_options = {'api_endpoint': 'us-vision.googleapis.com'}
    #client = vision.ImageAnnotatorClient(client_options=client_options)
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        #print('sadness: {}'.format(likelihood_name[face.sadness_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

print("----trial 1----")
s = time.time()
detect_faces('capture/face-20220313-000128.jpg')
e = time.time()
print("----elapsed time: {:.4f}----".format(e - s))
print("----trial 2----")
s = time.time()
detect_faces('capture/face-20220313-085222.jpg')
e = time.time()
print("----elapsed time: {:.4f}----".format(e - s))

