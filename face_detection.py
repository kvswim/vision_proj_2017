#Kyle Verdeyen
#Computer Vision 600.461 Final Project
#face_detection.py
#Uses a CascadeClassifier to first detect face in frame
#Then uses pretrained model to identify who it is
#For raspberry pi use only - also requires OpenCV2 to be installed (must be built on device)
#Todo: attach image of entrant in email
import io
import time
import picamera
import cv2
import smtplib
import numpy as np
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
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
	predicted = int(0) #in the event no faces are detected we want these to return 0
	confidence = float(0)
	for (x,y,w,h) in faces:
		predicted, confidence = predictor.predict(gray[y:y+h, x:x+w])
	return predicted, confidence

def sendEmail(predicted, confidence):
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465) #SSL port for Gmail
	server.ehlo() #identify ourselves to the server, Gmail prefers EHLO rather than HELO
	server.login("pivision2017", "vision2017") #username, password (tester address pivision2017@gmail.com)
	
	originaddress = "pivision2017@gmail.com" #From:
	destaddress = "pivision2017@gmail.com" #To:
	message = MIMEMultipart() #compose a composite email
	message["From"], message["To"], message["Subject"] = originaddress, destaddress, "New entry detected!"
	entrant = database[predicted]
	if confidence > 50:
		body = entrant + " has entered, with a confidence level of " + str(confidence)
	else:
		body = "Unknown entrant detected. I think it's " + entrant + "but my confidence is only" + str(confidence)
	body = MIMEText(body)
	message.attach(body)

	text = message.as_string()
	server.sendmail(originaddress, destaddress, text)
	server.close()


#loading the DB into RAM takes a long time because I'm using a potato for SD memory
print("Loading database into RAM, this might take a while...")
predictor = cv2.face.LBPHFaceRecognizer_create()
predictor.read('k_j_facedetect.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
print("Database loaded. Starting analysis...")
lasttime = None #variable to check the last time an email was sent to prevent spamming


#do this forever
while(True):
	iostream = io.BytesIO()
	grayimg = getImage(iostream)
	facedetect = detectFace(grayimg)
	prediction, confidencelvl = identifyFace(facedetect, grayimg)
	if prediction != 0 and confidencelvl != 0.0: #we've detected someone in frame
		if lasttime is None or time.time()-lasttime > 30: #if we have never sent an email or it's been at least 30 seconds since the last email
			sendEmail(prediction, confidencelvl)
			lasttime = time.time()
		else:
			print("email cooldown in effect")
	else:
		print("no faces found. continuing...")
	del grayimg, facedetect, prediction, confidencelvl, iostream #start all over
