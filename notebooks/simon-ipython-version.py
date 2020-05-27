# In[1]

import sys
sys.path.append('../../robotics-course/build')
sys.path.append('../../robotics-course/scenarios/build')
import cv2 as cv
import numpy as np
import libry as ry
import time
# from perception import find_ball
print(cv.__version__)

# In[2]

#Let's edit the real world before we create the simulation
RealWorld = ry.Config()
RealWorld.addFile("../../robotics-course/scenarios/challenge.g")
V = ry.ConfigurationViewer()
V.setConfiguration(RealWorld)

# In[3]

# you can also change the shape & size
targetObj=RealWorld.getFrame("obj0")
targetObj.setColor([1.,0,0])
# targetObj.setShape(ry.ST.sphere, [.03])
RealWorld.getFrame("obj0").setShape(ry.ST.ssBox, [.05, .05, .05, .01])
targetObj.setPosition([-0.1, .1, 0.7])
targetObj.setContact(1)

#remove some objects
for o in range(1,30):
    name = "obj%i" % o
    print("deleting", name)
    RealWorld.delFrame(name)

V.recopyMeshes(RealWorld)
V.setConfiguration(RealWorld)

# In[4]

# instantiate the simulation
S = RealWorld.simulation(ry.SimulatorEngine.physx, True)
S.addSensor("camera")

# In[5]

# create your model world
C = ry.Config()
C.addFile('../../robotics-course/scenarios/pandasTable.g')
#V = ry.ConfigurationViewer()
V.setConfiguration(C)
cameraFrame = C.frame("camera")

#the focal length
f = 0.895
f = f * 360.
fxfypxpy = [f, f, 320., 180.]

# save initial background
[rgb0, depth0] = S.getImageAndDepth()  #we don't need images with 100Hz, rendering is slow
points0 = S.depthData2pointCloud(depth0, fxfypxpy)

# In[6]

obj = C.addFrame("object")
# obj.setShape(ry.ST.sphere, [.03])
obj.setShape(ry.ST.ssBox, [.05, .05, .05, .01])
obj.setColor([0,1,0])
obj.setContact(1)
obj.setPosition([0,0,1])

V.setConfiguration(C)

# In[7]

sys.path.append('../')
from robot import Robot

robo = Robot(0.01, C, V, S, ry)
RSTATE = 2
for t in range(1000):
    # do perception
    if t%10 == 0:
        [rgb, depth] = S.getImageAndDepth()  #we don't need images with 100Hz, rendering is slow
        points = S.depthData2pointCloud(depth, fxfypxpy)
       
        # skipping perception
        p_obj = targetObj.getPosition()   
        r_obj = targetObj.getQuaternion()
        obj.setPosition(p_obj)
        obj.setQuaternion(r_obj)

        V.recopyMeshes(C)
        V.setConfiguration(C)

    # do state update
    if RSTATE == 0:
        pos = [0.2+0.8*np.sin(t/100),0,1]
        finish = robo.move_gripper_to_pos("R_gripper", pos)
        if finish:
            RSTATE = 3
    elif RSTATE == 1:
        pos = [0.5, 0, 1.5]
        finish = robo.move_gripper_to_pos("R_gripper", pos)
        if finish:
            RSTATE = 3
    elif RSTATE == 2:
        finish = robo.grasp("R_gripper", "object")
        if finish:
            RSTATE = 1
    elif RSTATE == 3:
        finish = robo.delayed_open_gripper(50)
        if finish:
            RSTATE = 2


# %%
