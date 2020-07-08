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
scene_file = '../models/connect_4_scenario.g'

# In[2]

# -------------------------------------------------------------
# create simulation world
# -------------------------------------------------------------

#Let's edit the real world before we create the simulation
RealWorld = ry.Config()
#RealWorld.addFile(pandas_model_file)
#RealWorld.addFile(connect_4_model_file)
#RealWorld.addFile(connect_4_sphere_file)
#RealWorld.addFile(ball_ramp_file)
RealWorld.addFile(scene_file)
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
#C.addFile(pandas_model_file)
#C.addFile(connect_4_model_file)
#C.addFile(ball_ramp_file)
C.addFile(scene_file)
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
    sphere = C.getFrame("sphere{}".format(i))
    sphere.setShape(ry.ST.sphere, [.022])
    #sphere.setColor([0,0,1])
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
from game import Game
from strategy import MonteCarloStrategy, get_asynch_human_strategy

# -------------------------------------------------------------

robo = Robot(0.015, C, V, S, ry)
robo_program = RobotConnectFourProgram(robo)

# variables for handling game state and asynchronous user input
waiting_for_input = 0
last_input = [6]
game = Game(MonteCarloStrategy, get_asynch_human_strategy(last_input))

for t in range(10000):

    # do perception every 10th timestep - rendering is slow
    if t%10 == 0:
        [rgb, depth] = S.getImageAndDepth()
        points = S.depthData2pointCloud(depth, fxfypxpy)
        bgr = cv.cvtColor(rgb,cv.COLOR_RGB2BGR)

        # skipping perception
        for i in range(len(sim_spheres)-1):
            p_obj = sim_spheres[i].getPosition()   
            r_obj = sim_spheres[i].getQuaternion()
            perceived_spheres[i].setPosition(p_obj)
            perceived_spheres[i].setQuaternion(r_obj)

        if len(rgb)>0: cv.imshow('OPENCV - rgb', bgr)
        if len(depth)>0: cv.imshow('OPENCV - depth', 0.5* depth)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    # look for user input
    for i in range(0,7): 
        if cv.waitKey(1) == ord(str(i)):
            last_input[0] = i
    print("Input: {}".format(last_input))

    # give the program new sphere id and drop position if needed
    # put new sphere on table if needed
    print("waiting for input {}".format(waiting_for_input))
    if robo_program.need_new_sphere:
        
        
        
        # step the ai - wait for input on the humans turn
        # ------------------------
        if game.player == game.player_2:
            waiting_for_input -= 1
        
        if waiting_for_input == 0 or game.player == game.player_1:
            # strategy from game object
            action = game.step()
            if action is None:
                # Game has been won
                pass
            else:
                robo_program.drop_spot = action
            # constant strategy
            #robo_program.drop_spot = 5
            robo_program.set_sphere_id(robo_program.sphere_id + 1)
            robo_program.need_new_sphere = False
            waiting_for_input = 150

            # after next S.set state this teleports a sphere
            sim_spheres[robo_program.sphere_id+10].setPosition([1.2,0,0.8])
            S.setState(RealWorld.getFrameState())
        # ------------------------
    
    # keep setting drop pos to current user input
    # perception is needed for this
    robo_program.drop_spot = last_input[0]
    
    # do state update
    robo_program.step()

# %%
