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
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.interpolate import BSpline, make_interp_spline #  Switched to BSpline
from skimage import exposure
''' Import custom modules '''
# add local path to make interpreter able to obtain custom modules. (when u run  py from glob scope)
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
# load Config
from config import D as CFG

sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/trackers')
# import tracker class
from tracker2Led import Track2Led
from trackerArruco import TrackArruco
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
        cv.setMouseCallback('Tracing and Recognition.', self.onMouse, DATA)
        SETTINGS.last_key_pressed = 255
        #SETTINGS.last_posn = (0,0)
        #SETTINGS.velocity = 40
        
    ###################### CALLBACK FUNCTIONS #########################

    def onMouse(self, event, x, y, flags, param):
        """ Callback dla kliknięcia myszy na okno Previw"""
        # clicked the left button
        if event==cv.EVENT_LBUTTONDOWN:
            h,w,c = param.base_image.shape 
            xR = map_img_to_real(x, w, CFG.AREA_WIDTH_REAL)
            yR = map_img_to_real(y, h, CFG.AREA_HEIGHT_REAL)
            self.DATA.target = (xR,yR)
            print('X, Y:', xR, yR, "    ", end=' ')
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

def draw_plot(feedback_list, setpoint_list, time_list, title, id):
    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)

    # feedback_smooth = spline(time_list, feedback_list, time_smooth)
    # Using make_interp_spline to create BSpline
    helper_x3 = make_interp_spline(time_list, feedback_list)
    feedback_smooth = helper_x3(time_smooth)

    L = len(time_list)
    f = plt.figure(id)
    plt.plot(time_smooth, feedback_smooth)
    plt.plot(time_list, setpoint_list)
    #plt.xlim((0, L))
    #plt.ylim((min(feedback_list)-0.5, max(feedback_list)+0.5))
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title(title)

    #plt.ylim((1-0.5, 1+0.5))

    plt.grid(True)
    return f

def warp_iamge_aruco(image, DATA):
    orig = image.copy()
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    gray = cv.bilateralFilter(gray, 15, 15, 15)
    #gray = exposure.rescale_intensity(gray, out_range=(0, 255))
    
    aruco_dict = aruco.Dictionary_get(CFG.ARUCO_DICT)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if len(corners) < 4: 
       if len(DATA.prevCorners) < 4:
           h,w,c = orig.shape
           return orig, h, w
       corners = DATA.prevCorners

    subs = 0
    if(len(DATA.prevCorners) != 0):
        for i in range(4): 
            x, y = sub_t(corners[i][0][0], DATA.prevCorners[i][0][0])
            subs += math.sqrt(x**2 + y**2)
        if subs < 30:
           corners = DATA.prevCorners
        else:
            print("Movement affected affine trans.")

    DATA.prevCorners = corners
    preview = aruco.drawDetectedMarkers(image, corners)
    cv.imshow('Preview markers detect', preview)

    #genPts = (v[0][0] for v in corners)
    genPts = []
    for i in range(4): # range(len(corners)):
        genPts.append(corners[i][0][i])
    pts = np.stack(genPts)
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv.getPerspectiveTransform(rect, dst)
    warp = cv.warpPerspective(orig, M, (maxWidth, maxHeight))
    #cv.imshow('wrap image', warp)
    return warp, maxHeight, maxWidth

def main_default():
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
    DATA.prevCorners = []
    DATA.area_height_captured = None
    DATA.area_width_captured = None

    if CFG.TRACKER_TYPE is CFG.LED_ENUM:
        tracker = Track2Led(DATA)
        trackerBootstrap = TrackerBootstrap(SETTINGS, DATA)
    else:
        tracker = TrackArruco(DATA)

    ROBOT = Robot2Led(0, CFG.ROB_CNTR, None, None, CFG.HEADING, CFG.DIAMETER, CFG.AXLE_LEN, CFG.WHEEL_RADIUS)
    #Robot2Led(0, (0,0), 0, 0, 0) # w tym obiekcie będą przechowywane aktualne dane o robocie

    if CFG.SIMULATION:#diamater=10, axle_len=10, wheel_radius=5
        simRobot = Robot2Led(0, CFG.ROB_CNTR, None, None, CFG.HEADING, CFG.DIAMETER, CFG.AXLE_LEN, CFG.WHEEL_RADIUS)
        simRobot.calculate_led_pos()

        model = RobotModel2Led(simRobot)
        sim = robotSimulationEnv(model)
        if CFG.CAMERA_FEEDBACK:
            sim.simulate_return_image(0,0,0.01)
            capture = cv.VideoCapture(CFG.VIDEO_PATH)
        #else:
            #capture = sim.simulate_return_image(0,0,0.01)
    else:
        capture = cv.VideoCapture(CFG.VIDEO_PATH)

        if capture.isOpened() is False:
            log_error("Błąd podczas otwarcia filmu lub inicjalizacji kamery")
            return
        else:
            log_info("Plik został poprawnie otwarty / Kamera zostala poprawnie zainicjalizowana.")

        
        # pominiecie klatek na początku filmu
        for _ in range(0, CFG.NUM_FRAMES_TO_SKIP):
            capture.grab()

        # prawdziwy numer klatki
        frame_counter = CFG.NUM_FRAMES_TO_SKIP

    
    log_info('Inicjalizacja sliderow do thresholdingu.')
    trackerBootstrap.setup_thresholds_sliders()

    if (CFG.AUTO_LOAD_THRESHOLDS):
        load_thresholds(SETTINGS.thresholds, CFG.THRESHOLDS_FILE_PATH)

    PID1 = pid(CFG.PROPORTIONAL1, CFG.INTEGRAL1, CFG.DERIVATIVE1)
    PID2 = pid(CFG.PROPORTIONAL2, CFG.INTEGRAL2, CFG.DERIVATIVE2)
    
    PID1.SetPoint = 0
    PID1.setSampleTime(0.01)
    PID1.update(0)
    PID1.setWindup(5.0)

    PID2.SetPoint = 0
    PID2.setSampleTime(0.01)
    PID2.update(0)
    PID2.setWindup(5.0)

    feedback_list = [[],[]]
    time_list =  [[],[]]
    setpoint_list =  [[],[]]

    wasDrawn = True
    Vel = CFG.VEL
    
    while(True):
        if CFG.SIMULATION:
            if SETTINGS.START == 0:
                if CFG.CAMERA_FEEDBACK:
                    sim.simulate_return_image(0,0,0.01)
                    grabbed, frame = capture.read()                 
                else:
                    frame = sim.simulate_return_image(0,0,0.01)
                
                DATA.base_image, DATA.area_height_captured, DATA.area_width_captured = warp_iamge_aruco(frame, DATA)
                #DATA.base_image = frame

                tracker.detectAndTrack(SETTINGS, DATA, ROBOT)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
                continue
        else:
            grabbed, frame = capture.read()
            if not grabbed:
                log_warn('Frame not grabbed. Continue...')
                #capture = cv.VideoCapture(CFG.VIDEO_PATH)
                continue

        #cv.waitKey(100)

        h, w = DATA.base_image.shape[:2]
        p = math.sqrt(h**2 + w**2)
        outTheta = PID1.output
        outVel = float(PID2.output/p * Vel)
        outVel = outVel if outVel < Vel else Vel
        
        vel_1 = outVel * cos(-outTheta)
        vel_2 = outVel * sin(-outTheta)
        
        # print(f'Vl: {vel_1}, Vr: {vel_2}')
        if CFG.SIMULATION:
            if CFG.CAMERA_FEEDBACK:
                    sim.simulate_return_image(vel_1, vel_2, 0.01)
                    grabbed, frame = capture.read()
            else:
                frame = sim.simulate_return_image(vel_1, vel_2, 0.01)

        DATA.base_image, DATA.area_height_captured, DATA.area_width_captured = warp_iamge_aruco(frame, DATA)
        #DATA.base_image = frame
        """Transformacja affiniczna dla prostokąta, określającego pole roboczese ###############"""
        # Zrobiona w juptyer lab

        """################## ROBOT DETECTION AND TRACKING ######################"""
        #detectAndTrack2LedRobot()  retval_image -> Rbot([time], postion, heading(orient))
        #nadrzedna klasa robot i podrzeden z dodatkowymi inforamcjami dla szegolengo rodzaju robota z metodami rysowania path i inne dla podklas      
        tracker.detectAndTrack(SETTINGS, DATA, ROBOT)

        """###################### ROBOT PID CONTROLLING #########################"""

        error = math.hypot(DATA.target[0] - ROBOT.robot_center[0], DATA.target[1] - ROBOT.robot_center[1])
        heading_error = ROBOT.heading - np.pi - math.atan2(ROBOT.robot_center[1]-DATA.target[1], ROBOT.robot_center[0]-DATA.target[0])
        heading_error = -1 * math.atan2(math.sin(heading_error), math.cos(heading_error))
        if (error < CFG.SIM_ERROR): Vel = 0.0
        #elif (heading_error > 0.2) : Vel = 2.0
        else: Vel = CFG.VEL
        print(f'error:{error}')
        print(f'heading_error:{heading_error}')
        #else: V = 5.1  
        PID1.update(heading_error)
        PID2.update(error)
         
        """######################## OTHER ACTIONS ###############################"""
        #zapis danych ruchu robota,. rejestracja ruchu wtf?!
        #DATA.robot_data.append((frame_counter, DATA.robot_center, DATA.led1_pos, DATA.led2_pos))   
        sw = statusWindow('Status')
        if (error > CFG.SIM_ERROR):

            feedback_list[0].append(heading_error)
            feedback_list[1].append(error)

            setpoint_list[0].append(PID1.SetPoint)
            setpoint_list[1].append(PID2.SetPoint)

            time_list[0].append(PID1.current_time)
            time_list[1].append(PID2.current_time)

            img = generate_path_image(DATA, step = 3)#(DATA.base_image, DATA.robot_data) #rysuj droge
            cv.imshow('Robot Path', img)

            wasDrawn = False

        elif wasDrawn == False:
            p1 = draw_plot(feedback_list[0], setpoint_list[0], time_list[0], 'PID CONTROLL HEADING', 1)
            p2 = draw_plot(feedback_list[1], setpoint_list[1], time_list[1], 'PID CONTROLL VELOCITY', 2)
            #free arrays
            p1.show()
            p2.show()

            feedback_list = [[],[]]
            setpoint_list = [[], []]
            time_list = [[], []]

            DATA.robot_data = []

            wasDrawn = True
        
        if CFG.SIMULATION:
            pass
        else:
            #zwiększenei licznika klatek o jeden
            frame_counter += 1

            # Jeżeli chcemy aby film był przetwarany w pętli, dla celów testowych.
            if CFG.PLAY_IN_LOOP == True:
                if trackerBootstrap.play_in_loop(capture, frame_counter) is True:
                    pass

            # pominiętych określonej ilości klatek na cykl
                for _ in range(0, CFG.FRAME_RATE):
                    capture.grab()
                    frame_counter += 1
                    #done abowe
                    #increment the frame counter, domyslnie = 0
                    # frame_counter += CFG.FRAME_RATE

        time.sleep(0.02)
        #heading_error = ROBOT.heading - np.arctan2(DATA.target[0] - ROBOT.robot_center[0], ROBOT.robot_center[1] - DATA.target[1])
        sw.drawData(ROBOT.robot_center, ROBOT.heading, error, heading_error)
        #ROBOT.print()
        hI, wI, _ = DATA.base_image.shape
        DATA.robot_data.append(ROBOT.unpackImg(hI, CFG.AREA_HEIGHT_REAL, wI, CFG.AREA_WIDTH_REAL))   

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    path_img = generate_path_image(DATA)
    #zapis path image na dysk
    file_path = r'C:\Users\barte\Documents\Studia VII\Image_processing\TadroBeaconTracker\tadro-tracker\2Led\paths'
    save_image(path_img, f'RobotPath_' + f'{datetime.now():%Y%m%d_%H%M%S}', file_path)
    capture.release()
    cv.destroyAllWindows()


# def main_simulation():
#     # create settings object to store necessary data for further processing, 
#     # we'll pass it to fcns later
#     #CFG
#     #Inicjalizacja obiektów do przechowywania ustawień i danych
#     SETTINGS = Settings()
#     SETTINGS.thresholds = [{}, {}]
#     SETTINGS.START = 0

#     DATA = Data()
#     DATA.robot_data = []
#     DATA.target = (0,0)
#     DATA.targetHeading = 0

#     if CFG.TRACKER_TYPE is CFG.LED_ENUM:
#         tracker = Track2Led(DATA)
#         trackerBootstrap = TrackerBootstrap(SETTINGS, DATA)
#     else:
#         tracker = TrackArruco(DATA)

#     ROBOT = Robot2Led(0, (0,0), 0, 0, 0)
#     simRobot = Robot2Led(20, (500, 300), (500, 480), (500, 520), 0, 75, 50, 5)
#     model = RobotModel2Led(simRobot)
#     sim = robotSimulationEnv(model)

#     PID1 = pid(CFG.PROPORTIONAL1, CFG.INTEGRAL1, CFG.DERIVATIVE1)
#     PID2 = pid(CFG.PROPORTIONAL2, CFG.INTEGRAL2, CFG.DERIVATIVE2)
    
#     log_info('Inicjalizacja sliderow do thresholdingu.')
#     trackerBootstrap.setup_thresholds_sliders()

#     if (CFG.AUTO_LOAD_THRESHOLDS):
#         load_thresholds(SETTINGS.thresholds, CFG.THRESHOLDS_FILE_PATH)

#     frame = sim.simulate_return_image(0,0,0.01)
#     #angular controll
#     PID1.SetPoint = 0
#     PID1.setSampleTime(0.01)
#     PID1.update(0)
#     PID1.setWindup(5.0)

#     PID2.SetPoint = 0
#     PID2.setSampleTime(0.01)
#     PID2.update(0)
#     PID2.setWindup(5.0)

#     feedback_list = [[],[]]
#     time_list =  [[],[]]
#     setpoint_list =  [[],[]]

#     wasDrawn = True
#     Vel = CFG.VEL
#     while(True):#(capture.isOpened()):
#         if SETTINGS.START == 0:
#             frame = sim.simulate_return_image(0,0,0.01)
#             DATA.base_image = frame
#             tracker.detectAndTrack2LedRobot(SETTINGS, DATA, ROBOT)
#             if cv.waitKey(1) & 0xFF == ord('q'):
#                 break
#             continue

#         h, w = DATA.base_image.shape[:2]
#         p = math.sqrt(h**2 + w**2)
#         outTheta = PID1.output
#         outVel = float(PID2.output/p * Vel)
#         outVel = outVel if outVel < Vel else Vel
        
#         vel_1 = outVel * cos(-outTheta)
#         vel_2 = outVel * sin(-outTheta)
        
#         ##vel_2 = Vel * sin(-outTheta)

#         frame = sim.simulate_return_image(vel_1,vel_2, 0.01)
        
#         DATA.base_image = frame
#         """ Transformacja affiniczna dla prostokąta, określającego pole roboczese """
#         # w przypadku symulacji niepotrzebna, teraz zalkezy id CAMERA_FEEDBACk w konfuguracji 


#         """ ################## ROBOT DETECTION AND TRACKING ###################### """
#         #detectAndTrack2LedRobot()  retval_image -> Rbot([time], postion, heading(orient))
#         #nadrzedna klasa robot i podrzeden z dodatkowymi inforamcjami dla szegolengo rodzaju robota z metodami rysowania path i inne dla podklas      
#         tracker.detectAndTrack2LedRobot(SETTINGS, DATA, ROBOT)

#         """ ###################### ROBOT PID CONTROLLING ######################### """
#         error = math.hypot(DATA.target[0] - ROBOT.robot_center[0], DATA.target[1] - ROBOT.robot_center[1])
#         heading_error = ROBOT.heading - np.pi - math.atan2(ROBOT.robot_center[1]-DATA.target[1], ROBOT.robot_center[0]-DATA.target[0])
#         heading_error = -1 * math.atan2(math.sin(heading_error), math.cos(heading_error))
#         if (error < CFG.SIM_ERROR): Vel = 0.0
#         #elif (heading_error > 0.2) : Vel = 2.0
#         else: Vel = CFG.VEL
#         print(f'error:{error}')
#         print(f'heading_error:{heading_error}')
#         #else: V = 5.1  
#         PID1.update(heading_error)
#         PID2.update(error)

#         """######################## OTHER ACTIONS ###############################"""
#         #zapis danych ruchu robota,. rejestracja ruchu wtf?!
#         #DATA.robot_data.append((frame_counter, DATA.robot_center, DATA.led1_pos, DATA.led2_pos))

#         sw = statusWindow('Status')
#         if (error > CFG.SIM_ERROR):

#             feedback_list[0].append(heading_error)
#             feedback_list[1].append(error)

#             setpoint_list[0].append(PID1.SetPoint)
#             setpoint_list[1].append(PID2.SetPoint)

#             time_list[0].append(PID1.current_time)
#             time_list[1].append(PID2.current_time)

#             img = generate_path_image(DATA, step = 3)#(DATA.base_image, DATA.robot_data) #rysuj droge
#             cv.imshow('Robot Path', img)

#             wasDrawn = False

#         elif wasDrawn == False:
#             p1 = draw_plot(feedback_list[0], setpoint_list[0], time_list[0], 'PID CONTROLL HEADING', 1)
#             p2 = draw_plot(feedback_list[1], setpoint_list[1], time_list[1], 'PID CONTROLL VELOCITY', 2)
#             #free arrays
#             p1.show()
#             p2.show()

#             feedback_list = [[],[]]
#             setpoint_list = [[], []]
#             time_list = [[], []]

#             DATA.robot_data = []

#             wasDrawn = True

#         time.sleep(0.02)
#         #heading_error = ROBOT.heading - np.arctan2(DATA.target[0] - ROBOT.robot_center[0], ROBOT.robot_center[1] - DATA.target[1])
#         sw.drawData(ROBOT.robot_center, ROBOT.heading, error, heading_error)
#         #ROBOT.print()
#         DATA.robot_data.append(ROBOT.unpack())   

#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break
    
#     path_img = generate_path_image(DATA)
#     #zapis path image na dysk
#     file_path = r'C:\Users\barte\Documents\Studia VII\Image_processing\TadroBeaconTracker\tadro-tracker\2Led'
#     save_image(path_img, f'RobotPath_' + '{datetime.now():%Y%m%d_%H%M%S}}', file_path)
#     cv.destroyAllWindows()

if __name__ == '__main__':
    #main_simulation()
    main_default()
log_info("Exit")
