#Kyle Verdeyen
#Computer Vision 600.461 Final Project
#face_detection.py
#Uses a CascadeClassifier to first detect face in frame
#Then uses pretrained model to identify who it is
#For raspberry pi use only - also requires OpenCV2 to be installed (must be built on device)
#Todo: make this live update, push notifications (email?)
import io
import picamera
import cv2
import numpy as np

#index conversions for identified people
database = {1 : "Kyle", 2 : "Jenny"}

def getImage(stream):
	with picamera.PiCamera() as camera:
		camera.resolution = (640,480)
		camera.capture(stream, format='jpeg')
	buff = np.fromstring(stream.getvalue(), dtype = np.uint8)
	image = cv2.imdecode(buff, 1)
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	return gray

def detectFace(gray):
	faces = face_cascade.detectMultiScale(gray, 1.1, 5)
	return faces

def identifyFace(faces, gray):
	predicted = int(0)
	confidence = float(0)
	for (x,y,w,h) in faces:
		predicted, confidence = predictor.predict(gray[y:y+h, x:x+w])
	return predicted, confidence

#loading the DB into RAM takes a long time because I'm using a potato for SD memory
print("Loading database into RAM, this might take a while...")
predictor = cv2.face.LBPHFaceRecognizer_create()
predictor.read('k_j_facedetect.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
print("Database loaded. Starting analysis...")

#do this forever
while(True):
	iostream = io.BytesIO()
	grayimg = getImage(iostream)
	facedetect = detectFace(grayimg)
	prediction, confidencelvl = identifyFace(facedetect, grayimg)
	if prediction != 0 and confidencelvl != 0.0:
		print("Prediction: ", prediction)
		print("Person", database[prediction])
		print("Confidence: ", confidencelvl)
	else:
		print("no faces found. continuing...")
	del grayimg, facedetect, prediction, confidencelvl, iostream #start all over

