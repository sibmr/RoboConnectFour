import numpy as np
from enum import Enum

class RobotState(Enum):
    grasp = 1
    lift = 2
    insert = 3
    drop = 4
    align_pos = 5
    align_z = 6
    going_to_init_q = 7
    idle = 8

class RobotStateMachine(object):
    """
    template for robot state machine
    """
    r_state = 0
    robot = None

    def __init__(self, robot):
        self.robot = robot

    def step(self):
        # start behaviors and change state / await termination
        # also steps physics, updates config/visulization 
        # over robot.optimize_and_update right now
        pass

class RobotProgram1(RobotStateMachine):
    def __init__(self, robot):
        self.robot = robot
        self.r_state = 2
    def step(self, t=0):
        if self.r_state == 0:
            pos = [0.2+0.8*np.sin(t/100),0,1]
            finish = self.robot.move_gripper_to_pos("R_gripper", pos)
            if finish:
                self.r_state = 3
        elif self.r_state == 1:
            pos = [0.5, 0, 1.5]
            finish = self.robot.move_gripper_to_pos("R_gripper", pos)
            if finish:
                self.r_state = 3
        elif self.r_state == 2:
            finish = self.robot.grasp("R_gripper", "object")
            if finish:
                self.r_state = 1
        elif self.r_state == 3:
            finish = self.robot.delayed_open_gripper("R_gripper", 50)
            if finish:
                self.r_state = 2

class RobotProgram2(RobotStateMachine):
    def __init__(self, robot):
        self.robot = robot
        self.RSTATE = 0
        self.stick_count = 1
        self.max_sticks = 10
        self.height = 1
    def step(self):
        if self.RSTATE == 0:
            finish = self.robot.grasp("R_gripper", "stick{}".format(self.stick_count))
            if finish:
                self.RSTATE = 1
        elif self.RSTATE == 1:
            pos = [0.1, 0.1, self.height]
            finish = self.robot.move_gripper_to_pos("R_gripper", pos)
            if finish:
                self.height += 0.1
                self.stick_count += 1
                self.RSTATE = 2
        elif self.RSTATE == 2:
            finish = self.robot.delayed_open_gripper("R_gripper", 50)
            if finish:
                self.RSTATE = 0

class RobotIdleProgram(RobotStateMachine):
    def __init__(self, robot):
        self.robot = robot
        self.RSTATE = 0
    def step(self):
        self.robot.step_simulation()

class RobotConnectFourProgram(RobotStateMachine):
    def __init__(self, robot):
        self.robot = robot
        self.RSTATE = RobotState.going_to_init_q
        self.sphere_id = 0
        self.drop_spot = 0
        self.max_spheres = 24
        self.drop_pos =     [
                            [-0.20, -0.04, 1.2],
                            [-0.14, -0.04, 1.2],
                            [-0.07, -0.04, 1.2],
                            [ 0.00, -0.04, 1.2],
                            [ 0.07, -0.04, 1.2],
                            [ 0.14, -0.04, 1.2],
                            [ 0.20, -0.04, 1.2]
                            ]
        self.need_new_sphere = True

    def step(self):
        if self.RSTATE == RobotState.grasp:
            finish = self.robot.grasp("R_gripper", "sphere{}".format(self.sphere_id))
            if finish:
                self.RSTATE = RobotState.lift
        elif self.RSTATE == RobotState.lift:
            pos = self.drop_pos[self.drop_spot]
            finish = self.robot.lift_gripper_to_z("R_gripper", z=pos[2]+0.0)
            if finish:
                self.RSTATE = RobotState.align_pos
        elif self.RSTATE == RobotState.align_pos:
            pos = self.drop_pos[self.drop_spot]
            finish = self.robot.move_gripper_to_pos("R_gripper", pos=pos, align_vec_z = [0,0,1])
            print("align pos")
            print(self.sphere_id)
            if finish:
                self.need_new_sphere = True
                self.RSTATE = RobotState.drop
        elif self.RSTATE == RobotState.drop:
            finish = self.robot.delayed_open_gripper("R_gripper", delay=100)
            if finish:
                self.RSTATE = RobotState.going_to_init_q
        
        elif self.RSTATE == RobotState.going_to_init_q:
            if not self.sphere_id is None and not self.need_new_sphere:
                self.RSTATE = RobotState.grasp
            else:
                self.robot.go_to_init_q()