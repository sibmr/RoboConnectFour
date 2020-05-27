from manipulation import Manipulation
import time
import numpy as np

class Robot(object):
    
    def __init__(self, tau, C, V, S, ry):
        self.tau = tau
        self.manipulation = Manipulation(tau=tau)
        self.is_closing = False
        self.C = C
        self.V = V
        self.S = S
        self.ry = ry
        
    def optimize(self):
        komo = self.manipulation.komo
        komo.optimize(True)
        end_config = komo.getConfiguration(0)
        self.C.setFrameState(end_config)
        self.V.setConfiguration(self.C)
        q = self.C.getJointState()
        return q
    
    def step(self, q=None):
        if q is None:
            self.S.step([], self.tau, self.ry.ControlMode.none)
        else:
            self.S.step(q, self.tau, self.ry.ControlMode.position)
            
    def evaluate_dist(self, obj1, obj2):
        [y,J] = self.C.evalFeature(self.ry.FS.positionDiff, [obj1, obj2])
        return y, J
    
    def grasp(self, gripper, obj):
        print("Grasp")
        # The high-level grasp task is only finished when the simulation yields getGripperIsGrasping == True
        while not self.S.getGripperIsGrasping(gripper):
            time.sleep(self.tau)
            q = self.S.get_q()
            y, _ = self.evaluate_dist(gripper + "Center", obj)
            # TODO decide between np.linalg.norm(y) and np.abs(y).max()
            if not self.is_closing and np.linalg.norm(y) < 0.02: #np.abs(y).max() < 1e-2:
                print("Closing Gripper")
                self.S.closeGripper(gripper)
                self.is_closing = True # Avoid that closeGripper() is called multiple times
            self.manipulation.clear()  
            self.manipulation.grasp(gripper, obj)
            q = self.optimize()
            self.step(q)
        # When exiting the loop getGripperIsGrasping is true, so the closing progress is finished
        self.is_closing = False 
            
    def open_gripper(self):
        # TODO this is sketched code and needs work
        print("Open")
        while not m.open():
            time.sleep(self.tau)
            self.step()

