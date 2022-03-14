#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan

np.warnings.filterwarnings('ignore')
FOV=86
def callback(data):   
    global distances 
    distances = data.ranges
    array_length = len(distances)
    cropped_array = distances#[motion_from:motion_to]
    distance_to_human = np.nanmin(cropped_array)
    index = np.nanargmin(cropped_array)
    angle_zero = (320 - index)/320*FOV/2
    print(f"Length: {array_length} Min distance: {distance_to_human} Index: {index} Angle: {angle_zero}")
    

if __name__ == '__main__':
    try:
        rospy.init_node('laserscan_to_distance', anonymous=True)
        rospy.Subscriber('scan', LaserScan, callback)
        rospy.spin()
    except rospy.ROSInterruptException: pass