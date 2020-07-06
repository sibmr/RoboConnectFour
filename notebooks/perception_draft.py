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

p = perception.Perception(f)

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
        rgb = cv.rotate(rgb, cv.ROTATE_180)
        depth = cv.rotate(depth, cv.ROTATE_180)

        if gaussian_blur:
            rgb = cv.GaussianBlur(rgb, (5,5), 1, 1)
        dim = depth.shape
        depth_grid = depth[round(dim[0]/2), round(dim[1]/2)]
        background_rgb = rgb
        diff_bool = (np.abs(depth-depth_grid) < 1e-7)
        diff_gray = diff_bool.astype(np.uint8) * 255
        #diff_gray = cv.GaussianBlur(diff_gray, (3,3), 1, 1)

        contours,hierarchy = cv.findContours(diff_gray, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        contour = max(contours, key = cv.contourArea)
        x,y,w,h = cv.boundingRect(contour)
        rgb_grid = np.zeros(rgb.shape,np.uint8)
        rgb_grid[y:y+h,x:x+w] = rgb[y:y+h,x:x+w]
        cv.rectangle(rgb,(x,y),(x+w,y+h),(0,255,0),2)
               
        img_seg_red = p.segment_color(rgb_grid, [255,0,0])
        img_seg_blue = p.segment_color(rgb_grid, [0,0,255])
        center_lst_seg_red = p.erode(img_seg_red)
        center_lst_seg_blue = p.erode(img_seg_blue)
        p.draw_circles(rgb_grid, center_lst_seg_red, color=(255,0,0))
        p.draw_circles(rgb_grid, center_lst_seg_blue, color= (0,0,255))

        points = S.depthData2pointCloud(depth, fxfypxpy)
        cameraFrame.setPointCloud(points, rgb)
        V.recopyMeshes(C)
        V.setConfiguration(C)
            
        if len(rgb)>0:
            cv.imshow('OPENCV - rgb', cv.cvtColor(rgb, cv.COLOR_RGB2BGR))
        if len(rgb)>0:
            cv.imshow('OPENCV - rgb_grid', cv.cvtColor(rgb_grid, cv.COLOR_RGB2BGR))
        if len(depth)>0:
            cv.imshow('OPENCV - red', img_seg_red)
        if len(depth)>0:
            cv.imshow('OPENCV - blue', img_seg_blue)
        #if len(depth)>0:
        #    cv.imshow('OPENCV - depth', 0.5* depth)
        #if len(diff_gray)>0:
        #    cv.imshow('OPENCV - gray', diff_gray)

        if cv.waitKey() & 0xFF == ord('q'):
            break
            
    S.step([], tau, ry.ControlMode.none)