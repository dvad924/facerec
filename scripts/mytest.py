#! /usr/bin/env python
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String, Header
from cv_bridge import CvBridge, CvBridgeError
from message_filters import TimeSynchronizer, Subscriber
from Ros_Coms.msg import bbox,bbox_array
from Ros_Coms.msg import conf,Face,Face_array
import cv2
import appbridge
import dlib

class drec:
    def __init__(self,bbox=None):
        if bbox is not None:
            self.unpackbbox(bbox)
    def unpackbbox(self,bbox):
        self.box = bbox
    def top(self):
        return self.box.ymin
    def bottom(self):
        return self.box.ymax
    def left(self):
        return self.box.xmin
    def right(self):
        return self.box.xmax
    
bridge = CvBridge()
frCB,frDestroy = appbridge.init()

publisher1 = None
publisher2 = None

settings = None
def todrect(bbox):
    rec = drec( bbox )
    return dlib.rectangle( rec.left(), rec.top(), rec.right(), rec.bottom() )
    
def furtherCallback( data ):
    return frCB( data )

def tobbox( box ):
    b = bbox()
    b.xmin = box.left()
    b.xmax = box.right()
    b.ymin = box.top()
    b.ymax = box.bottom()
    return b

def toconf( con ) :
    c = conf()
    c.pred = con['name']
    c.score = con['score']
    return c

def toFaceMsgs( faces ):
    Fs = Face_array()
    Fs.Faces = []
    for face in faces:
        f = Face()
        f.id = face['id']
        f.box = tobbox(face['box'])
        f.confs = map(toconf,face['conf'])
        Fs.Faces.append(f)
    Fs.header = Header()
    Fs.header.stamp = rospy.Time.now()
    return Fs

def callback( im_msg, bbox_array ):
    print("!RECIEVED IMAGE!")
    try:
        cv2_img = bridge.imgmsg_to_cv2( im_msg, "bgr8" )
        bboxes = map( todrect, bbox_array.bboxes )
        len( bboxes )
        if len( bboxes ) == 0:
            return
        f,finfo = furtherCallback( ( bboxes, cv2_img ) )    
        frame1_message = bridge.cv2_to_imgmsg( f, "bgr8" )
        face_msg = toFaceMsgs( finfo )
        

        publisher1.publish( frame1_message )
        publisher2.publish( face_msg )
    
        
    except CvBridgeError, e:
        print( e )

def cmdcallback( msg ) :
    global settings
    settings = commandhandler( msg )
        
def main():
    rospy.init_node( 'darknet_cam_sub' )
    print ( "I do Live" )
    image_topic = 'darknet_cam'
    
    incam   = rospy.resolve_name( "incam" )
    inboxes = rospy.resolve_name( "inboxes" )
    outanns = rospy.resolve_name( "out" )
    viz     = rospy.resolve_name( "viz" )
    outface = rospy.resolve_name( "outface" )


    
    incam   = incam   if incam   != "/incam"   else "/darknet_cam"
    inboxes = inboxes if inboxes != "/inboxes" else "/darknet_bboxes"
    outanns = outanns if outanns != "/out"     else "/TheFaces/annotated"
    viz     = viz     if viz     != "/viz"     else "/TheFaces/viz"
    outface = outface if outface != "/outface" else "/TheFaces/labels"

    
    print( "img topic:" , incam )
    print( "bbox topic:", inboxes )
    print( "out annot: ", outanns )
    print( "viz:" , viz )
    print( "outface:", outface )

    #identify global variables
    global publisher1
    global publisher2 
    
    publisher1 = rospy.Publisher( outanns , Image , queue_size = 1 )
    publisher2 = rospy.Publisher( outface , Face_array, queue_size = 1 )

    # image and bounding box subscribers
    tss = TimeSynchronizer( ( Subscriber( incam , Image ),
                              Subscriber( inboxes , bbox_array ) ) , 1 )
    tss.registerCallback( callback )
    #####################################################################

    # GUI command listener
    # guicmds = rospy.Subscriber( uicmds, String, cmdcallback )
    ####################################################################
    rospy.spin()

if __name__ == '__main__':
    main()
    print("I'm Not Dead Yet")
    frDestroy()
    print("Now I'm Dead")
