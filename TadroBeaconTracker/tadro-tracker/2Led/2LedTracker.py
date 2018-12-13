import numpy as np
import cv2 as cv
import math
from os.path import normpath
import copy

from config import D as Config
from robot import Robot
def init_globals():
    """ 
    Sets up the data we need in the global dictionary D, with is two sets of thresholdings values for two tracked object (leds) green and blue
    The function provides interactive gui for easy tresholding configuration.
    """
    pass

print(Config.__dict__, '\n')

robot = Robot(30, (12,32), np.pi)
robot.print()

Robot(30, (12,32), np.pi/2).print()
Robot(30, (12,32), np.pi*1.2343).print()
Robot(30, (12,32), np.pi*3.2343).print()

import random
random.seed(40)

for i in range(0, 100):
    Robot(random.randint(1,100)/50, (random.randint(1,100)/20,random.randint(1,100)/20), random.randint(1,100)/50.2323).print()


