




#DNN model source path which will be used in cv2.dnn
prototxt = 'model/deploy.prototxt'
model = 'model/res10_300x300_ssd_iter_140000.caffemodel'


def detect_faces(frame):
	net = cv2.dnn.readNetFromCaffe(prototxt, model)

	image = imutils.resize(frame, width=400)
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    return detections