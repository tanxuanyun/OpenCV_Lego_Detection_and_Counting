import logging
import sys
from tkinter import Tk, messagebox
import eel
import base64
import time
import os
import json
import cv2
import numpy as np
from camera import VideoCamera


lower={'Yellow':(14,90,0),'Orange':(4,49,160),'Mediumazure':(84,58,77),'Lime':(9,72,104),'Lightgray':(0,0,83),'Grey':(0,0,44),'Green':(51,39,65),'Mediumblue':(102,53,70)}

upper={'Yellow':(28,255,255),'Orange':(12,206,196),'Mediumazure':(104,215,198),'Lime':(37,162,152),'Lightgray':(209,40,140),'Grey':(192,39,83),'Green':(69,127,146),'Mediumblue':(137,162,152)}

global x

# Read Images
img = cv2.imread("./web/image/empty.png",cv2.IMREAD_GRAYSCALE)

# Setup the images to display in html file
@eel.expose
def setup():
   text_send_to_js("Select the level of difficulty before pressing Start Video ", "p1")
   img_send_to_js(img, "output")
 
#  Your code depend on image processing
# This is a sample code to change 
# and send processed image to JavaScript  
@eel.expose
def video_feed():
  global x
  option= eel.get_Option()()
  if option == 'Level 1':
    video_name = "./web/image/brick1_02.mp4"
  elif option == 'Level 2':
    video_name = "./web/image/brick3_10.mp4"
  elif option == 'Level 3':
    video_name = "./web/image/brick6_14.mp4"
  else:
    text_send_to_js("Select the level of difficulty before pressing Start Video", "p1")

  if option == 'Level 1' or option == 'Level 2' or option == 'Level 3':
    x = VideoCamera(video_name)
    y = process(x)
    text_send_to_js("Wait until the end of video before selecting the next video", "p2")
    #stop early
    z=cv2.VideoCapture(video_name)
    nFrames = int(z.get(cv2.CAP_PROP_FRAME_COUNT))
    a=0
    for frame in y:
      #    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      img_send_to_js(frame, "output")
      a=a+1
      if a==(nFrames-2):
        break
    text_send_to_js("Video Ended", "p2")
      

# Get Camera from video feed
# Add ur codes to process here

def process(camera):
  cntFrame=24
  while True:
      cntFrame=cntFrame+1
      success, frame = camera.get_frame()
      lego_val = {
        "yellow2x2":0,
         "yellow2x3":0, 
         "yellow2x4":0,
         "lime2x2":0,
         "lime2x4":0,
         "orange2x2":0,
         "orange2x4":0,
         "mediumblue2x4":0,
         "mediumazure4x6":0, 
         "lightgray2x4":0,
         "grey2x8":0,
         "green2x8":0,
         "total":0}
      badge_update_dict={
        "yellow2x2badge":"",
         "yellow2x3badge":"", 
         "yellow2x4badge":"",
         "lime2x2badge":"",
         "lime2x4badge":"",
         "orange2x2badge":"",
         "orange2x4badge":"",
         "mediumblue2x4badge":"",
         "mediumazure4x6badge":"", 
         "lightgray2x4badge":"",
         "grey2x8badge":"",
         "green2x8badge":"",}
      blurred = cv2.GaussianBlur(frame, (11, 11), 0)
      hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
      for key, value in upper.items():
          kernel = np.ones((9,9),np.uint8)
          mask = cv2.inRange(hsv, lower[key], upper[key])
          
          if cv2.countNonZero(mask) == 0:
            continue
          
          mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
          mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

          contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
          center = None

          #Circle Detection
          gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
          gray_blurred = cv2.blur(gray, (3, 3))
          mask_lego = cv2.bitwise_and(gray_blurred, gray_blurred, mask=mask) 
          detected_circles = cv2.HoughCircles(mask_lego,cv2.HOUGH_GRADIENT, 1, 20, param1 = 19, param2 =12, minRadius = 5, maxRadius = 10)

          if detected_circles is not None: 

            # Convert the circle parameters a, b and r to integers. 
            detected_circles = np.uint16(np.around(detected_circles))
            
            
            #lego contour 
            for i in range(len(contours)):
              area = cv2.contourArea(contours[i])
              if (area>2500):
                M = cv2.moments(contours[i])
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                rect = cv2.minAreaRect(contours[i])
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                contour= eel.contour()()
                if contour==True:
                  cv2.drawContours(frame,[box],0,(0,255,0),2)
                  cv2.circle(frame,center, 5, (0, 255, 0), -1)
                numcircle=0
                for pt in detected_circles[0, :]:
                  a, b, r = pt[0], pt[1], pt[2]
                  dist=cv2.pointPolygonTest(contours[i],(a, b),False)
                  if dist==1:
                    numcircle=numcircle+1
                  circle= eel.circle()()
                  if circle==True:
                    cv2.circle(frame, (a, b), r, (0, 255, 0), 1) 
                    cv2.circle(frame, (a, b), 1, (0, 0, 255), 1) 
                    
                #determine type of lego base on number of circle
                text=legotype(numcircle,key)
                badge=text+"badge"
                #text=str(numcircle) +" "+ key + " lego"
                label= eel.label()()
                if label==True:
                  cv2.putText(frame,str(text), center, cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,0,0),2)
                if cntFrame%25 == 0:
                  lego_val[text]=lego_val[text]+1
                  badge_update_dict[badge]="New"
                  lego_val["total"]=lego_val["total"]+1
                  lego_val_send_to_js(lego_val)
                  badge_update(badge_update_dict)

      yield frame


def lego_val_send_to_js(lego_val):
  for key, value in lego_val.items():
    text_send_to_js(str(value), key)

def badge_update(badge_update_dict):
  for key, value in badge_update_dict.items():
    text_send_to_js(str(value), key)


def legotype(num,colour):
  name=""
  if colour=="Green":
    name="green2x8"
  elif colour=="Grey":
    name="grey2x8"
  elif colour=="Lightgray":
    name="lightgray2x4"
  elif colour=="Mediumazure":
    name="mediumazure4x6"
  elif colour=="Mediumblue":
    name="mediumblue2x4"
  elif colour=="Orange":
    if num<=5:
      name="orange2x2"
    elif num>5 :
      name="orange2x4"
  elif colour=="Lime":
    if num<=5:
      name="lime2x2"
    elif num>5 :
      name="lime2x4"
  elif colour=="Yellow":
    if num<=4:
      name="yellow2x2"
    elif num>4 and num<=6:
      name="yellow2x3"
    elif num>6 :
      name="yellow2x4"
  return name




# Stop Video Capturing
# Do not touch
@eel.expose
def stop_video_feed():
  x.stop_capturing()
  text_send_to_js("Video Stopped", "p2")
  
# Restart Video Caturing
# Do not touch
@eel.expose
def restart_video_feed():
  x.restart_capturing()
  text_send_to_js("Video Started", "p2")
  
# Send text from python to Javascript 
# Do not touch
def text_send_to_js(val,id):
  eel.updateTextSrc(val,id)()

# Send image from python to Javascript 
# Do not touch
def img_send_to_js(img, id):
  if np.shape(img) == () :
    
    eel.updateImageSrc("", id)()
  else:
    ret, jpeg = cv2.imencode(".jpg",img)
    jpeg.tobytes()
    blob = base64.b64encode(jpeg) 
    blob = blob.decode("utf-8")
    eel.updateImageSrc(blob, id)()

# Start function for app
# Do not touch
def start_app():
  try:
    start_html_page = 'index.html'
    eel.init('web')
    logging.info("App Started")

    eel.start('index.html', size=(1000, 800))

  except Exception as e:
    err_msg = 'Could not launch a local server'
    logging.error('{}\n{}'.format(err_msg, e.args))
    show_error(title='Failed to initialise server', msg=err_msg)
    logging.info('Closing App')
    sys.exit()

if __name__ == "__main__":
  #x = VideoCamera(video_name)
  start_app()