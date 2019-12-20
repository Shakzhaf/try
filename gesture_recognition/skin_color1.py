import cv2
import numpy as np
from pathlib import Path
import sys
from predict_gesture import predict_gesture

# from mis.handtracking.utils import detector_utils as detector_utils
from utils import detector_utils as detector_utils
detection_graph, sess = detector_utils.load_inference_graph()
palm_cascade = cv2.CascadeClassifier('./mis/haar_cascade_code/Hand_haar_cascade.xml')

#defaults
score_thresh=0.5
fps=0
width=320
height=180
display=1
num_workers=4
queue_sie=5

cap = cv2.VideoCapture(cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

num_frames=0
im_width, im_height = width,height
num_hands_detect=2

def convolve(B, r):
	D = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(r,r))
	cv2.filter2D(B, -1, D, B)
	return B



calibarate = True
ret = True

while(ret):
	ret, webcam_img = cap.read()
	webcam_img = cv2.flip(webcam_img,1)
	image_hsv =cv2.cvtColor(webcam_img,cv2.COLOR_BGR2HSV)

	boxes, scores = detector_utils.detect_objects(webcam_img,detection_graph, sess)

	#box_coordinates(num_hands_detect, score_thresh, scores, boxes, im_width, im_height, image_np)
	box_coordinates=detector_utils.box_coordinates(num_hands_detect, score_thresh,scores, boxes, im_width, im_height,webcam_img)
	detector_utils.draw_box_on_image(num_hands_detect, score_thresh,scores, boxes, im_width, im_height,webcam_img)
	if cv2.waitKey(25) & 0xFF == ord('c'):
		calibarate = True
	
	if calibarate==True:
		detector_utils.draw_fps_on_image("calibarating",webcam_img)
		try:
			y_d=box_coordinates[0][1]
			x_d=box_coordinates[0][0]
			h_d=box_coordinates[1][1]-y_d
			w_d=box_coordinates[1][0]-x_d

			print('hand detected at: ',x_d,' , ',y_d,' , ',h_d,' , ',w_d)
			model_hsv = image_hsv[y_d:y_d+h_d, x_d:x_d+w_d]
		except:
			try:
				palms = palm_cascade.detectMultiScale(cv2.cvtColor(webcam_img, cv2.COLOR_BGR2GRAY), 1.3, 5)
				(ex,ey,ew,eh) = palms[0]
				cv2.rectangle(webcam_img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
				(x_d, y_d, w_d, h_d) = palms[0]
				print('hand detected at: ',palms[0][0],' , ',palms[0][1],' , ',palms[0][2],' , ',palms[0][3])
				model_hsv = image_hsv[y_d:y_d+h_d+20, x_d:x_d+w_d+10]
			except:
				print('no hand detected')
				(x_d, y_d, w_d, h_d) = (185,39,75,75)
				cv2.rectangle(webcam_img,(x_d,y_d),(x_d+w_d,y_d+h_d),(0,255,0),2)
				model_hsv = image_hsv[y_d:y_d+h_d+20, x_d:x_d+w_d+10]

		cv2.imshow('input image: ', webcam_img)
		cv2.imshow('sample: ', cv2.cvtColor(model_hsv,cv2.COLOR_HSV2RGB))

		if cv2.waitKey(25) & 0xFF == ord('d'):
			calibarate = False

	
	M = cv2.calcHist([model_hsv], channels=[0, 1], mask=None, 
					histSize=[80, 256], ranges=[0, 180, 0, 256] )

	#Backprojection of our original image using the model histogram M
	B = cv2.calcBackProject([image_hsv], channels=[0,1], hist=M, 
							ranges=[0,180,0,256], scale=1)

	B = convolve(B, r=5)

	#Threshold to clean the image and merging to three-channels
	_, thresh = cv2.threshold(B, 30, 255, cv2.THRESH_BINARY)

	cv2.imshow('input image: ', webcam_img)
	cv2.imshow('sample: ', cv2.cvtColor(model_hsv,cv2.COLOR_HSV2BGR))
	cv2.imshow('answer: ',cv2.bitwise_and(webcam_img,webcam_img, mask = thresh))

	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		cap.release()
		break