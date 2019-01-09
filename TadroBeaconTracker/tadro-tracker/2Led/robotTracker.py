''' Import packages '''
import numpy as np
import cv2 as cv
import math
import copy
import sys
from os.path import normpath
from functools import partial 
import pickle
from datetime import datetime
import time

''' Import custom modules '''
# add local path to make interpreter able to obtain custom modules. (when u run  py from glob scope)
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
# load Config
from config import D as CFG
# import tracker class
from tracker2Led import Track2Led
# import Robot class
from robot import *
# custom simpl logger
from logger import *
# import utils
from utils import *

class Settings(object):
    pass

class Data(object):
    pass

def setup_thresholds_sliders(SETTINGS):
    """Create windows, and set thresholds, Preview, Threshold_i, Sliders_i, i->[0,1] or more"""
    SETTINGS.thresholds[CFG.LEFT_LD] = {'low_red': 0, 'high_red': 255,
                            'low_green': 0, 'high_green': 255,
                            'low_blue': 0, 'high_blue': 255,
                            'low_hue': 0, 'high_hue': 255,
                            'low_sat': 0, 'high_sat': 255,
                            'low_val': 0, 'high_val': 255}

    SETTINGS.thresholds[CFG.RIGHT_LD] = {'low_red': 0, 'high_red': 255,
                            'low_green': 0, 'high_green': 255,
                            'low_blue': 0, 'high_blue': 255,
                            'low_hue': 0, 'high_hue': 255,
                            'low_sat': 0, 'high_sat': 255,
                            'low_val': 0, 'high_val': 255}

    cv.namedWindow('Preview'); cv.moveWindow('Preview', 0, 0)

    for i in range(len(SETTINGS.thresholds)):
        cv.namedWindow(f'Threshold_{i}')
        if CFG.HALF_SIZE:
            CFG.THR_WIND_OFFSET /= 2

        cv.moveWindow(f'Threshold_{i}', CFG.THR_WIND_OFFSET[0] + (i * CFG.THR_WIND_SLF_OFFSET), CFG.THR_WIND_OFFSET[1])

        cv.namedWindow(f'Sliders_{i}')
        if CFG.HALF_SIZE: 
            CFG.SLD_WIND_OFFSET /= 2

        cv.moveWindow(f'Sliders_{i}', CFG.SLD_WIND_OFFSET[0] + (i * CFG.SLD_WIND_SLF_OFFSET), CFG.SLD_WIND_OFFSET[1])
    
    # pomysł na rejestrowanie sliderow z wykorzystaiem partial
        for thresh_name in SETTINGS.thresholds[i].keys():
           cv.createTrackbar(thresh_name, 'Sliders_%d' % i, SETTINGS.thresholds[i][thresh_name], 255,
           partial(change_slider, SETTINGS.thresholds, i, thresh_name))
    """
    # jeden ze sposobów stworzenia wielu sliderów
        def create_slider_callback(thresholds, i, thresh_name):
            return lambda x: change_slider(thresholds, i, thresh_name, x)

        for thresh_name in thresholds[i].keys():
            cv.createTrackbar(thresh_name, 'Sliders_%d' % i, thresholds[i][thresh_name], 255,
           (lambda x: create_slider_callback(thresholds, i, thresh_name))(i))
           #domknciecie, zachowuje context dla i
    """
    # Set the method to handle mouse button presses
    cv.setMouseCallback('Preview', onMouse, None)
    SETTINGS.last_key_pressed = 255
    #SETTINGS.last_posn = (0,0)
    #SETTINGS.velocity = 40
    
###################### CALLBACK FUNCTIONS #########################

def onMouse(event, x, y, flags, DATA):
    """ Callback dla kliknięcia myszy na okno Previw"""
    # clicked the left button
    if event==cv.EVENT_LBUTTONDOWN: 
        print('X, Y:', x, y, "    ", end=' ')
        (b,g,r) = DATA.processed_image[y,x]
        print('R, G, B: ', int(r), int(g), int(b), "    ", end=' ')
        (h,s,v) = DATA.hsv[y,x]
        print('H, S, V', int(h), int(s), int(v))
        DATA.down_coord = (x,y)

# Function for changing the slider values
def change_slider(thresholds, i, name, new_threshold):
    """ Callback do zmiany wartośći sliderów i wyświetlenia ustawionej wartości w konsoli."""
    thresholds[i][name] = new_threshold
    print('{name}: {val}'.format(name=name, val = thresholds[i][name]))


####################### UTILITY ClASS / FUNCTIONS ##########################


def play_in_loop(capture, frame_counter):
    ''' Here should be explenation how it work'''
    frame_counter+=1
    #If the last frame is reached, reset the capture and the frame_counter
    CV_CAP_PROP_FRAME_COUNT = 7
    if frame_counter != capture.get(CV_CAP_PROP_FRAME_COUNT):
        return False
    
    # pominiecie klatek na początku filmu
    for _ in range(0, CFG.NUM_FRAMES_TO_SKIP):
        capture.grab()
    frame_counter = CFG.NUM_FRAMES_TO_SKIP
    # ustawienie capture na konkretną klatke filmu
    CV_CAP_PROP_POS_FRAMES = 1
    capture.set(CV_CAP_PROP_POS_FRAMES, frame_counter)
    return True

def main():
    # create settings object to store necessary data for further processing, 
    # we'll pass it to fcns later
    #CFG
    #Inicjalizacja obiektów do przechowywania ustawień i danych
    
    SETTINGS = Settings()
    SETTINGS.thresholds = [{}, {}]

    DATA = Data()
    DATA.robot_data = []
    tracker = Track2Led(DATA)

    ROBOT = Robot(0,0,0)

    log_info('Inicjalizacja sliderow do thresholdingu.')
    setup_thresholds_sliders(SETTINGS)

    capture = cv.VideoCapture(CFG.VIDEO_PATH)
    if capture.isOpened() is False:
        log_error("Błąd podczas otwarcia filmu lub inicjalizacji kamery")
        return
    else:
        log_info("Plik został poprawnie otwarty / Kamera zostala poprawnie zainicjalizowana.")

    if (CFG.AUTO_LOAD_THRESHOLDS):
        load_thresholds(SETTINGS.thresholds, CFG.THRESHOLDS_FILE_PATH)

    # pominiecie klatek na początku filmu
    for _ in range(0, CFG.NUM_FRAMES_TO_SKIP):
        capture.grab()

    # prawdziwy numer klatki
    frame_counter = CFG.NUM_FRAMES_TO_SKIP

    while(True):#(capture.isOpened()):
        grabbed, frame = capture.read()
        if not grabbed:
            log_warn('Frame not grabbed. Continue...')
            capture = cv.VideoCapture(CFG.VIDEO_PATH)
            continue
        
        DATA.base_image = frame
        ##################### ROBOT DETECTION AND TRACKING #######################
        #handle_image() wtf?! retval_image -> Rbot([time], postion, heading(orient))
        #nadrzedna klasa robot i podrzeden z dodatkowymi inforamcjami dla szegolengo rodzaju robota z metodami rysowania path i inne dla podklas
        
        tracker.detectAndTrack2LedRobot(SETTINGS, DATA, ROBOT)
        ROBOT.print()
        #################### ROBOT PID CONTROLLING ########################


        ########################### OTHER ACTIONS ################################


        
        #zapis danych ruchu robota,. rejestracja ruchu wtf?!
        #DATA.robot_data.append((frame_counter, DATA.robot_center, DATA.led1_pos, DATA.led2_pos))   
        DATA.robot_data.append(ROBOT)   
        #zwiększenei licznika klatek o jeden
        frame_counter += 1

        # Jeżeli chcemy aby film był przetwarany w pętli, dla celów testowych.
        if CFG.PLAY_IN_LOOP == True:
            if play_in_loop(capture, frame_counter) is True:
                pass

        # pominiętych określonej ilości klatek na cykl
        for _ in range(0, CFG.FRAME_RATE):
            capture.grab()
            frame_counter += 1
        #done abowe
        #increment the frame counter, domyslnie = 0
        #frame_counter += CFG.FRAME_RATE

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    path_img = generate_path_image(DATA)
    #zapis path image na dysk
    file_path = r'C:\Users\barte\Documents\Studia VII\Image_processing\TadroBeaconTracker\tadro-tracker\2Led'
    save_image(path_img, f'RobotPath_' + '{datetime.now():%Y%m%d_%H%M%S}}', file_path)
    capture.release()
    cv.destroyAllWindows()

main()

log_info("Exit")
