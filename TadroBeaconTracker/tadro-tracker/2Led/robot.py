import numpy as np
from math import sin, cos
import operator
import math
import sys
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/trackers')
from utils import *

def round_tuple(a):
    #return tuple(map(math.ceil, a))
    return tuple(map(round, a))

def add_t(a, b):
    '''dodanie dwoch punktow, tuple '''
    return tuple(map(operator.add, a, b))

class Robot():
    def __init__(self, time, robot_center, heading, diamater = 10):
        self.time = time if time != None else ''
        self.robot_center = robot_center if robot_center != None else ''
        self.heading = heading if heading != None else ''
        self.diamater = diamater if diamater != None else ''

    def update(self, time, robot_center, heading, diamater):
        self.time = time if time != None else ''
        self.robot_center = robot_center if robot_center != None else ''
        self.heading = heading if heading != None else ''
        self.diamater = diamater if diamater != None else ''

    def print(self):
        try:
            print("|Time: {0:7.3f}, Position: ({1[0]:4}, {1[1]:4}), Heading: {2:7.4f}, {3:6.2f}|"
                .format(self.time, self.robot_center, self.heading, self.heading*180.0/np.pi))
        except Exception as e:
            raise e
    
class Robot2Led(Robot):
    def __init__(self, time, robot_center, led1_pos, led2_pos, heading, diamater=10, axle_len=10, wheel_radius=5):
        self.led1_pos = led1_pos if led1_pos != None else ''
        self.led2_pos = led2_pos if led2_pos != None else ''
        self.axle_len = axle_len
        self.wheel_radius = wheel_radius
        Robot.__init__(self, time, robot_center, heading, diamater)

    def update(self, time, robot_center, led1_pos, led2_pos, heading, diamater=10, wheel_radius=5):
        self.led1_pos = led1_pos if led1_pos != None else ''
        self.led2_pos = led2_pos if led2_pos != None else ''
        self.time = time if time != None else ''
        self.robot_center = robot_center if robot_center != None else ''
        self.heading = heading if heading != None else ''
        self.diamater = diamater if diamater != None else ''
        self.wheel_radius = wheel_radius
    
    def unpack(self):
        return (self.led1_pos, self.led2_pos, self.time, self.robot_center, self.heading, self.diamater, self.axle_len)
    
    def unpackImg(self, hI, hR, wI, wR):
        imgMax = (hI, wI)
        realMax = (hR, wR)

        led1_pos = map_point_to_img(self.led1_pos, imgMax, realMax)
        led2_pos = map_point_to_img(self.led2_pos, imgMax, realMax)
        robot_center = map_point_to_img(self.robot_center, imgMax, realMax)
        diamater = map_real_to_img(self.diamater, imgMax[0], realMax[0])
        axle_len = map_real_to_img(self.axle_len, imgMax[0], realMax[0])

        return (led1_pos, led2_pos, self.time, robot_center, self.heading, diamater, axle_len)
    def calculate_led_pos(self):
        led_1_diff = (sin(-self.heading) * -self.axle_len/2.0, cos(-self.heading) * -self.axle_len/2.0)
        led_2_diff = (sin(-self.heading) * self.axle_len/2.0, cos(-self.heading) * self.axle_len/2.0)
        self.led1_pos = round_tuple(add_t(self.robot_center, led_1_diff))
        self.led2_pos = round_tuple(add_t(self.robot_center, led_2_diff))

class RobotAruco(Robot):
    def __init__(self, time, robot_center, heading, diamater=10, axle_len=10, wheel_radius=5):
        self.axle_len = axle_len
        self.wheel_radius = wheel_radius
        Robot.__init__(self, time, robot_center, heading, diamater)

    def update(self, time, robot_center, heading, diamater=10, wheel_radius=5):
        self.time = time if time != None else ''
        self.robot_center = robot_center if robot_center != None else ''
        self.heading = heading if heading != None else ''
        self.diamater = diamater if diamater != None else ''
        self.wheel_radius = wheel_radius
    
    def unpack(self):
        return (self.time, self.robot_center, self.heading, self.diamater, self.axle_len)
