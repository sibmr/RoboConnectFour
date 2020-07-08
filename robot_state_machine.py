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
    move_above_object = 9
    go_to_handover = 10
    receive = 11
    release = 12
    goto_q_before_handover = 13


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
        self.pickup_pos_red = [6.16610706e-01, 3.63965373e-04, 6.93810999e-01]
        self.pickup_pos_blue = [-6.16570711e-01, -3.49139242e-04,  6.93794310e-01]
        self.drop_pos =     [
                            [-0.205,-0.05, 1.2],
                            [-0.137,-0.05, 1.2],
                            [-0.07, -0.05, 1.2],
                            [ 0.00, -0.05, 1.2],
                            [ 0.07, -0.05, 1.2],
                            [ 0.137,-0.05, 1.2],
                            [ 0.205,-0.05, 1.2]
                            ]
        self.need_new_sphere = True
        self.receiving_gripper = "L_gripper"
        self.gripper_with_sphere = "R_gripper"
        self.sphere_name = None

    def set_sphere_id(self, sphere_id, mode=1):
        self.sphere_id = sphere_id
        if mode == 0:
            self.sphere_name = "sphere{}".format(self.sphere_id)
        else:
            if self.sphere_id % 2 == 1:
                self.sphere_name = "sphere_red"
            else:
                self.sphere_name = "sphere_blue"

    def step(self):
        # initq -> move above object -> grasp -> lift 
        # if drop_spot > 2: -> handover
        # -> align_pos -> drop -> initq
        if self.RSTATE == RobotState.going_to_init_q:
            if not self.sphere_id is None and not self.need_new_sphere:
                self.RSTATE = RobotState.move_above_object
            else:
                self.robot.go_to_init_q(threshold=0)
        elif self.RSTATE == RobotState.move_above_object:
            finish = self.robot.move_gripper_to_pos(self.gripper_with_sphere, pos=[0,0,0.3], align_vec_z = [0,0,1], align_vec_y = [-1,0,0], rel_to_object=self.sphere_name)
            if finish:
                self.RSTATE = RobotState.grasp
        elif self.RSTATE == RobotState.grasp:
            finish = self.robot.grasp(self.gripper_with_sphere, self.sphere_name, align_vec_z = [0,0,1], align_vec_y=[-1,0,0])
            if finish:
                self.RSTATE = RobotState.lift
        elif self.RSTATE == RobotState.lift:
            pos = self.drop_pos[self.drop_spot]
            finish = self.robot.lift_gripper_to_z(self.gripper_with_sphere, z=pos[2]+0.0)
            if finish:
                if self.drop_spot > 2 and self.gripper_with_sphere == "R_gripper":
                    self.RSTATE = RobotState.align_pos
                elif self.drop_spot < 3 and self.gripper_with_sphere == "L_gripper":
                    self.RSTATE = RobotState.align_pos
                else:
                    self.RSTATE = RobotState.goto_q_before_handover
        elif self.RSTATE == RobotState.align_pos:
            pos = self.drop_pos[self.drop_spot]
            finish = self.robot.move_gripper_to_pos(self.gripper_with_sphere, pos=pos, align_vec_z = [0,0,1], align_vec_y=[-1,0,0], alignment_priority=-1e3)
            print("align pos")
            print(self.sphere_id)
            if finish:
                self.need_new_sphere = True
                self.RSTATE = RobotState.drop
        elif self.RSTATE == RobotState.drop:
            finish = self.robot.delayed_open_gripper(self.gripper_with_sphere, delay=100)
            if finish:
                self.gripper_with_sphere, self.receiving_gripper = self.receiving_gripper, self.gripper_with_sphere
                self.RSTATE = RobotState.going_to_init_q
        # ------------------------------------------------------------------------------
        # handover states
        elif self.RSTATE == RobotState.goto_q_before_handover:
            finish = self.robot.go_to_init_q()
            if finish:
                self.RSTATE = RobotState.go_to_handover
        elif self.RSTATE == RobotState.go_to_handover:
            finish = self.robot.go_to_handover()
            if finish:
                self.RSTATE = RobotState.receive
        elif self.RSTATE == RobotState.receive:
            finish = self.robot.grasp(self.receiving_gripper, self.sphere_name)
            if finish:
                self.RSTATE = RobotState.release
        elif self.RSTATE == RobotState.release:
            finish = self.robot.delayed_open_gripper(self.gripper_with_sphere, delay=100)
            if finish:
                self.gripper_with_sphere, self.receiving_gripper = self.receiving_gripper, self.gripper_with_sphere
                self.RSTATE = RobotState.align_pos
        # ------------------------------------------------------------------------------
