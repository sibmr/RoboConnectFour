import cv2 as cv
import numpy as np

class Perception(object):
    # for segmentation
    depth_background = None
    rgb_background = None
    rgb_background_blur = None
    
    blur = None
    
    # for ball exercise
    vel = 0
    prev_pos = None
    
    def __init__(self, f):
        self.f = f
        #self.blur = (lambda img : cv.GaussianBlur(img, (0,0), 0.6,0.6))
       
    def set_background(self,rgb_background, depth_background):
        self.depth_background = depth_background
        self.rgb_background = rgb_background
        self.rgb_background_blur = self.blur(rgb_background)
    
    #def set_background_from_sim(self,sim):
    #    self.set_background(*sim.getImageAndDepth())
    
    def get_object_pixels(self,depth):
        cond = (self.depth_background > depth)
        imgray = (cond*255).astype(np.uint8)
        contours, hierarchy = cv.findContours(imgray,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(rgb, contours, -1, (0,255,0), 3)
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
    
    def segment_rgb(self,rgb):
        opor = np.logical_or
        opand = np.logical_and
        
        diff = cv.absdiff(self.rgb_background_blur, self.blur(rgb))

        flatb = diff.reshape((360*640,3))[:,0]
        flatg = diff.reshape((360*640,3))[:,1]
        flatr = diff.reshape((360*640,3))[:,2]

        cond = opand(flatb!=0, flatg!=0, flatr!=0)

        imgray = np.zeros(360*640, dtype=np.uint8)
        imgray[np.where(cond)[0]] = 255
        imgray = imgray.reshape(360,640)

        contours, hierarchy = cv.findContours(imgray,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(rgb, contours, -1, (0,255,255), 6)

        return rgb
    
    def segment_color(self, rgb, mask_rgb):
        hsv = cv.cvtColor(rgb, cv.COLOR_RGB2HSV)
        mask_hsv = cv.cvtColor(np.uint8([[mask_rgb]]), cv.COLOR_RGB2HSV)[0,0]
        diff = np.array([30, 100, 100])
        lower = (mask_hsv - diff).clip(min=0)
        upper = (mask_hsv + diff).clip(max=255)
        #imgray = (cv.inRange(hsv, lower, upper).astype(np.uint8))*255
        imgray = (cv.inRange(hsv, lower, upper))
        return imgray

    def erode(self, imgray, iterations=5):
        #imgray = cv.GaussianBlur(imgray, (3,3), 1, 1)
        kernel = np.ones((3,3),np.uint8)
        imgray = cv.erode(imgray,kernel,iterations=iterations)
        contours, hierarchy = cv.findContours(imgray,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        center_lst = []
        for contour in contours:
            M = cv.moments(contour)
            center_lst.append([M["m10"] / M["m00"], M["m01"] / M["m00"], 10])
        #rgb = cv.drawContours(rgb, contours, -1, (255,255,0), 3)
        return center_lst

    def hough(self, imgray):
        circles = cv.HoughCircles(imgray,cv.HOUGH_GRADIENT,1,18,
                            param1=150,param2=10,minRadius=8,maxRadius=15)
        center_lst = []
        if circles is not None:
            center_lst = circles[0]
        return center_lst

    def draw_circles(self, img, circle_lst, color=(0,255,0)):
        for i in circle_lst:
            cv.circle(img,(int(i[0]),int(i[1])),int(i[2]),color,2)
    
    def get_image_coordinates_manual(self, depth, bin_img):
        y, x = np.where(bin_img==255)
        z = depth[y,x]
        x = (320-x.reshape((len(x),1)))/self.f
        y = (180-y.reshape((len(y),1)))/self.f
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
