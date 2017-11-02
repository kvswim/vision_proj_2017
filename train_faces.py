#take series of images, identify face in image,
#and train a classifier based on it 
import sys
import io
import os
import picamera
import cv2
import numpy as np

def get_images_labels(filepath):
    image_path = [os.path.join(filepath, f) for f in os.listdir(filepath)]
    images = []
    labels = []
    face_cascade = cv2.CascadeClassifier('/home/pi/vision_proj_2017/haarcascade_frontalface_alt.xml')
    for path in image_path:
        grayscale_image = cv2.imread(path, 0)
        subject = os.path.split(path)[1].split('.')[0].replace('subject','')
        face = face_cascade.detectMultiScale(grayscale_image)
        for (x, y, w, h) in face:
            images.append(images[y: y+h][x: x+w])
            labels.append(subject)
            print("Adding subject %s to DB" % subject)
    return images, labels

#using local binary patterns histograms algorithm
#saves speed over Haar training

images, labels = get_images_labels('./subjectimages')
recognizer = cv2.createLBHFFaceRecognizer()
recognizer.train(images, np.array(labels))
recognizer.save('k_j_facedetect.xml')
