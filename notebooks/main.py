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
pandas_model_file = '../scenarios/pandasTable.g'
ghost_sphere_file = '../models/connect_4_ghost_sphere.g'
scene_file_sim = '../models/connect_4_scenario_mirror_sim.g'
scene_file_conf = '../models/connect_4_scenario_mirror_conf.g'
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
RealWorld.addFile(scene_file_sim)
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
for i in range(1,67):
    sphere = RealWorld.getFrame("sphere{}".format(i))
    sphere.setContact(1)
    sim_spheres.append(sphere)

#for i in range(1,6):
#    RealWorld.getFrame("ball_ramp{}".format(i)).setContact(1)

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
C.addFile(scene_file_conf)
#V = ry.ConfigurationViewer()
V.setConfiguration(C)
cameraFrame = C.frame("camera")

# In[6]

# -------------------------------------------------------------
# add objects for perceived world
# -------------------------------------------------------------


for i in range(1,11):
    C.getFrame("connect4_coll{}".format(i)).setContact(1)

#for i in range(1,6):
#    C.getFrame("ball_ramp{}".format(i)).setContact(1)

V.setConfiguration(C)

def set_fence_color(color, corners=False):
    k = 7
    if corners:
        k = 11
    for i in range(1,k):
        RealWorld.getFrame(f"fence{i}").setColor(color)
        S.setState(RealWorld.getFrameState())
        

# In[7]

# -------------------------------------------------------------
# Main perception-manipulation loop
# -------------------------------------------------------------

sys.path.append('../')
from robot import Robot
from robot_state_machine import RobotConnectFourProgram
from game import Game
from strategy import MonteCarloStrategy, MinMaxStrategy, AsyncHumanStrategy
from perception import Perception

# -------------------------------------------------------------
tau = 0.015
robo = Robot(tau, C, V, S, ry)
robo_program = RobotConnectFourProgram(robo)

# variables for handling game state and asynchronous user input
waiting_for_input = 0
last_input = [6] # Human input initialization should be arbitrary existing column (0-6)
human_player = False
#human_player = input("Is there a human player (y/n)") == "y"
player_won = None
if human_player:
    game = Game(MonteCarloStrategy, AsyncHumanStrategy, selfstate=False)
    human_player = game.player_2
else:
    game = Game(MonteCarloStrategy, MinMaxStrategy, selfstate=False)
    human_player = None

timestep = 0
while last_input != 7: # Human can quit by pressing 0

    # do perception every 20th timestep - rendering is slow
    if timestep % 20 == 0: # rendering period = 20*timestep = 20*0.015s = 0.3s
        [rgb, depth] = S.getImageAndDepth()
        grid = Perception.detect_grid_state(rgb, depth)
        game.set_grid(grid)

    #if human_player is not None:
    # look for user input
    usr_in = cv.waitKey(1)
    for i in range(0,8):
        if  usr_in == ord(str(i)):
            last_input = 6-(i-1)
            print("Input set: {}".format(last_input))
            human_player.user_input = last_input

    # give the program new sphere id and drop position if needed
    # put new sphere on table if needed
    if waiting_for_input != 0:
        print("Waiting for input {}".format(waiting_for_input))
    if robo_program.need_new_sphere:
        # step the ai - wait for input on the humans turn
        # ------------------------
        if waiting_for_input > 0:
            waiting_for_input -= 1
        
        if waiting_for_input == 0 or game.player == game.player_1:
            if not game.next_move:
                # Only execute next game step if previous operation is executed and perceived
                print("Waiting for turn to be executed")
            else:
                action = game.step()
                if action is None:
                    # Game is finished
                    # The Player from the previous turn is the winner
                    player_won = game.player_2.player if game.player.player==game.player_1.player else game.player_1.player
                    robo_program.game_won(player_won, game.player_1.player)
                else:
                    # Not finished, next turn
                    robo_program.drop_spot = action

                # Count how many spheres have been dropped in the grid
                robo_program.set_sphere_id(robo_program.sphere_id + 1)
                robo_program.need_new_sphere = False
                
                # reset waiting counter if there is a human player
                if human_player is not None: waiting_for_input = 100
                if human_player is None: waiting_for_input = 25

                # after next S.set state this teleports a sphere
                if game.player == game.player_1:
                    sim_spheres[robo_program.sphere_id+22].setPosition([1.2,0,0.8])
                else:
                    sim_spheres[robo_program.sphere_id+22].setPosition([-1.2,0,0.8])
                S.setState(RealWorld.getFrameState())
            # ------------------------
    
    # whacky color changes
    if player_won is not None:
        if timestep % 8 > 3:
            if player_won == game.player_1.player:
                set_fence_color([1,0,0], corners=True)
            else:
                set_fence_color([0,0,1], corners=True)
        else:
            set_fence_color([.3,.3,.3])

    # keep setting drop pos to current user input
    # perception is needed for this
    if game.player == game.player_1 and human_player:
        robo_program.drop_spot = last_input
    
    # do state update
    robo_program.step()

    timestep += 1
# %%
