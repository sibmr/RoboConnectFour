# In[1]

import sys
sys.path.append('../../robotics-course/build')
sys.path.append('../../robotics-course/scenarios/build')
import cv2 as cv
import numpy as np
import libry as ry
import time
print(cv.__version__)

connect_4_model_file = "../models/connect_4_6x7_simple.g"
connect_4_sphere_file = "../models/connect_4_balls_simple.g"
ball_ramp_file = "../models/ball_ramp_conv.g"
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
RealWorld.addFile(ball_ramp_file)
V = ry.ConfigurationViewer()
V.setConfiguration(RealWorld)

# In[3]

# -------------------------------------------------------------
# manage objects in the simulation world
# -------------------------------------------------------------

# set contacts for models in the scene
# TODO check if we need to do this for RealWorld
for i in range(1,12):
    RealWorld.getFrame("connect4_coll{}".format(i)).setContact(1)

sim_spheres = []
for i in range(1,25):
    sphere = RealWorld.getFrame("sphere{}".format(i))
    sphere.setContact(1)
    sim_spheres.append(sphere)

for i in range(1,6):
    RealWorld.getFrame("ball_ramp{}".format(i)).setContact(1)

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
C.addFile(ball_ramp_file)
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


for i in range(1,11):
    C.getFrame("connect4_coll{}".format(i)).setContact(1)

for i in range(1,6):
    C.getFrame("ball_ramp{}".format(i)).setContact(1)

perceived_spheres =[]
for i in range(1,len(sim_spheres)):
    sphere = C.addFrame("sphere{}".format(i))
    sphere.setShape(ry.ST.sphere, [.022])
    sphere.setColor([0,0,1])
    sphere.setContact(1)
    sphere.setPosition([0,0,10+i])
    perceived_spheres.append(sphere)

for t in range(100):
    q = S.get_q()
    S.step([], 0.01, ry.ControlMode.none)

sys.path.append('..')
import perception

points = []
tau = .01
gaussian_blur = True

for t in range(10):
    time.sleep(0.01)
    
    #grab sensor readings from the simulation
    q = S.get_q()
    if t%10 == 0:
        # Prepare image
        [rgb, depth] = S.getImageAndDepth()  #we don't need images with 100Hz, rendering is slow
        perception.Perception.detect_grid_state(rgb, depth)

        points = S.depthData2pointCloud(depth, fxfypxpy)
        cameraFrame.setPointCloud(points, rgb)
        V.recopyMeshes(C)
        V.setConfiguration(C)

        if cv.waitKey() & 0xFF == ord('q'):
            break
            
    S.step([], tau, ry.ControlMode.none)