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
from scipy.interpolate import interp1d
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
# import statusWindow
from statusWindow import statusWindow
# import PID 
from PID import PID as pid

sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/Symulator')
# sim
from robotSimulator import *

class Settings(object):
    pass

class Data(object):
    pass

class TrackerBootstrap:
    def __init__(self, SETTINGS, DATA):
        self.SETTINGS = SETTINGS
        self.DATA = DATA

    def setup_thresholds_sliders(self):
        SETTINGS = self.SETTINGS
        DATA = self.DATA

        """Create windows, and set thresholds, Tracing and Recognition., Threshold_i, Sliders_i, i->[0,1] or more"""
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

        cv.namedWindow('Tracing and Recognition.'); cv.moveWindow('Tracing and Recognition.', 0, 0)

        #cv.createTrackbar('Slider_heading', 'Tracing and Recognition.', DATA.targetHeading, 360, self.change_heading,)
        cv.createTrackbar('0 : OFF \n1 : ON','Tracing and Recognition.',0,1, self.switch)
        
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
                    partial(self.change_slider, SETTINGS.thresholds, i, thresh_name))
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
        cv.setMouseCallback('Tracing and Recognition.', self.onMouse, None)
        SETTINGS.last_key_pressed = 255
        #SETTINGS.last_posn = (0,0)
        #SETTINGS.velocity = 40
        
    ###################### CALLBACK FUNCTIONS #########################

    def onMouse(self, event, x, y, flags, param):
        """ Callback dla kliknięcia myszy na okno Previw"""
        # clicked the left button
        if event==cv.EVENT_LBUTTONDOWN: 
            self.DATA.target = (x,y)
            print('X, Y:', x, y, "    ", end=' ')
            (b,g,r) = self.DATA.processed_image[y,x]
            print('R, G, B: ', int(r), int(g), int(b), "    ", end=' ')
            (h,s,v) = self.DATA.hsv[y,x]
            print('H, S, V', int(h), int(s), int(v))
            self.DATA.down_coord = (x,y)


    # Function for changing the slider values
    def change_slider(self, thresholds, i, name, new_threshold):
        """ Callback do zmiany wartośći sliderów i wyświetlenia ustawionej wartości w konsoli."""
        thresholds[i][name] = new_threshold
        print('{name}: {val}'.format(name=name, val = thresholds[i][name]))

    def change_heading(self, new_heading):
        targetHeading = new_heading * np.pi/180.0
        self.DATA.targetHeading = targetHeading
        print(f'targetHeading: {new_heading}')

    def switch(self, onOff):
        self.SETTINGS.START = onOff
        print(f'Settings.START: {onOff}')
    ####################### UTILITY ClASS / FUNCTIONS ##########################

    def play_in_loop(self, capture, frame_counter):
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

def main_default():
    # create settings object to store necessary data for further processing, 
    # we'll pass it to fcns later
    #CFG
    #Inicjalizacja obiektów do przechowywania ustawień i danych

    SETTINGS = Settings()
    SETTINGS.thresholds = [{}, {}]

    DATA = Data()
    DATA.robot_data = []
    DATA.target = (0,0)
    DATA.targetHeading = 0

    tracker = Track2Led(DATA)
    trackerBootstap = TrackerBootstrap(SETTINGS, DATA)
    

    ROBOT = Robot2Led(0,(0,0),0,0,0)

    #PID = PID(CFG.PROPORTIONAL, CFG.INTEGRAL, CFG.DERIVATIVE)

    log_info('Inicjalizacja sliderow do thresholdingu.')
    trackerBootstap.setup_thresholds_sliders()

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
        """Transformacja affiniczna dla prostokąta, określającego pole roboczese ###############"""
        # Zrobiona w juptyer lab

        """################## ROBOT DETECTION AND TRACKING ######################"""
        #detectAndTrack2LedRobot()  retval_image -> Rbot([time], postion, heading(orient))
        #nadrzedna klasa robot i podrzeden z dodatkowymi inforamcjami dla szegolengo rodzaju robota z metodami rysowania path i inne dla podklas      
        tracker.detectAndTrack2LedRobot(SETTINGS, DATA, ROBOT)

        """###################### ROBOT PID CONTROLLING #########################"""

         #PID = DATA.target
         
        """######################## OTHER ACTIONS ###############################"""
        #zapis danych ruchu robota,. rejestracja ruchu wtf?!
        #DATA.robot_data.append((frame_counter, DATA.robot_center, DATA.led1_pos, DATA.led2_pos))   

        sw = statusWindow('Status')
        error = math.hypot(DATA.target[0] - ROBOT.robot_center[0], DATA.target[1] - ROBOT.robot_center[1])
        heading_error = ROBOT.heading - math.atan2(ROBOT.robot_center[1]-DATA.target[1], ROBOT.robot_center[0]-DATA.target[0])
        sw.drawData(ROBOT.robot_center, ROBOT.heading, error, heading_error)
        #ROBOT.print()
        DATA.robot_data.append(ROBOT)   

        #zwiększenei licznika klatek o jeden
        frame_counter += 1

        # Jeżeli chcemy aby film był przetwarany w pętli, dla celów testowych.
        if CFG.PLAY_IN_LOOP == True:
            if trackerBootstap.play_in_loop(capture, frame_counter) is True:
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

def main_simulation():
    # create settings object to store necessary data for further processing, 
    # we'll pass it to fcns later
    #CFG
    #Inicjalizacja obiektów do przechowywania ustawień i danych
    SETTINGS = Settings()
    SETTINGS.thresholds = [{}, {}]
    SETTINGS.START = 0

    DATA = Data()
    DATA.robot_data = []
    DATA.target = (0,0)
    DATA.targetHeading = 0
    tracker = Track2Led(DATA)
    trackerBootstap = TrackerBootstrap(SETTINGS, DATA)

    ROBOT = Robot2Led(0,(0,0),0,0,0)
    simRobot = Robot2Led(20, (500, 300), (500, 480), (500, 520), 0, 75, 50, 5)
    model = RobotModel2Led(simRobot)
    sim = robotSimulationEnv(model)

    PID1 = pid(CFG.PROPORTIONAL1, CFG.INTEGRAL1, CFG.DERIVATIVE1)
    PID2 = pid(CFG.PROPORTIONAL2, CFG.INTEGRAL2, CFG.DERIVATIVE2)
    
    log_info('Inicjalizacja sliderow do thresholdingu.')
    trackerBootstap.setup_thresholds_sliders()

    if (CFG.AUTO_LOAD_THRESHOLDS):
        load_thresholds(SETTINGS.thresholds, CFG.THRESHOLDS_FILE_PATH)

    frame = sim.simulate_return_image(-2,0,2)
    PID1.SetPoint = 0
    PID1.setSampleTime(0.01)
    PID1.update(0)
    
    PID2.SetPoint = 0
    PID2.setSampleTime(0.01)
    PID2.update(0)
    Vel = CFG.VEL
    while(True):#(capture.isOpened()):
        if SETTINGS.START == 0:
            frame = sim.simulate_return_image(0,0)
            DATA.base_image = frame
            tracker.detectAndTrack2LedRobot(SETTINGS, DATA, ROBOT)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        outTheta = PID1.output
        outVel = float(PID2.output/1000*Vel)

        vel_1 = outVel * cos(-outTheta)
        vel_2 = outVel * sin(-outTheta)

        frame = sim.simulate_return_image(vel_1,vel_2)
        
        DATA.base_image = frame
        """Transformacja affiniczna dla prostokąta, określającego pole roboczese ###############"""
        # Zrobiona w juptyer lab

        """################## ROBOT DETECTION AND TRACKING ######################"""
        #detectAndTrack2LedRobot()  retval_image -> Rbot([time], postion, heading(orient))
        #nadrzedna klasa robot i podrzeden z dodatkowymi inforamcjami dla szegolengo rodzaju robota z metodami rysowania path i inne dla podklas      
        tracker.detectAndTrack2LedRobot(SETTINGS, DATA, ROBOT)

        """###################### ROBOT PID CONTROLLING #########################"""
        error = math.hypot(DATA.target[0] - ROBOT.robot_center[0], DATA.target[1] - ROBOT.robot_center[1])
        heading_error = ROBOT.heading - np.pi - math.atan2(ROBOT.robot_center[1]-DATA.target[1], ROBOT.robot_center[0]-DATA.target[0])
        heading_error = -1 * math.atan2(math.sin(heading_error), math.cos(heading_error))
        #if (error < CFG.SIM_ERROR and heading_error < 0.2): Vel = 0
        #else: Vel = CFG.VEL
        print(f'error:{error}')
        print(f'heading_error:{heading_error}')
        #else: V = 5.1  
        PID1.update(heading_error)
        PID2.update(error)
        """######################## OTHER ACTIONS ###############################"""
        #zapis danych ruchu robota,. rejestracja ruchu wtf?!
        #DATA.robot_data.append((frame_counter, DATA.robot_center, DATA.led1_pos, DATA.led2_pos))   

        sw = statusWindow('Status')
        
        #heading_error = ROBOT.heading - np.arctan2(DATA.target[0] - ROBOT.robot_center[0], ROBOT.robot_center[1] - DATA.target[1])
        sw.drawData(ROBOT.robot_center, ROBOT.heading, error, heading_error)
        #ROBOT.print()
        DATA.robot_data.append(ROBOT)   

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    path_img = generate_path_image(DATA)
    #zapis path image na dysk
    file_path = r'C:\Users\barte\Documents\Studia VII\Image_processing\TadroBeaconTracker\tadro-tracker\2Led'
    save_image(path_img, f'RobotPath_' + '{datetime.now():%Y%m%d_%H%M%S}}', file_path)
    cv.destroyAllWindows() 
if __name__ == '__main__':
    main_simulation()
log_info("Exit")
