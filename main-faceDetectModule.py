from faceFeature import MirrorFaceDetect


app = MirrorFaceDetect()

def main():
	for _ in range(1):
		print(app.detect_motion_webcam())



if __name__ == '__main__':
	main()