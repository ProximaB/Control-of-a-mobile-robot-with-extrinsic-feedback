from math import sin, cos, tan
import numpy as np
import math
import sys
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
from robot import Robot, Robot2Led, RobotAruco, Robot2LedBicycle
from logger import *
from config import D as CFG

def round_tuple(a):
    #return tuple(map(math.ceil, a))
    return tuple(map(round, a))
class RobotBicycleModel:
    def __init__(self, robot : Robot2LedBicycle, round_pos = 10):
        self.robot = robot
        self.round_pos = round_pos
    
    def simulate_robot(self, Vel, th, time_diff):
        x_pos, y_pos = self.robot.robot_center
        heading = self.robot.heading
        axle_len = self.robot.axle_len
        wheel_radius = self.robot.wheel_radius  
        length = self.robot.length
        theta = self.robot.theta 
        
        theta += th
        if theta > np.pi/2: theta = np.pi/2
        if theta < -np.pi/2: theta = -np.pi/2
        # heading
        heading += Vel / length * tan(theta) * time_diff
        
       # if heading > np.pi: heading = (heading%np.pi)
        #if heading < -np.pi: heading = -(heading%np.pi) #0 - Pi dla kąta w lewo i -Pi, 0 

        self.robot.heading = heading
        log_print(f'heading:{heading}')
        log_print(f'self.robot.robot_center:{self.robot.robot_center}')

        x_pos += Vel * cos(heading) * time_diff # mnoze przez czas, bo calka z predkosci po czasie daje droge
        y_pos += Vel * sin(heading) * time_diff 
        self.robot.robot_center = (x_pos, y_pos)
        self.robot.theta = theta
        self.robot.heading = heading

    def round_robot_properties(self):
        x_pos, y_pos = self.robot.robot_center
        heading = self.robot.heading

        x_pos = round(x_pos, self.round_pos) 
        y_pos = round(y_pos, self.round_pos)
        self.robot.robot_center = (x_pos, y_pos)

        heading = np.round(heading, self.round_pos)
        self.robot.heading = heading

    def simulate_robot_process(self, Vel, theta,  time_diff):
        self.simulate_robot(Vel, theta, time_diff)
class RobotModel2Wheels:
    def __init__(self, robot : Robot, round_pos = 10):
        self.robot = robot
        self.round_pos = round_pos

    def draw_robot(self, x_pos, y_pos, heading):
        pass
    
    #def simulate_path(self, velocity, trun, time_diff):
        # model - > x,y heading
    
    """ def simulate_robot(self, vel_0, vel_1, time_diff):
        x_pos, y_pos = self.robot.robot_center
        heading = self.robot.heading
        axle_len = self.robot.axle_len

        if vel_1 == vel_0:
            log_print(f'heading:{heading}')
            x_pos += sin(heading) * vel_0 * time_diff * 4
            y_pos += cos(heading) * vel_0 * time_diff * 4
            log_print(f'Pozycja w mdl: {sin(-heading) * vel_0 * time_diff}:{cos(-heading) * vel_0 * time_diff}')
            self.robot.robot_center = (x_pos, y_pos)
            return
        #angular_vel = 1/axle_len(vel_0 - vel_1)
        local_axle = 1
        #distance = vel * time_diff
        radius = local_axle / 2.0 * (vel_0 + vel_1) / (vel_1 - vel_0)

        # theta
        heading += (time_diff / local_axle) * (vel_1 - vel_0)
        heading = math.atan2(sin(heading), cos(heading))
        self.robot.heading = heading
        log_print(f'heading:{heading}')
        log_print(f'self.robot.robot_center:{self.robot.robot_center}')

        th = heading
        x_pos += cos(th / 2) * ( 2 * radius * sin(th/2))
        y_pos += sin(th / 2) * ( 2 * radius * sin(th/2))
        self.robot.robot_center = (x_pos, y_pos) """

    def simulate_robot(self, Vl, Vr, time_diff):
        x_pos, y_pos = self.robot.robot_center
        heading = self.robot.heading
        axle_len = self.robot.axle_len
        wheel_radius = self.robot.wheel_radius  
        #angular_vel = 1/axle_len(vel_0 - vel_1)
        #distance = vel * time_diff
        
        # theta
        heading += wheel_radius/axle_len * (Vr - Vl) * time_diff
        heading = math.atan2(sin(heading), cos(heading)) #0 - Pi dla kąta w lewo i -Pi, 0 
        #heading = heading % (2*np.pi)
        self.robot.heading = heading
        log_print(f'heading:{heading}')
        log_print(f'self.robot.robot_center:{self.robot.robot_center}')

        x_pos += wheel_radius/2 * (Vr + Vl) * cos(heading) * time_diff
        y_pos += wheel_radius/2 * (Vr + Vl) * sin(heading) * time_diff
        self.robot.robot_center = (x_pos, y_pos)


    def round_robot_properties(self):
        x_pos, y_pos = self.robot.robot_center
        heading = self.robot.heading

        x_pos = round(x_pos, self.round_pos) 
        y_pos = round(y_pos, self.round_pos)
        self.robot.robot_center = (x_pos, y_pos)

        heading = np.round(heading, self.round_pos)
        self.robot.heading = heading

    def simulate_robot_process(self, vel_0, vel_1, time_diff):
        self.simulate_robot(vel_0, vel_1, time_diff)
        #self.simulate_robot(vel_0, vel_1, time_diff)
        #self.round_robot_properties()
        #self.robot.robot_center = round_tuple(self.robot.robot_center)
        #dead_zones()
        #interpolation_linear()
        #draw_robot()'''
        #pass
        #log_info(f'robot_center: {self.robot.robot_center}')
if __name__ == "__main__":
    """  robot = Robot2Led(0, (0,0), (10,10), (20,20), np.pi/2)
    model = RobotBicycleModel(robot, 10)
    #robot.simulate_robot(20, 20, 10)
    log_print(f"|x_pos:{robot.robot_center[0]}| y_pos:{robot.robot_center[1]}| heading:{robot.heading}|")
    model.simulate_robot_process(10, 0, 1)
    log_print(f"|x_pos:{robot.robot_center[0]}| y_pos:{robot.robot_center[1]}| heading:{robot.heading}|")
    model.simulate_robot_process(0, 0, 10)
    log_print(f"|x_pos:{robot.robot_center[0]}| y_pos:{robot.robot_center[1]}| heading:{robot.heading}|")
    model.simulate_robot_process(-10, 10, 10)
    log_print(f"|x_pos:{robot.robot_center[0]}| y_pos:{robot.robot_center[1]}| heading:{robot.heading}|") 
    """
    #model.simulate_robot_process(5, 1, 10)
    #log_print(f"|x_pos:{robot.robot_center[0]}| y_pos:{robot.robot_center[1]}| heading:{robot.heading}|")

    robot = Robot2LedBicycle(0, CFG.ROB_CNTR, None, None, CFG.HEADING, 0, CFG.LENGTH, CFG.DIAMETER, CFG.AXLE_LEN, CFG.WHEEL_RADIUS)
    model = RobotBicycleModel(robot, 10)
    #robot.simulate_robot(20, 20, 10)
    log_print(f"|x_pos:{robot.robot_center[0]}| y_pos:{robot.robot_center[1]}| heading:{robot.heading}| theta:{robot.theta}|")
    model.simulate_robot_process(5, -np.pi/2, 1)
    log_print(f"|x_pos:{robot.robot_center[0]}| y_pos:{robot.robot_center[1]}| heading:{robot.heading}| theta:{robot.theta}|")
    model.simulate_robot_process(0, 0, 10)
    log_print(f"|x_pos:{robot.robot_center[0]}| y_pos:{robot.robot_center[1]}| heading:{robot.heading}| theta:{robot.theta}|")
    model.simulate_robot_process(-5, -np.pi/2, 1)
    log_print(f"|x_pos:{robot.robot_center[0]}| y_pos:{robot.robot_center[1]}| heading:{robot.heading}| theta:{robot.theta}|")