# use sommmmmee type of detection, likely a corner/crosshair, or some kind of small pattern etched onto the wafer
# in the corner of it out of the way of where the actual lithography will go
# after detectioing said patter, have a known distance away from where that pattern is etched from the
# target position for the lithography
# move stage accordingly based on where the pattern was found

# can we get a known distance from where the etch happens to the center of the wafer?
# will that position change from wafer to wafer?

# Test a feature match
# Test a corner detection
# Test a edge detection



# Below is a test example program for a corner detection algorithm

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('pattern_code/WIN_20261109_19_04_13_Pro.jpg')
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

corners = cv.goodFeaturesToTrack(gray,25,0.01,10)
corners = np.int32(corners)

for i in corners:
    x,y = i.ravel()
    cv.circle(img,(x,y),3,255,-1)

plt.imshow(img),plt.show()
