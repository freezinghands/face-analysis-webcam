from dataManagerFaceapi import AzureFaceApi

f1 = AzureFaceApi()

v = f1.detect_face_src('capture/face-20220313-085222.jpg')

print(v)

