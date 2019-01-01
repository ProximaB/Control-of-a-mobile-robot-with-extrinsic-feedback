''' Import packages '''
import numpy as np
import cv2 as cv
import math
import copy
import sys
from os.path import normpath
from functools import partial 

''' Import custom modules '''
# add local path to make interpreter able to obtain custom modules. (when u run  py from glob scope)
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
# load Config
from config import D as CFG
# import Robot class
from robot import Robot

class Settings(object):
    pass

class Data(object):
    pass

def setup_thresholds_sliders(thresholds : dict, data : object):
    """Create windows, and set thresholds, Preview, Threshold_i, Sliders_i, i->[0,1] or more"""
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

    cv.namedWindow('Preview'); cv.moveWindow('Preview', 0, 0)

    for i in range(len(thresholds)):
        cv.namedWindow(f'Threshold_{i}')
        if CFG.HALF_SIZE:
            CFG.THR_WIND_OFFSET /= 2

        cv.moveWindow(f'Threshold_{i}', CFG.THR_WIND_OFFSET[0] + (i * CFG.THR_WIND_SLF_OFFSET), CFG.THR_WIND_OFFSET[1])

        cv.namedWindow(f'Sliders_{i}')
        if CFG.HALF_SIZE: 
            CFG.SLD_WIND_OFFSET /= 2

        cv.moveWindow(f'Sliders_{i}', CFG.SLD_WIND_OFFSET[0] + (i * CFG.SLD_WIND_SLF_OFFSET), CFG.SLD_WIND_OFFSET[1])

        print('Green: {}'.format(CFG.LEFT_LD))
        thresholds[0]['Test'] = CFG.RIGHT_LD
        print('thresholds: {}'.format(thresholds[0]['Test']))
        print('setting->thresholds: {}'.format(thresholds[0]['Test']))

        for thresh_name in thresholds[i].keys():
           cv.createTrackbar(thresh_name, 'Sliders_%d' % i, thresholds[i][thresh_name], 255,
           partial(change_slider, thresholds, i, thresh_name))

    # Set the method to handle mouse button presses
    cv.setMouseCallback('Preview', onMouse, data)

    # We have not created our "scratchwork" images yet
    created_images = False

    # Variable for key presses
    last_key_pressed = 255

    last_posn = (0,0)
    velocity = 40

###################### CALLBACK FUNCTIONS #########################

def onMouse(event, x, y, flags, data):
    """ the method called when the mouse is clicked """
    # clicked the left button
    if event==cv.EVENT_LBUTTONDOWN: 
        print("x, y are", x, y, "    ", end=' ')
        (b,g,r) = data.image[y,x]
        print("r,g,b is", int(r), int(g), int(b), "    ", end=' ')
        (h,s,v) = data.hsv[y,x]
        print("h,s,v is", int(h), int(s), int(v))
        data.down_coord = (x,y)

# Function for changing the slider values
def change_slider(thresholds, i, name, new_threshold):
    """ a small function to change a slider value """
    thresholds[i][name] = new_threshold
    print('{name}: {val}'.format(name=name, val = thresholds[i][name]))
def main():
    # create settings object to store necessary data for further processing, we'll pass it to fcns
    SETTINGS = Settings()
    SETTINGS.thresholds = [{}, {}]

    DATA = Data()

    setup_thresholds_sliders(SETTINGS.thresholds, DATA)

main()
cv.waitKey(0)
print("[INFO] Exited")
