# OpenCV_Lego_Detection_and_Counting

## Table of Contents
* [Introduction](#Introduction)
* [Objective](#Objective)
* [Graphical User Interface](#Graphical-User-Interface)
* [Computer vision approach](#Computer-vision-approach)
* [Contrain](#Contrain)
* [Result and discussions](#Result-and-discussions)
* [Conclusion](#Conclusion) 

## Introduction

In machine vision system, a camara is used to capture the image and the computer is used to process, analyse and measure various characteristics for decision making. In this assignment, a machine vision system is to be designed for detection and sorting of Lego Bricks. The characteristic to differentiate the Legos which are used in this design are colour and number of circles in each Lego. For colour detection, thresholding operation using inRange is used. The Legos will be detected base on the range of pixel values in the HSV colour space. The hue (H) channelwhich models the colour type can be very useful in image processing task that need to segment object base on its colour (opencv, n.d.). For Saturation (S) channel, shades of grey represent unsaturated and no white component represent fully saturated (opencv, n.d.). Value (V) channel represent the brightness or the intensity of the colour. Compared to RGB, HSV is easier to segment an object in the image based on its colour (opencv, n.d.). 
<br/><img src="HSV.png" alt="HSV_Colour" width="300"/>
<br/>For circle detection, Hough Transform is used to find circles in an image. OpenCV uses Hough Gradient Method which uses the gradient information of edges (opencv, n.d.).
<br/><img src="Circle_Detection.png" alt="Circle_Detection" width="250"/>

## Objective
This report will be discussing about the program designed for detection and sorting of Lego Bricks. It will be explaining the GUI, the computer vision approach taken to identify the type of Lego and number of Legos. Furthermore, the different constraints will also be discussed. Lastly, the result of the output video will be analysed. 

## Graphical-User-Interface
The following image shows the GUI of the program. 
<br/><img src="GUI.png" alt="GUI" width="600"/>
<br/>The following are the steps on detecting and counting Lego using the GUI above.
1. Select the video level of difficulty from the drop-down option
<br/><img src="Step1.png" alt="Step1" width="300"/> 
2. Click on Start Video button to start Lego detection
<br/><img src="Step2.png" alt="Step2" width="300"/> 
3. Click on Stop button to pause video and Restart button to continue the video
<br/><img src="Step3.png" alt="Step3" width="300"/> 
4. The toggle buttons in the control can do the following:
  <br/>a. Lego Detection toggle button allow the contour and centre point to be drawn on the output video
  <br/><img src="Step4a.png" alt="Step4a" width="300"/> 
  <br/>b. Circle Detection toggle button allow the circle and the centre point of circle to be drawn on the output video
  <br/><img src="Step4b.png" alt="Step4b" width="300"/> 
  <br/>c. Identify Lego toggle button will label the type of Lego in the output video
  <br/><img src="Step4c.png" alt="Step4c" width="300"/> 
5. The table will display the number of Lego detected for each type of Lego and the total 
number of Lego detected in each frame. The badge will alert the user of the Lego 
detected.
<br/><img src="Step5.png" alt="Step5" width="300"/> 
6. When video ended it will be shown beside the drop-down option. Another video level 
of difficulty can be selected from the drop-down option after the video playing have 
stopped.
<br/><img src="Step6.png" alt="Step6" width="300"/> 

## Computer-vision-approach
### Before detection and counting
Initially, the user is asked to select the video base on it level of difficulty for detection and counting. The empty.png image is being displayed in the beginning.


## Contrain

## Result-and-discussions

## Conclusion
