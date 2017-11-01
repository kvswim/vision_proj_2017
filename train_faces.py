#Record a short clip of video, break down into series of images,
#use images to train new user
import io
import picamera
import cv2
import numpy as np

stream = io.BytesIO()
with picamera.PiCamera() as camera:
	camera.resolution = (640, 480)
	camera.start_recording(stream, format='h264')
	camera.wait_recording(5)
	camera.stop_recording()
