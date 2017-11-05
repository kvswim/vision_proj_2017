import io
import picamera
import cv2
import numpy as np

#init memory stream so images don't need to be saved/read
#so we aren't slamming the SD
stream = io.BytesIO()

#get image
with picamera.PiCamera() as camera:
	camera.resolution = (640,480)
	camera.capture(stream, format='jpeg')

buff = np.fromstring(stream.getvalue(), dtype = np.uint8)

image = cv2.imdecode(buff, 1)
face_cascade = cv2.CascadeClassifier('/home/pi/vision_proj_2017/haarcascade_frontalface_alt.xml')
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.1, 5)
predictor = cv2.face.LBPHFaceRecognizer_create()
print("Loading database...")
predictor.read('k_j_facedetect.xml')
print("Database loaded.")
print('found '+str(len(faces))+' faces')
for (x,y,w,h) in faces:
	cv2.rectangle(image, (x,y), (x+w, y+h), (255,255,0),2)
	predicted, confidence = predictor.predict(gray[y:y+h, x:x+w])
	print("Prediction:")
	print(predicted)
	print("Confidence:")
	print(confidence)
	cv2.imshow("Recognized face", image[y:y+h,x:x+w])
	cv2.waitKey(0)
	cv2.destroyAllWindows()
cv2.imwrite('result.jpg',image)
