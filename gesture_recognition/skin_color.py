import cv2
import numpy as np
import utilities

palm_cascade = cv2.CascadeClassifier('./mis/haar_cascade_code/Hand_haar_cascade.xml')
calibarate = True
width=320
height=180

def convolve(B, r):
    D = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(r,r))
    cv2.filter2D(B, -1, D, B)
    return B

def put_text(image,text):
    font = cv2.FONT_HERSHEY_SIMPLEX 
    org = (50, 50) 
    fontScale = 1
    color = (255, 0, 0) 
    thickness = 1
    image = cv2.putText(image, text, org, font,  
                    fontScale, color, thickness, cv2.LINE_AA)
    return image

cap = cv2.VideoCapture(cv2.CAP_DSHOW)
ret =True

while ret:
    ret, image = cap.read()
    image  = cv2.resize(image,(width,height))
    image = cv2.flip(image,1)
    image = utilities.contour_mask(image)
    image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV) 

    if cv2.waitKey(25) & 0xFF == ord('c'):
        calibarate = True
    
    if calibarate==True:
        put_text(image,'calibarating')
        try:
            palms = palm_cascade.detectMultiScale(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 1.3, 5)
            (ex,ey,ew,eh) = palms[0]
            cv2.rectangle(image,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            (x_d, y_d, w_d, h_d) = palms[0]
            print('hand detected at: ',palms[0][0],' , ',palms[0][1],' , ',palms[0][2],' , ',palms[0][3])
            model_hsv = image_hsv[y_d:y_d+h_d+20, x_d:x_d+w_d+10]
        except:
            print('no hand detected by haar')
            (x_d, y_d, w_d, h_d) = (185,39,75,75)
            model_hsv = image_hsv[y_d:y_d+h_d+20, x_d:x_d+w_d+10]
        if cv2.waitKey(25) & 0xFF == ord('d'):
            calibarate = False

        
        grabcut = utilities.grabcut(image,(x_d, y_d, w_d, h_d))
        cv2.imshow('grabcut',grabcut)
        # skin = utilities.contour_mask(grabcut)
        # cv2.imshow('skin', skin)

        cv2.imshow('input image: ', image)
        cv2.imshow('sample: ', cv2.cvtColor(model_hsv,cv2.COLOR_HSV2RGB))
        

    #Get the model histogram M
    M = cv2.calcHist([model_hsv], channels=[0, 1], mask=None, 
                    histSize=[80, 256], ranges=[0, 180, 0, 256] )

    #Backprojection of our original image using the model histogram M
    B = cv2.calcBackProject([image_hsv], channels=[0,1], hist=M, 
                            ranges=[0,180,0,256], scale=1)

    B = convolve(B, r=5)

    #Threshold to clean the image and merging to three-channels
    _, thresh = cv2.threshold(B, 30, 255, cv2.THRESH_BINARY)

    cv2.imshow('input image: ', image)
    # cv2.imshow('preprocessed: ', preprocess(image))
    cv2.imshow('sample: ', cv2.cvtColor(model_hsv,cv2.COLOR_HSV2RGB))
    cv2.imshow('answer: ',cv2.bitwise_and(image,image, mask = thresh))

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break