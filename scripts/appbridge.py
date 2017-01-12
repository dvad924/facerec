from facerecognition.rosdemo import ROS_Facing
from multiprocessing import Lock

def init():
    classifierLock = Lock()
    cb,destroy = ROS_Facing(classifierLock)

    return cb,destroy


