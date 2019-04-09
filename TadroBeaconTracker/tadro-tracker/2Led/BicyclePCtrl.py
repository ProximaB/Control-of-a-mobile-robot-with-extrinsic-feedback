import numpy as np
import sys
import math
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/trackers')
# custom simpl logger
from logger import *
# import utils
from utils import *
# import PID 
from PID import PID

sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/Symulator')
# models
from RobotModel2Wheels import RobotBicycleModel

sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
# load Config
from config import D as CFG

class BicyclePCtrl:
    def __init__(self, pid1 : PID, pid2 : PID, ROBOT : RobotBicycleModel):
        self.PID1 = pid1
        self.PID2 = pid2

    def getControl(self, PID1_output_theta, PID2_output_dist):
        vel = 0.5 * PID2_output_dist + 10
        theta = 0.3 * PID1_output_theta 
        return (vel, theta)

class DiffCtrl:
    def __init__(self, pid1 : PID, pid2 : PID, ROBOT : RobotBicycleModel):
        self.PID1 = pid1
        self.PID2 = pid2
        self.Vel = CFG.VEL

    def getControl(self, PID1_output_theta, PID2_output_dist, DATA, ROBOT):
        h, w = DATA.base_image.shape[:2]
        p = math.sqrt(h**2 + w**2)
        outTheta = PID1_output_theta.output
        outVel = float(PID2_output_dist.output/p * self.Vel)
        outVel = outVel if outVel < self.Vel else self.Vel
        
        available_area_rect = [(ROBOT.diamater, ROBOT.diamater//2), (CFG.AREA_WIDTH_REAL - ROBOT.diamater, CFG.AREA_HEIGHT_REAL - ROBOT.diamater//2)]
        x0,y0 = available_area_rect[0]
        x1, y1 = available_area_rect[1]
        x, y = ROBOT.robot_center

        if (y0 < y < y1 and x0 < x < x1 or done_heading):
            vel_1 = outVel * cos(-outTheta)
            vel_2 = outVel * sin(-outTheta)
            #vel_1 = -(2*outVel - outTheta * CFG.AXLE_LEN )/ 2*CFG.WHEEL_RADIUS
            #vel_2 = -(2*outVel + outTheta * CFG.AXLE_LEN )/ 2*CFG.WHEEL_RADIUS
            if((y0< y < y1 and x0< x < x1)):
                done_heading = False
        else:
            #vel_1 = outVel*0.5; vel_2 = -outVel*0.5
            vel_1 = 0; vel_2=0
            #wasDrawn = False
            if abs(heading_error) > 20*np.pi/180:
                #vel_1 = outVel*0.5; vel_2 = outVel*0.5
                vel_1 = outVel*0.5; vel_2 = -outVel*0.5
                done_heading = True              
        return (PID2_output_dist, PID1_output_theta)

if __name__ == "__main__":
    ctrl = BicyclePCtrl(None, None, None)
    vel, theta = ctrl.getControl(30, np.pi/2)
    print(f'vel: {vel}, theta: {theta}')