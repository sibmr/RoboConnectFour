# In[1]

import sys
sys.path.append('../../robotics-course/build')
sys.path.append('../../robotics-course/scenarios/build')
import cv2 as cv
import numpy as np
import libry as ry
import time
print(cv.__version__)

connect_4_model_file = "../models/connect_4_6x7.g"
connect_4_sphere_file = "../models/connect_4_balls.g"
pandas_model_file = '../../robotics-course/scenarios/pandasTable.g'

# In[2]

# -------------------------------------------------------------
# create simulation world
# -------------------------------------------------------------

#Let's edit the real world before we create the simulation
RealWorld = ry.Config()
RealWorld.addFile(pandas_model_file)
RealWorld.addFile(connect_4_model_file)
RealWorld.addFile(connect_4_sphere_file)
V = ry.ConfigurationViewer()
V.setConfiguration(RealWorld)

# In[3]

# -------------------------------------------------------------
# manage objects in the simulation world
# -------------------------------------------------------------

# set contacts for models in the scene
# TODO check if we need to do this for RealWorld
for i in range(1,121):
    RealWorld.getFrame("connect4_coll{}".format(i)).setContact(1)

sim_spheres = []
for i in range(1,25):
    sphere = RealWorld.getFrame("sphere{}".format(i))
    sphere.setContact(1)
    sim_spheres.append(sphere)

V.recopyMeshes(RealWorld)
V.setConfiguration(RealWorld)

# In[4]

# -------------------------------------------------------------
# create camera for perceiving the simulation world
# -------------------------------------------------------------

# instantiate the simulation
S = RealWorld.simulation(ry.SimulatorEngine.physx, True)
S.addSensor("camera")

# In[5]

# -------------------------------------------------------------
# create and configure perceived world
# -------------------------------------------------------------

# create your model world
C = ry.Config()
C.addFile(pandas_model_file)
C.addFile(connect_4_model_file)
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

# -------------------------------------------------------------
# add objects for perceived world
# -------------------------------------------------------------


for i in range(1,121):
    C.getFrame("connect4_coll{}".format(i)).setContact(1)

perceived_spheres =[]
for i in range(len(sim_spheres)):
    sphere = C.addFrame("sphere{}".format(i))
    sphere.setShape(ry.ST.sphere, [.022])
    sphere.setColor([0,0,1])
    sphere.setContact(1)
    sphere.setPosition([0,0,10+i])
    perceived_spheres.append(sphere)


V.setConfiguration(C)

# In[7]

# -------------------------------------------------------------
# Main perception-manipulation loop
# -------------------------------------------------------------

sys.path.append('../')
from robot import Robot
from robot_state_machine import RobotConnectFourProgram

robo = Robot(0.01, C, V, S, ry)
robo_program = RobotConnectFourProgram(robo)

for t in range(10000):

    # do perception every 10th timestep - rendering is slow
    if t%10 == 0:
        [rgb, depth] = S.getImageAndDepth()
        points = S.depthData2pointCloud(depth, fxfypxpy)
       
        # skipping perception
        for i in range(len(sim_spheres)):
            p_obj = sim_spheres[i].getPosition()   
            r_obj = sim_spheres[i].getQuaternion()
            perceived_spheres[i].setPosition(p_obj)
            perceived_spheres[i].setQuaternion(r_obj)

        V.recopyMeshes(C)
        V.setConfiguration(C)
    
    # put new sphere on table if needed
    print(robo_program.need_new_sphere)
    if robo_program.need_new_sphere:
        # this does not move sphere
        # TODO find out how to move sphere in sim
        sim_spheres[robo_program.sphere_count].setPosition([0,-0.2,0.8])
        robo_program.need_new_sphere = False

    # do state update
    robo_program.step()

# %%
