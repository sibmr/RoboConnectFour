import numpy as np

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
        self.RSTATE = 0
        self.sphere_count = 1
        self.max_spheres = 24
        self.drop_pos =     [
                            [-0.20, -0.04, 1],
                            [-0.14, -0.04, 1],
                            [-0.07, -0.04, 1],
                            [ 0.00, -0.04, 1],
                            [ 0.07, -0.04, 1],
                            [ 0.14, -0.04, 1],
                            [ 0.20, -0.04, 1]
                            ]
        self.need_new_sphere = True

    def step(self):
        if self.RSTATE == 0:
            finish = self.robot.grasp("R_gripper", "sphere{}".format(self.sphere_count))
            if finish:
                self.RSTATE = 1
        elif self.RSTATE == 1:
            pos = self.drop_pos[0]
            finish = self.robot.move_gripper_to_pos("R_gripper", pos, align_vec_z = [0,0,1])
            if finish:
                self.sphere_count += 1
                self.need_new_sphere = True
                self.RSTATE = 2
        elif self.RSTATE == 2:
            finish = self.robot.delayed_open_gripper("R_gripper", 50)
            if finish:
                self.RSTATE = 0