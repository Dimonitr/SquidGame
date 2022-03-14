#!/usr/bin/python3
import rospy, os, sys, rospkg
import numpy, datetime
import time, cv_bridge, cv2
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import numpy as np
import random
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

bridge = cv_bridge.core.CvBridge()

img_available = False
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
    print("Motion detected")
    #Set crosshair on the target
    crosshair[0],crosshair[1]=int(x+w/2),int(y+h/2)
    breakout=True

  #Drawing crosshair
  cv2.circle(frame, (crosshair[0],crosshair[1]), 50, (0,0,255), 1)
  cv2.line(frame, (crosshair[0]-55,crosshair[1]),(crosshair[0]+55,crosshair[1]),(0,0,255),1)
  cv2.line(frame, (crosshair[0],crosshair[1]-55),(crosshair[0],crosshair[1]+55),(0,0,255),1)
  #Picks a random point and moves the crosshair to it
  if point[0]-5 < crosshair[0] < point[0]+5 and point[1]-5 < crosshair[1] < point[1]+5:
    point = (random.randint(0, frame.shape[0]), random.randint(0, frame.shape[0]))
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
  if breakout:
    for i in range(100):#sometimes frames are missing
      cv2.imshow("Security Feed", frame)
      if (cv2.waitKey(1) & 0xFF) == ord('q'):
            stopped()

  cv2.imshow("Security Feed", frame)
  if (cv2.waitKey(1) & 0xFF) == ord('q'):
        stopped()
  #cv2.imshow("Thresh", thresh)
  #cv2.imshow("Frame Delta", frameDelta)

  firstFrame = gray

  return breakout

def get_image(image_msg):
    global img_available, new_img_msg
    img_available = True
    new_img_msg = image_msg

def player(melody_name):
    global to_files, soundhandle
    soundhandle.stopAll()
    soundhandle.playWave(to_files + melody_name)

def stopped():
  cv2.destroyAllWindows()
  quit()


if __name__ == '__main__':
    global cmd_vel_pub, to_files, soundhandle
    rospy.init_node('demo_squid', anonymous=True)
    rospy.Subscriber('/camera/color/image_raw', Image, get_image)
    soundhandle=SoundClient()

    rospack = rospkg.RosPack()
    to_files=rospack.get_path('squid_demo')+'/audio/'

    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    twist_msg = Twist()
    while not rospy.is_shutdown():
        
        time.sleep(random.uniform(1,5))
        player("red_light.wav")
        print("Red light")
        status_light = np.zeros((700, 700, 3), np.uint8)
        status_light[:] = (0, 0, 255)
        for i in range(50):
            cv2.imshow("Status", status_light)
            cv2.waitKey(1)
        twist_msg.angular.z = 1.6
        for i in range(20):
            cmd_vel_pub.publish(twist_msg)
            time.sleep(0.1)
        twist_msg.angular.z = 0.0
        for i in range(5):
            cmd_vel_pub.publish(twist_msg)
        time.sleep(1)
        firstFrame = None
        i=0
        while i<150:
            if img_available:
                # print("New_image")
                # Convert the image from Image message to OpenCV image format
                cv_image = bridge.imgmsg_to_cv2(new_img_msg, desired_encoding='bgr8')
                # print(cv_image.shape)
                # print(cv_image[1])
                # print("Converted")
                img_available = False
                i+=1
                if motion_detector(cv_image):
                    player("shots_fired.wav")
                    time.sleep(2)
                    break
        twist_msg.angular.z = -1.6
        print("Green light")
        player("green_light.wav")
        status_light = np.zeros((700, 700, 3), np.uint8)
        status_light[:] = (0, 255, 0)
        for i in range(50):
            cv2.imshow("Status", status_light)
            cv2.waitKey(1)
        time.sleep(2)
        for i in range(20):
            cmd_vel_pub.publish(twist_msg)
            time.sleep(0.1)
        twist_msg.angular.z=0.0
        for i in range(5):
            cmd_vel_pub.publish(twist_msg)
    twist_msg.angular.z = 0.0
    for i in range(5):
        cmd_vel_pub.publish(twist_msg)
