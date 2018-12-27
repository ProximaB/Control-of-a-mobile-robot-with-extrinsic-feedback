''' Import packages '''
import numpy as np
import cv2 as cv
import math
import copy
import sys
from os.path import normpath

''' Import custom modules '''
# add local path to make interpreter able to obtain custom modules. (when u run  py from glob scope)
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
# load Config
from config import D as CFG
# import Robot class
from robot import Robot

class Settings(object):
    pass


settings = Settings()
settings.thresholds = [{}, {}]

thresholds = settings.thresholds
thresholds[CFG.LEFT_LD] = {'low_red': 0, 'high_red': 255,
                           'low_green': 0, 'high_green': 255,
                           'low_blue': 0, 'high_blue': 255,
                           'low_hue': 0, 'high_hue': 255,
                           'low_sat': 0, 'high_sat': 255,
                           'low_val': 0, 'high_val': 255}

thresholds[CFG.RIGHT_LD] = {'low_red': 0, 'high_red': 255,
                           'low_green': 0, 'high_green': 255,
                           'low_blue': 0, 'high_blue': 255,
                           'low_hue': 0, 'high_hue': 255,
                           'low_sat': 0, 'high_sat': 255,
                           'low_val': 0, 'high_val': 255}

thresholds[CFG.RIGHT_LD] 


print('Green: {}'.format(CFG.LEFT_LD))
thresholds[0]['qswe'] = CFG.RIGHT_LD
print('thresholds: {}'.format(thresholds))
print('setting->thresholds: {}'.format(settings.thresholds))
