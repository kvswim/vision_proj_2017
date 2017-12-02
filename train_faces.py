#Kyle Verdeyen
#Computer Vision 600.461 Final Project
#train_faces.py
#take series of images, identify face in image, and train a classifier based on it
#For PC use. Don't try running this on a Pi, you will CRASH your device.
#This loves to eat RAM, 4GB+ highly recommended 
#Try to keep the final database <400MB in order to fit into the Pi's RAM.
#2 people with 1000 images each yields a database of size 261mb. 
#todo: allow updating of database
#dream todo: improve RAM consumption, multithread or CUDA support
import sys
import io
import os
import cv2
import numpy as np

def get_images_labels(filepath):
    image_path = [os.path.join(filepath, f) for f in os.listdir(filepath)]
    images = []
    labels = []
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    for path in image_path:
        grayscale_image = cv2.imread(path, 0)
        subject = os.path.split(path)[1].split('.')[0].replace('subject','')
        face = face_cascade.detectMultiScale(grayscale_image)
        for (x, y, w, h) in face:
            images.append(grayscale_image[y: y+h, x: x+w])
            labels.append(subject)

            #print("Added subject %s to DB" % subject)
        del grayscale_image, subject, face # minimal effort to conserve RAM use
    return images, labels

#using local binary patterns histograms algorithm
#saves speed over Haar training
print("Building database...")
images, labels = get_images_labels('./subjectimages')
print("DB complete. Now training...")
labels = map(int, labels) #convert strings to ints
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(images, np.array(labels))
recognizer.write('k_j_facedetect.xml')
print("Done.")
#recognizer.read
