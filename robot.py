from optimization_objective import OptimizationObjective
import time
import numpy as np

class Robot(object):
    
    def __init__(self, tau, C, V, S, ry):
        """
        store references to global configuration, visualization, simulation and library
        store statfulness for robor behavior

        tau:    simulation time step in seconds
        C:      configuration
        V:      visualization
        S:      simulation
        ry:     library imported elsewhere (may not want to import twice)
        """        
        self.tau = tau
        self.optimization_objective = OptimizationObjective(tau, C, V, S, ry)
        self.C = C
        self.V = V
        self.S = S
        self.ry = ry

        # statefulness and constants for behavior functions
        self.is_opening = False
        self.is_closing = False
        self.gripper_open_delay = 0
        self.gripper_width_threshold = 1e-3 # TODO tbd

        self.init_q = self.S.get_q()
        
    def optimize_and_update(self):
        """
        call komo to optimize for objectives currently set in self.optimization_objective
        update configuration and display

        return: new robot configuration
        """
        komo = self.optimization_objective.komo
        komo.optimize(True)
        end_config = komo.getConfiguration(0)
        self.C.setFrameState(end_config)
        self.V.setConfiguration(self.C)
        q = self.C.getJointState()
        return q
    
    def step_simulation(self, q=None):
        """
        step simulation, 
        optionally with new robot configuration as control sinal

        q:  state in joint space as control signal
        """
        if q is None:
            self.S.step([], self.tau, self.ry.ControlMode.none)
        else:
            self.S.step(q, self.tau, self.ry.ControlMode.position)
            
    def evaluate_dist(self, obj1, obj2):
        """
        return: vector difference of the positions of obj1 and obj2
        """
        [y,J] = self.C.evalFeature(self.ry.FS.positionDiff, [obj1, obj2])
        return y, J

    def lift_gripper_to_z(self, gripper, z):
        """
        gripper:    gripper that will be moved
        z:          z position to move the gripper to
        return:     0 if behavior has not terminated,
                    else return integer indicating status of behavior or behavior termination
        """
        print("Lift")
        self.optimization_objective.clear()
        stepsize = 0.1
        pos, _ = self.C.evalFeature(self.ry.FS.position, [gripper + "Center"])
        diff = z-pos[2]
        height = z*0.7
        if pos[2]< height:
            normdiff = diff/np.linalg.norm(diff)
            pos[2] = pos[2] + normdiff*stepsize
            self.move_gripper_to_pos(gripper, pos=pos, movement_priority=2e3)
        else:
            height = 0
            pos[2] = z
            return self.move_gripper_to_pos(gripper, pos=pos, align_vec_z=[0,0,1], align_vec_y=[-1,0,0], movement_priority=4e3) 

    def move_gripper_to_pos(self, gripper, pos, align_vec_z=None, align_vec_y=None, rel_to_object=None, movement_priority=5e3, alignment_priority=3e3):
        """
        gripper:    gripper that will be moved
        pos:        position to move the gripper to
        return:     0 if behavior has not terminated,
                    else return integer indicating status of behavior or behavior termination
        """
        print("Move")
        
        self.optimization_objective.clear()

        obj_pos = np.array([0,0,0])
        if rel_to_object:
            obj_pos, _ = self.C.evalFeature(self.ry.FS.position, [rel_to_object])
        
        q = self.S.get_q()
        diff, _ = self.C.evalFeature(self.ry.FS.position, [gripper + "Center"])
        diff -= np.array(obj_pos+pos)
        dist = np.linalg.norm(diff)
        if alignment_priority < 0:
            align_prio = min(-alignment_priority*(0.2/dist)**3, -alignment_priority)
        else:
            align_prio = alignment_priority 

        if dist < 0.01:
            return True
        
        self.optimization_objective.move_to_position(gripper, obj_pos + pos, align_vec_z=align_vec_z, align_vec_y=align_vec_y, movement_priority=movement_priority, alignment_priority=align_prio)
        q = self.optimize_and_update()
        self.step_simulation(q)
        return False

    def grasp(self, gripper, obj=None, align_vec_z = None, align_vec_y = None):
        """
        gripper:    gripper that will be grasping
        obj:        object that will be grasped
        return:     0 if behavior has not terminated, 
                    else return integer indicating status of behavior or behavior termination
        """
        print("Grasp")
        # The high-level grasp task is only finished when the simulation yields getGripperIsGrasping == True
        
        self.optimization_objective.clear()

        if self.S.getGripperIsGrasping(gripper):
            self.is_closing = False 
            return True
        q = self.S.get_q()
        # TODO decide between np.linalg.norm(y) and np.abs(y).max()
        if obj is not None:
            y, _ = self.evaluate_dist(gripper + "Center", obj)
            if not self.is_closing and np.linalg.norm(y) < 0.02: #np.abs(y).max() < 1e-2:
                print("Closing Gripper")
                self.S.closeGripper(gripper, speed=2.0)
                self.is_closing = True # Avoid that closeGripper() is called multiple times
        else:
            if not self.is_closing: #np.abs(y).max() < 1e-2:
                print("Closing Gripper")
                self.S.closeGripper(gripper, speed=2.0)
                self.is_closing = True # Avoid that closeGripper() is called multiple times
            

        if obj is not None:
            self.optimization_objective.grasp(gripper, obj, align_vec_z = align_vec_z, align_vec_y=align_vec_y)
            q = self.optimize_and_update()
            self.step_simulation(q)
        else:
            self.step_simulation(q)
        # When exiting the loop getGripperIsGrasping is true, so the closing progress is finished
        
            
    def delayed_open_gripper(self, gripper, delay):
        """
        gripper:    gripper that is currently grasping
        delay:      time to wait for after releasing the object
        return:     0 if behavior has not terminated, 
                    else return integer indicating status of behavior or behavior termination
                    in this case 1 indicates termination
        """
        self.optimization_objective.clear()
        print("Open")
        self.S.openGripper(gripper)
        self.gripper_open_delay += 1
        self.step_simulation()
        if self.gripper_open_delay == delay:
            self.gripper_open_delay = 0
            return True
        return False

    def go_to_init_q(self, threshold=1):
        """
        let the robot move to the initial joint configuration

        threshold:  the threshold euclidean distance in joint space where this action returns the termination flag
        return:     0 if behavior has not terminated, 
                    else return integer indicating status of behavior or behavior termination
                    in this case 1 indicates termination
        """

        self.optimization_objective.clear()

        dist = np.linalg.norm(self.init_q-self.S.get_q())
        if dist < threshold:
            return True 
        
        self.optimization_objective.go_to_q(self.init_q)
        q = self.optimize_and_update()
        self.step_simulation(q)
        return False

    def go_to_handover(self):
        """
        let the robot arms go into a handover position, where both arms have the object between their grippers
        """
        self.optimization_objective.clear()

        y, _ = self.evaluate_dist("R_gripperCenter", "L_gripperCenter")
        
        dist = np.linalg.norm(y)
        if dist < 0.02:
            return True
        
        self.optimization_objective.go_to_handover(alignment_prio=4e2*(0.04/dist))
        q = self.optimize_and_update()
        self.step_simulation(q)

        return False
        
