import numpy as np
import pandas as pd
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from numpy import loadtxt
from keras.models import load_model
import cv2
# from sklearn.preprocessing import LabelBinarizer
# label_binrizer = LabelBinarizer()
model=load_model('model.h5')

def predict_gesture(img):
	img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#print(img.shape)
	img = np.reshape(img,(28,28,1))
	# print(img)
	cv2.imshow('img',cv2.resize(img, (100,100)))

	#img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#query = model.predict_classes(img.reshape((1,28,28,1)))
	query = np.array([img])
	# print(query.shape)
	prediction=model.predict_classes(query).round()
	return np.argmax(prediction)



# answer=predict_gesture(cv2.imread('0.png'))
# print(answer)