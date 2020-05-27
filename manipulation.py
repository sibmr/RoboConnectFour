class Manipulation:
    
    def __init__(self, tau, C, V, S, ry):
        self.C = C
        self.V = V
        self.S = S
        self.ry = ry
        
        self.tau = tau
        self.komo = C.komo_path(1.0, 1, self.tau, True)
        self.opening = False
        self.gripper_width_threshold = 1e-3 # TODO tbd
        
    def clear(self):
        self.komo = self.C.komo_path(1.0, 1, self.tau, True)
        self.komo.clearObjectives()
        self.komo.add_qControlObjective(order=1, scale=1)
    
    def grasp(self, gripper, obj):
        ry = self.ry
        self.komo.addObjective([1.], ry.FS.positionDiff, [gripper,obj], ry.OT.sos, [1e3]);
        #self.komo.addObjective([1.], ry.FS.positionDiff, [gripper, obj], ry.OT.sos, [1e2]);
        self.komo.addObjective([1.], ry.FS.vectorZ, [gripper], ry.OT.sos, [1e2], target=[0,0,1]);
        self.komo.addObjective([1.], ry.FS.scalarProductXZ, [obj,gripper], ry.OT.sos, [1e2]);
        self.komo.addObjective([1.], ry.FS.scalarProductXY, [obj,gripper], ry.OT.sos, [1e2]);
        self.komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.ineq, [1e2])
        self.komo.addObjective([1.], ry.FS.qItself, [], ry.OT.sos, [1e1], order=1);
        self.komo.addObjective([], ry.FS.qItself, ["R_finger1"], ry.OT.eq, [1e1], order=1)
           
    def open_gripper(self):
        # TODO this is sketched code and needs work
        if not self.opening:
            self.S.openGripper("R_gripper")
            self.opening = True
        return self.S.getGripperWidth("R_gripper") < self.gripper_width_threshold
            
    def go_to_object(self, gripper, obj):
        ry = self.ry
        # TODO make go_to_object() more general than grasp()
        self.komo.addObjective([1.], ry.FS.positionDiff, [gripper,obj], ry.OT.sos, [1e3]);
        #self.komo.addObjective([1.], ry.FS.positionDiff, ["R_gripperCenter", "percept"], ry.OT.sos, [1e2]);
        self.komo.addObjective([1.], ry.FS.vectorZ, [gripper], ry.OT.sos, [1e2], target=[0,0,1]);
        self.komo.addObjective([1.], ry.FS.scalarProductXZ, [obj,gripper], ry.OT.sos, [1e2]);
        self.komo.addObjective([1.], ry.FS.scalarProductXY, [obj,gripper], ry.OT.sos, [1e2]);
        self.komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.ineq, [1e2])
        self.komo.addObjective([1.], ry.FS.qItself, [], ry.OT.sos, [1e3], order=1);
        self.komo.addObjective([], ry.FS.qItself, ["R_finger1"], ry.OT.eq, [1e1], order=1)
