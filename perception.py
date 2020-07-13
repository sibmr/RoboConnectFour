import cv2 as cv
import numpy as np

class Perception(object):
"""
    This class is a perception toolbox to extract the connect 4 game state.
    All methods are static and the class has no members.
    Therefore, the class works as library for convenient usage.
"""

    @staticmethod
    def get_object_pixels(depth, depth_background):
        cond = (depth_background > depth)
        imgray = (cond*255).astype(np.uint8)
        contours, hierarchy = cv.findContours(imgray,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(rgb, contours, -1, (0,255,0), 3)
        return imgray

    @staticmethod
    def segment_rgb(rgb):
        opor = np.logical_or
        opand = np.logical_and
        rgb_blur = cv.GaussianBlur(rgb, (5,5), 1, 1)
        diff = cv.absdiff(rgb_background_blur, rgb_blur)

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

    @staticmethod
    def detect_grid_state(rgb, depth, display=True):
        # Flip image to match perspective of robot arms
        rgb = cv.flip(rgb, flipCode=1)
        # Gaussian Blur to increase robustness of algorithms
        rgb = cv.GaussianBlur(rgb, (5,5), 1, 1)
        # Find region of interest for grid
        x,y,w,h = Perception.extract_roi(depth)
        rgb_grid = np.zeros(rgb.shape, dtype=np.uint8)
        rgb_grid[y:y+h,x:x+w] = rgb[y:y+h,x:x+w]
        # Extract circular objects
        center_lst_red, center_blue_lst = Perception.extract_circles(rgb_grid, strategy=Perception.erode)
        # Infer grid state from circle centers
        grid = Perception.get_grid_state_from_centers(center_lst_red, center_blue_lst, x, y, w, h)

        if display:
            if len(rgb)>0:
                cv.rectangle(rgb,(x,y),(x+w,y+h),(0,255,0),2)
                cv.imshow('OPENCV - rgb', cv.cvtColor(rgb, cv.COLOR_RGB2BGR))
            if len(rgb)>0:
                Perception.draw_circles(rgb_grid, center_lst_red, color=(255,0,0))
                Perception.draw_circles(rgb_grid, center_blue_lst, color= (0,0,255))
                cv.imshow('7-- OPENCV - rgb_grid --1', cv.cvtColor(rgb_grid, cv.COLOR_RGB2BGR))

        return grid

    @staticmethod
    def calc_cell_from_pixel(center, x, y, w, h, grid_width, grid_height):
        # Helper method to calculate grid cell from pixel position
        grid_x = ((center[0] - w*0.05 - x) / (w*0.9) - 1.0/grid_width/2.0) * grid_width
        grid_x = int(np.round(grid_x))
        grid_y = ((center[1] - h*0.24 - y) / (h * 0.73) - 1.0/grid_height/2.0) * grid_height
        grid_y = grid_height - int(np.round(grid_y)) - 1
        return grid_x, grid_y

    @staticmethod
    def get_grid_state_from_centers(center_red_lst, center_blue_lst, x, y, w, h):
        # Transform pixel coordinates into grid cell occupancy
        grid_width = 7
        grid_height = 6
        grid = np.zeros((grid_width, grid_height), dtype=np.uint8)
        for center_red in center_red_lst:
            grid_x, grid_y = Perception.calc_cell_from_pixel(center_red, x, y, w, h, grid_width, grid_height)
            if grid_x < grid_width and grid_y < grid_height:
                grid[grid_x, grid_y] = 1
            else:
                print("Invalid position detected: (" + str(grid_x) + "|" + str(grid_y) + ")")
        for center_blue in center_blue_lst:
            grid_x, grid_y = Perception.calc_cell_from_pixel(center_blue, x, y, w, h, grid_width, grid_height)
            if grid_x < grid_width and grid_y < grid_height:
                grid[grid_x, grid_y] = 2
            else:
                print("Invalid position detected: (" + str(grid_x) + "|" + str(grid_y) + ")")        
                
        return grid

    @staticmethod
    def extract_roi(depth):
        # Find region of interest in image center based on depth information
        dim = depth.shape
        depth_grid = depth[round(dim[0]/2), round(dim[1]/2)]
        diff_bool = (np.abs(depth-depth_grid) < 1e-7)
        diff_gray = diff_bool.astype(np.uint8) * 255
        # Fit a rectangle around the largest contour
        contours, hierarchy = cv.findContours(diff_gray, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        contour = max(contours, key = cv.contourArea)
        x,y,w,h = cv.boundingRect(contour)
        return x,y,w,h

    @staticmethod
    def extract_circles(img, strategy, display=False):
        # Return blue and red circular objects from image
        img_seg_red = Perception.segment_color(img, [255,0,0])
        img_seg_blue = Perception.segment_color(img, [0,0,255])
        if display:
            if len(img_seg_red)>0:
                cv.imshow('OPENCV - red', img_seg_red)
            if len(img_seg_blue)>0:
                cv.imshow('OPENCV - blue', img_seg_blue)
        center_lst_seg_red = strategy(img_seg_red, display=False)
        center_lst_seg_blue = strategy(img_seg_blue, display=False)
        return center_lst_seg_red, center_lst_seg_blue

    @staticmethod
    def segment_color(rgb, mask_rgb):
        # Segment image by color
        hsv = cv.cvtColor(rgb, cv.COLOR_RGB2HSV)
        mask_hsv = cv.cvtColor(np.uint8([[mask_rgb]]), cv.COLOR_RGB2HSV)[0,0]
        diff = np.array([30, 100, 100])
        lower = (mask_hsv - diff).clip(min=0)
        upper = (mask_hsv + diff).clip(max=255)
        imgray = (cv.inRange(hsv, lower, upper))
        return imgray

    @staticmethod
    def erode(imgray, iterations=3, display=False):
        # Combine morphological operations to reduce segmented image to separate clusters
        kernel_erode = np.ones((3,3),np.uint8)
        kernel_open = np.ones((3,9),np.uint8)

        for i in range(3):
            imgray = cv.erode(imgray, kernel_erode, iterations=1)
            imgray = cv.morphologyEx(imgray, cv.MORPH_OPEN, kernel_open)
            imgray = cv.morphologyEx(imgray, cv.MORPH_OPEN, kernel_open)

        contours, hierarchy = cv.findContours(imgray,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        if display:
            imgray_disp = imgray.copy()
            if len(imgray_disp)>0:
                cv.imshow('OPENCV - erode', imgray_disp)
        center_lst = []
        for contour in contours:
            M = cv.moments(contour)
            try:
                center_lst.append([M["m10"] / M["m00"], M["m01"] / M["m00"], 10])
            except ZeroDivisionError:
                # Contour is only one point, use that point
                contour_x_y = contour[0][0]
                center_lst.append([contour_x_y[0], contour_x_y[1], 10])

        return center_lst

    @staticmethod
    def hough(imgray):
        # Use circle hough transformation to detect circular objects
        circles = cv.HoughCircles(imgray,cv.HOUGH_GRADIENT,1,18,
                            param1=150,param2=10,minRadius=8,maxRadius=15)
        center_lst = []
        if circles is not None:
            center_lst = circles[0]
        return center_lst

    @staticmethod
    def draw_circles(img, circle_lst, color=(0,255,0)):
        # Draw list of circles onto image
        for i in circle_lst:
            cv.circle(img,(int(i[0]),int(i[1])),int(i[2]),color,2)
    
    @staticmethod
    def get_image_coordinates_manual(f, depth, bin_img):
        y, x = np.where(bin_img==255)
        z = depth[y,x]
        x = (320-x.reshape((len(x),1))) / f
        y = (180-y.reshape((len(y),1))) / f
        z = z.reshape((len(z),1))
        xyz = np.hstack((x,y,z))
        return xyz
    
    @staticmethod
    def get_image_coordinates_auto(depth, bin_img, fxfypxpy, S):
        x, y = np.where(bin_img==255)
        z = depth[x,y]
        x = x.reshape((len(x),1))
        y = y.reshape((len(y),1))
        z = z.reshape((len(z),1))
        points = S.depthData2pointCloud(depth, fxfypxpy)[x,y]
        return points
    
    @staticmethod
    def get_pc_mean(pc, vel, prev_mean=None, use_velocity=0):
        if prev_mean is not None:
            diff = np.linalg.norm(pc-prev_mean, axis=2)
            filter_outliers = np.where(diff<0.06)
            mean = np.mean(pc[filter_outliers],axis=0)
            
            if np.isnan(mean).any():
                return prev_mean, prev_mean + vel*(use_velocity+1)
            else:
                vel = prev_mean-mean
                return mean, mean + vel*use_velocity
        else:
            return np.mean(pc,axis=0)[0]
