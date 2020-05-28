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

sticks = []
for i in range(1, 11):
    stick = RealWorld.getFrame("obj{}".format(i))
    stick.setPosition([0+(i/50), -0.3, 0.7+i/50])
    stick.setShape(ry.ST.ssBox, [.05, .15, .05, .01])
    stick.setColor([0.2+ i/20, 0.1, 0.4+i/20])
    stick.setContact(1)
    sticks.append(stick)

#remove some objects
for o in range(11,30):
    name = "obj%i" % o
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

stickobjs =[]
for i in range(10):
    stickobj = C.addFrame("stick{}".format(i))
    # obj.setShape(ry.ST.sphere, [.03])
    stickobj.setShape(ry.ST.ssBox, [.05, .15, .05, .01])
    stickobj.setColor([0.5,0,0.5])
    stickobj.setContact(1)
    stickobj.setPosition([0,0,10+i])
    stickobjs.append(stickobj)

V.setConfiguration(C)

# %%
class RobotProgram1(object):
    def __init__(self, robot):
        self.robot = robot
        self.RSTATE = 2
    def step(self):
        if self.RSTATE == 0:
            pos = [0.2+0.8*np.sin(t/100),0,1]
            finish = self.robot.move_gripper_to_pos("R_gripper", pos)
            if finish:
                self.RSTATE = 3
        elif self.RSTATE == 1:
            pos = [0.5, 0, 1.5]
            finish = self.robot.move_gripper_to_pos("R_gripper", pos)
            if finish:
                self.RSTATE = 3
        elif self.RSTATE == 2:
            finish = self.robot.grasp("R_gripper", "object")
            if finish:
                self.RSTATE = 1
        elif self.RSTATE == 3:
            finish = self.robot.delayed_open_gripper(50)
            if finish:
                self.RSTATE = 2

class RobotProgram2(object):
    def __init__(self, robot):
        self.robot = robot
        self.RSTATE = 0
        self.stick_count = 1
        self.max_sticks = 10
        self.height = 1
    def step(self):
        if self.RSTATE == 0:
            finish = self.robot.grasp("R_gripper", "stick{}".format(self.stick_count))
            if finish:
                self.RSTATE = 1
        if self.RSTATE == 1:
            pos = [0.1, 0.1, self.height]
            finish = self.robot.move_gripper_to_pos("R_gripper", pos)
            if finish:
                self.height += 0.1
                self.stick_count += 1
                self.RSTATE = 2
        elif self.RSTATE == 2:
            finish = self.robot.delayed_open_gripper(50)
            if finish:
                self.RSTATE = 0


# In[7]

sys.path.append('../')
from robot import Robot

robo = Robot(0.01, C, V, S, ry)
#robo_program = RobotProgram1(robo)
robo_program = RobotProgram2(robo)

for t in range(10000):
    # do perception
    if t%10 == 0:
        [rgb, depth] = S.getImageAndDepth()  #we don't need images with 100Hz, rendering is slow
        points = S.depthData2pointCloud(depth, fxfypxpy)
       
        # skipping perception
        p_obj = targetObj.getPosition()   
        r_obj = targetObj.getQuaternion()
        obj.setPosition(p_obj)
        obj.setQuaternion(r_obj)

        for i in range(10):
            p_obj = sticks[i].getPosition()   
            r_obj = sticks[i].getQuaternion()
            stickobjs[i].setPosition(p_obj)
            stickobjs[i].setQuaternion(r_obj)

        V.recopyMeshes(C)
        V.setConfiguration(C)
    
    # do state update
    robo_program.step()


# %%


# %%