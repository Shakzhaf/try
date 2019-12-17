import cv2
import numpy as np
from pathlib import Path
import sys


# path_to_utils = Path("C:/Users/hp/intuitive_user_interface/gesture_recognition/mis/handtracking/utils")
# path_to_haar = Path("C:/Users/hp/intuitive_user_interface/gesture_recognition/mis/haar_cascade_code")

# insert at 1, 0 is the script path (or '' in REPL)
# sys.path.append("..")
#sys.path.append("C:/Users/hp/intuitive_user_interface/gesture_recognition/mis/haar_cascade_code")

# from mis.handtracking.utils import detector_utils as detector_utils
from utils import detector_utils as detector_utils
detection_graph, sess = detector_utils.load_inference_graph()
palm_cascade = cv2.CascadeClassifier('./mis/haar_cascade_code/Hand_haar_cascade.xml')

#defaults
score_thresh=0.5
fps=1
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



ret = True

while(ret):
	ret, webcam_img = cap.read()
	webcam_img = cv2.flip(webcam_img,1)
	
	try:
		webcam_img = cv2.cvtColor(webcam_img, cv2.COLOR_BGR2RGB)
	except:
		print("Color conversion error")

	boxes, scores = detector_utils.detect_objects(webcam_img,
                                                      detection_graph, sess)


#box_coordinates(num_hands_detect, score_thresh, scores, boxes, im_width, im_height, image_np)
	box_coordinates=detector_utils.box_coordinates(num_hands_detect, score_thresh,
                                         scores, boxes, im_width, im_height,
                                         webcam_img)

	

	detector_utils.draw_box_on_image(num_hands_detect, score_thresh,
                                         scores, boxes, im_width, im_height,
                                         webcam_img)

	try:
		y_d=box_coordinates[0][1]
		x_d=box_coordinates[0][0]
		h_d=box_coordinates[1][1]-y_d
		w_d=box_coordinates[1][0]-x_d

		feed_image = webcam_img[y_d:y_d+h_d, x_d:x_d+w_d]

		feed_image = cv2.resize(feed_image,(100,100))
		#feed_image = cv2.cvtColor(feed_image, cv2.COLOR_BGR2GRAY)
		
		cv2.imshow('feed_image',feed_image)
	except:
		#print('no boxes maybe')
		try:
			palms = palm_cascade.detectMultiScale(cv2.cvtColor(webcam_img, cv2.COLOR_BGR2GRAY), 1.3, 5)
			for (ex,ey,ew,eh) in palms:
				cv2.rectangle(webcam_img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
			y_d=palms[0][1]
			x_d=palms[0][0]
			h_d=palms[0][3]
			w_d=palms[0][2]

			feed_image = webcam_img[y_d:y_d+h_d, x_d:x_d+w_d]

			feed_image = cv2.resize(feed_image,(100,100))
			#feed_image = cv2.cvtColor(feed_image, cv2.COLOR_BGR2GRAY)
			
			cv2.imshow('feed_image',feed_image)
		except:
			print('no boxes maybe')

	if (display > 0):
		if (fps > 0):
			detector_utils.draw_fps_on_image("FPS : " + str(int(fps)),
                                             webcam_img)
		cv2.imshow('Single-Threaded Detection',cv2.cvtColor(webcam_img, cv2.COLOR_RGB2BGR))

		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			cap.release()
			break
	else:
		print("frames processed: ", num_frames, "elapsed time: ",
              elapsed_time, "fps: ", str(int(fps)))



