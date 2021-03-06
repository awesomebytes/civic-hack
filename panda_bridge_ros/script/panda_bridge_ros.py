#!/usr/bin/env python

import rospy
from panda import Panda
from std_msgs.msg import String
from can_msgs.msg import Frame

def panda_bridge_ros():

    can_pub_ = rospy.Publisher('can_frame_msgs', Frame, queue_size=10)
    rospy.init_node('can_bridge', anonymous=True)
    rate = rospy.Rate(200) # 10hz

    panda = Panda()

    while not rospy.is_shutdown():

	can_msg = panda.can_recv()

	if can_msg:

		frame = convert_panda_to_msg(can_msg[0])
		frame.header.frame_id = ""
		frame.header.stamp = rospy.get_rostime()

		can_pub_.publish(frame)

    	rate.sleep()

def convert_panda_to_msg(can_msg):
	
	frame = Frame()
	frame.id = can_msg[0]
	frame.dlc = 8 
	frame.is_error = 0
	frame.is_rtr = 0
	frame.is_extended = 0

	frame.data = can_msg[2]

	return frame

if __name__ == '__main__':
    try:
        panda_bridge_ros()
    except rospy.ROSInterruptException:
        pass
