#! /usr/bin/env python
import rospy
from std_msgs.msg import String



def main():
    rospy.init_node('texter')
    pub = rospy.Publisher('speech_commands',String)
    r = rospy.Rate(0.1) # 10s gap
    while not rospy.is_shutdown():
        pub.publish("Who is that guy in the corner?")
        r.sleep()

if __name__ == "__main__":
    main()
