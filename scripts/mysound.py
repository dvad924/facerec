#! /usr/bin/env python
import rospy
from std_msgs.msg import String

import facerecognition.tts as tts

def callback(stringmsg):
    string = stringmsg.data
    print(string)
    tts.gentts(str(string))

def main():
    rospy.init_node('speech')
    print( "i'm alive")
    msg_topic = 'speech_commands'

    mysub = rospy.Subscriber(msg_topic,String,callback)

    rospy.spin()

if __name__ == '__main__':
    main()

    
