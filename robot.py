class Robot():
    
    def __init__(self, tau):
        self.tau = tau
        self.manipulation = Manipulation(tau=tau)
        self.is_closing = False
        
    def optimize(self):
        komo = self.manipulation.komo
        komo.optimize(True)
        end_config = komo.getConfiguration(0)
        C.setFrameState(end_config)
        V.setConfiguration(C)
        q = C.getJointState()
        return q
    
    def step(self, q=None):
        if q is None:
            S.step([], self.tau, ry.ControlMode.none)
        else:
            S.step(q, self.tau, ry.ControlMode.position)
            
    def evaluate_dist(self, obj1, obj2):
        [y,J] = C.evalFeature(ry.FS.positionDiff, [obj1, obj2])
        return y, J
    
    def grasp(self, gripper, obj):
        print("Grasp")
        # The high-level grasp task is only finished when the simulation yields getGripperIsGrasping == True
        while not S.getGripperIsGrasping(gripper):
            time.sleep(self.tau)
            q = S.get_q()
            y, _ = self.evaluate_dist(gripper + "Center", obj)
            # TODO decide between np.linalg.norm(y) and np.abs(y).max()
            if not self.is_closing and np.linalg.norm(y) < 0.02: #np.abs(y).max() < 1e-2:
                print("Closing Gripper")
                S.closeGripper(gripper)
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

robot = Robot(tau=0.01)
robot.grasp("R_gripper", "percept")

