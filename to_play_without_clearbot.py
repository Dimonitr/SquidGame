import datetime
import numpy as np
import time
import cv2
import random
# This is demo without robotont for just motion detection. It fails here but doesn't fail on robotont

vs = cv2.VideoCapture(0)

firstFrame = None
area = 70
crosshair = [0,200]
point = (300,300)

# loop over the frames of the video
def motion_detector(frame):
  global firstFrame, crosshair, point
  breakout = False
  # grab the current frame and initialize the occupied/unoccupied
  # text
  text = "Unoccupied"
  # if the frame could not be grabbed, then we have reached the end
  # of the video
  if frame is None:
    return False

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (21, 21), 0)

  # compute the absolute difference between the current frame and
  # first frame
  if firstFrame is None:
    firstFrame = gray

  frameDelta = cv2.absdiff(firstFrame, gray)
  thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
  # dilate the thresholded image to fill in holes, then find contours
  # on thresholded image
  kernel = np.ones((40,40), 'uint8')
  thresh = cv2.dilate(thresh, kernel, iterations=5)
  thresh = cv2.erode(thresh, kernel, iterations=1)
  cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
  # loop over the contours
  for c in cnts:
    # if the contour is too small, ignore it
    if cv2.contourArea(c) < area:
      continue
    # compute the bounding box for the contour, draw it on the frame,
    # and update the text
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    text = "Occupied"
    #Set crosshair on the target
    crosshair[0],crosshair[1]=int(x+w/2),int(y+h/2)
    breakout=True

  #Drawing crosshair
  cv2.circle(frame, (crosshair[0],crosshair[1]), 50, (0,0,255), 1)
  cv2.line(frame, (crosshair[0]-55,crosshair[1]),(crosshair[0]+55,crosshair[1]),(0,0,255),1)
  cv2.line(frame, (crosshair[0],crosshair[1]-55),(crosshair[0],crosshair[1]+55),(0,0,255),1)
  #Picks a random point and moves the crosshair to it
  if point[0]-5 < crosshair[0] < point[0]+5 and point[1]-5 < crosshair[1] < point[1]+5:
    point = (random.randint(0, vs.get(cv2.CAP_PROP_FRAME_WIDTH)), random.randint(0, vs.get(cv2.CAP_PROP_FRAME_HEIGHT)))
  if crosshair[0] < point[0] and abs(crosshair[0] - point[0])>=5:
    crosshair[0] += 5
  elif crosshair[0] > point[0] and abs(crosshair[0] - point[0])>=5:
    crosshair[0] -= 5
  if crosshair[1] < point[1] and abs(crosshair[1] - point[1])>=5:
    crosshair[1] += 5
  elif crosshair[1] > point[1] and abs(crosshair[1] - point[1])>=5:
    crosshair[1] -= 5

  # draw the text and timestamp on the frame
  cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
  cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
  # show the frame and record if the user presses a key
  cv2.imshow("Security Feed", frame)
  cv2.waitKey(1)
  #cv2.imshow("Thresh", thresh)
  #cv2.imshow("Frame Delta", frameDelta)

  firstFrame = gray

  return breakout

while True:
    print("Red light")
    for i in range(200):# Red light
        frame = vs.read()[1]
        if motion_detector(frame):
            break
    print("Green light")
    time.sleep(3)# Green light time