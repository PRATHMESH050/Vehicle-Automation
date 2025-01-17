import cv2
import numpy as np

def make_coordinates(image,line_parameters ):
  slope, intercept = line_parameters
  y1 = image.shape[0]
  y2 = int(y1*3/5)
  x1 = int((y1- intercept)/slope)
  x2 = int((y2-intercept)/slope)
  return np.array([x1,y1,x2,y2])
  

def average_slope_intercept(image , lines):
  left_fit = []
  right_fit = [] 
  if lines is None:
    return None 
  for line in lines:
    for x1,y1,x2,y2 in line:
      fit = np.polyfit((x1,x2),(y1,y2),1)
      slope = fit[0]
      intercept = fit[1]
      if slope < 0:
        left_fit.append((slope, intercept))
      else:
        right_fit.append((slope, intercept))

  left_fit_average = np.average(left_fit, axis = 0)
  right_fit_average = np.average(right_fit,axis=0) 
  left_line = make_coordinates(image , left_fit_average)
  right_line = make_coordinates(image , right_fit_average)
  averaged_line = [left_line, right_line]
  return averaged_line



def canny(image):
  gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
  blur = cv2.GaussianBlur(gray,(5,5),0)
  canny = cv2.Canny(blur,30,150)
  return canny




def display_line(image, lines):
  line_image = np.zeros_like(image)
  if lines is not None:
    for line in lines:
      x1, y1, x2, y2 = line.reshape(4)
      cv2.line(line_image, (x1,y1), (x2,y2), [255,0,0], 10)
  return line_image




def region_of_intrest(image):
  height = image.shape[0]
  width = image.shape[1]
  mask =  np.zeros_like(image)
  polygons = np.array([[(200,height), (1100, height), (550, 250)]])
  
  cv2.fillPoly(mask, polygons, 255)
  masked_image = cv2.bitwise_and(canny,mask)
  return masked_image



image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny_image = canny(lane_image)
cropped_image = region_of_intrest(canny_image)
lines = cv2.HoughLinesP(cropped_image,2,np.pi/180, 100, np.array([]),minLineLength=40,maxLineGap=5)
averaged_line = average_slope_intercept(lane_image,lines)
line_image = display_line(lane_image, lines)
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
cv2.imshow('result',combo_image)
cv2.waitKey(0)