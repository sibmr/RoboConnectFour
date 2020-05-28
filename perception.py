import cv2 as cv
import numpy as np

class Perception(object):
    # for segmentation
    depth_background = None
    bgr_background = None
    bgr_background_blur = None
    
    blur = None
    
    # for ball exercise
    vel = 0
    prev_pos = None
    
    def __init__(self):
        self.blur = (lambda img : cv.GaussianBlur(img, (0,0), 0.6,0.6))
       
    def set_background(self,bgr_background, depth_background):
        self.depth_background = depth_background
        self.bgr_background = bgr_background
        self.bgr_background_blur = self.blur(bgr_background)
    
    def set_background_from_sim(self,sim):
        self.set_background(*sim.getImageAndDepth())
    
    def get_object_pixels(self,depth):
        cond = (self.depth_background > depth)
        imgray = (cond*255).astype(np.uint8)
        contours, hierarchy = cv.findContours(imgray,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(bgr, contours, -1, (0,255,0), 3)
        return imgray
    
    def get_unique_colors(self):
        return np.array(
            [
            [0,255,0]
            [255,0,0],
            [255,255,0],
            [255,0,255],
            [0,255,255],
            ])
    
    def segment_bgr(self,bgr):
        opor = np.logical_or
        opand = np.logical_and
        
        diff = cv.absdiff(self.bgr_background_blur, self.blur(bgr))

        flatb = diff.reshape((360*640,3))[:,0]
        flatg = diff.reshape((360*640,3))[:,1]
        flatr = diff.reshape((360*640,3))[:,2]

        cond = opand(flatb!=0, flatg!=0, flatr!=0)

        imgray = np.zeros(360*640, dtype=np.uint8)
        imgray[np.where(cond)[0]] = 255
        imgray = imgray.reshape(360,640)

        contours, hierarchy = cv.findContours(imgray,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(bgr, contours, -1, (0,255,255), 6)

        return bgr
    
    def segment_by_color(self,bgr,mask_bgr):
        hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
        mask_hsv = cv.cvtColor(np.uint8([[mask_bgr]]), cv.COLOR_BGR2HSV)[0,0]
        diff = np.array([10, 80, 80])
        lower = (mask_hsv - diff).clip(min=0)
        upper = (mask_hsv + diff).clip(max=255)
        #imgray = (cv.inRange(hsv, lower, upper)*255).astype(np.uint8)
        imgray = (cv.inRange(hsv, lower, upper))
        
        contours, hierarchy = cv.findContours(imgray,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        bgr = cv.drawContours(bgr, contours, -1, (255,255,0), 3)
        return imgray
    
    def get_image_coordinates_manual(self, depth, bin_img):
        y, x = np.where(bin_img==255)
        z = depth[y,x]
        x = (320-x.reshape((len(x),1)))/f
        y = (180-y.reshape((len(y),1)))/f
        z = z.reshape((len(z),1))
        xyz = np.hstack((x,y,z))
        return xyz
    
    def get_image_coordinates_auto(self, depth, bin_img, fxfypxpy, S):
        x, y = np.where(bin_img==255)
        z = depth[x,y]
        x = x.reshape((len(x),1))
        y = y.reshape((len(y),1))
        z = z.reshape((len(z),1))
        points = S.depthData2pointCloud(depth, fxfypxpy)[x,y]
        
        return points
    
    def get_pc_mean(self, pc, prev_mean=None, use_velocity=0):
        if prev_mean is not None:
            diff = np.linalg.norm(pc-prev_mean, axis=2) 
            
            filter_outliers = np.where(diff<0.06)
            
            #print(pc.shape)
            #print(filter_outliers)
            mean = np.mean(pc[filter_outliers],axis=0)
            
            if np.isnan(mean).any():
                return prev_mean, prev_mean + self.vel*(use_velocity+1)
            else:
                self.vel = prev_mean-mean
                return mean, mean + self.vel*use_velocity
        else:
            return np.mean(pc,axis=0)[0]
