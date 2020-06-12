class OptimizationObjective(object):
    
    def __init__(self, tau, C, V, S, ry):
        """
        store references to global configuration, visualization, simulation and library
        initialize new komo one-step path

        tau:    simulation time step in seconds
        C:      configuration
        V:      visualization
        S:      simulation
        ry:     library imported elsewhere (may not want to import twice)
        """
        self.tau = tau
        self.C = C
        self.V = V
        self.S = S
        self.ry = ry
        
        self.komo = C.komo_path(1.0, 1, self.tau, True)
        
    def clear(self):
        """
        reset komo one-step path optimiation objectives
        """
        # TODO: reinitialization may not be necessary if resetting anyways
        self.komo = self.C.komo_path(1.0, 1, self.tau, True)
        self.komo.clearObjectives()
        self.komo.add_qControlObjective(order=1, scale=1)
    
    def grasp(self, gripper, obj):
        """
        constraints gripping specified object with specified gripper
        """
        ry = self.ry
        self.komo.addObjective([1.], ry.FS.positionDiff, [gripper+"Center",obj], ry.OT.sos, [1e3])
        #self.komo.addObjective([1.], ry.FS.positionDiff, [gripper, obj], ry.OT.sos, [1e2])
        self.komo.addObjective([1.], ry.FS.vectorZ, [gripper], ry.OT.sos, [1e2], target=[0,0,1])
        #self.komo.addObjective([1.], ry.FS.scalarProductXZ, [obj,gripper], ry.OT.sos, [1e2])
        self.komo.addObjective([1.], ry.FS.scalarProductXY, [obj,gripper], ry.OT.sos, [1e2])
        self.komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.ineq, [1e2])
        self.komo.addObjective([1.], ry.FS.qItself, [], ry.OT.sos, [2e1], order=1)
        #self.komo.addObjective([1.], ry.FS.qItself, [], ry.OT.sos, [3e1])
        self.komo.addObjective([], ry.FS.qItself, ["R_finger1"], ry.OT.eq, [1e1], order=1)
        self.komo.addObjective([], ry.FS.qItself, ["R_finger2"], ry.OT.eq, [1e1], order=1)
            
    def go_to_object(self, gripper, obj):
        ry = self.ry
        # TODO make go_to_object() more general than grasp()
        self.komo.addObjective([1.], ry.FS.positionDiff, [gripper,obj], ry.OT.sos, [1e3])
        #self.komo.addObjective([1.], ry.FS.positionDiff, ["R_gripperCenter", "percept"], ry.OT.sos, [1e2])
        self.komo.addObjective([1.], ry.FS.vectorZ, [gripper], ry.OT.sos, [1e2], target=[0,0,1])
        self.komo.addObjective([1.], ry.FS.scalarProductXZ, [obj,gripper], ry.OT.sos, [1e2])
        self.komo.addObjective([1.], ry.FS.scalarProductXY, [obj,gripper], ry.OT.sos, [1e2])
        self.komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.ineq, [1e2])
        self.komo.addObjective([1.], ry.FS.qItself, [], ry.OT.sos, [1e3], order=1)
        self.komo.addObjective([], ry.FS.qItself, ["R_finger1"], ry.OT.eq, [1e1], order=1)

    def move_to_position(self, gripper, pos, align_vec_z = None):
        """
        constraints for moving the gripper center of specified gripper to specified position
        """
        ry = self.ry
        if align_vec_z:
            self.komo.addObjective([1.], ry.FS.vectorZ, [gripper], ry.OT.sos, [1e2], target=align_vec_z)
        self.komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.ineq, [1e2])
        self.komo.addObjective([1.], ry.FS.position, [gripper + "Center"], ry.OT.sos, [1e3], target=pos)
        self.komo.addObjective([1.], ry.FS.qItself, [], ry.OT.sos, [2e1], order=1)
        #self.komo.addObjective([1.], ry.FS.qItself, [], ry.OT.sos, [3e1]);
        self.komo.addObjective([], ry.FS.qItself, ["R_finger1"], ry.OT.eq, [1e1], order=1)
        self.komo.addObjective([], ry.FS.qItself, ["R_finger2"], ry.OT.eq, [1e1], order=1)