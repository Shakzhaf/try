import cv2
import numpy as np

def grabcut(image, rect):
    mask = np.zeros(image.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    cv2.grabCut(image,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    grabcut = image*mask2[:,:,np.newaxis]

    return grabcut

def ycbcr_skin_mask(image):
    img_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    skin_ycrcb_min = np.array((0, 138, 67))
    skin_ycrcb_max = np.array((255, 173, 133))
    blur = cv2.GaussianBlur(img_ycrcb,(11,11),0)
    mask = cv2.inRange(blur, skin_ycrcb_min, skin_ycrcb_max)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    blur = cv2.medianBlur(mask, 5)
    hsv_d = cv2.dilate(mask, kernel)
    res = cv2.bitwise_and(image,image,mask = hsv_d)
    return res

def hsv_skin_mask(image):
    
    blur = cv2.GaussianBlur(image, (3,3), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # lower_color = np.array([108, 23, 82])
    # upper_color = np.array([179, 255, 255])

    lower_color = np.array([0, 58, 50])
    upper_color = np.array([30, 255, 255])

    # lower_color = np.array([0, 10, 60])
    # upper_color = np.array([20, 150, 255])

    # lower_color = np.array([0, 48, 80])
    # upper_color = np.array([20, 255, 255])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    blur = cv2.medianBlur(mask, 5)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    hsv_d = cv2.dilate(blur, kernel)

    return hsv_d

def contour_mask(image):
    # Your code to threshold
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Close contour
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Find outer contour and fill with white
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cv2.fillPoly(close, cnts, [255,255,255])

    # cv2.imshow('close', close)
    # cv2.imshow('image',image)
    return cv2.bitwise_and(image,image, mask = close)

