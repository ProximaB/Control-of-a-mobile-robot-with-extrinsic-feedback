import sys
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

class BicyclePCtrl:
    def __init__(self, pid1 : PID, pid2 : PID, ROBOT : RobotBicycleModel):
        self.PID1 = pid1
        self.PID2 = pid2
    
    getControl(PID1, PID2, ROBOT)