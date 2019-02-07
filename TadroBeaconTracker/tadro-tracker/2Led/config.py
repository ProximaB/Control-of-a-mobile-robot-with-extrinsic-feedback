from os.path import normpath
import cv2.aruco as aruco
import cv2 as cv
class Data:
    def __init__(self):
        pass
        
D = Data()

######################## SET D CONSTANTS CONFIG OBJECT ######################## 
# Real Robot area settings
D.AREA_HEIGHT_REAL = 50 #[mm] 12.8 razy mniejsze niz pix 12.8mm/px
D.AREA_WIDTH_REAL = 100 #[mm]

D.LED_ENUM = 1
D.ARUCCO_ENUM = 2

D.SIMULATION = True
D.CAMERA_FEEDBACK = True # czy obraz przechwycic z kamery czy wprost z symulatora
D.WARP_TOLERANCE = 20#2 # tolerancja na zmiane markerow, zmienijsza zakłoócenia,
# Choose tracker algorithm: 2 Led -> 0, Arruco marker -> 1
D.TRACKER_TYPE = D.LED_ENUM #D.ARUCCO_ENUM # D.LED_ENUM

if D.TRACKER_TYPE is D.LED_ENUM:
    # Robot settings 
    D.ROB_CNTR = (50, 25) # x, y
    D.HEADING = 0
    D.DIAMETER = 10 #15#10 
    D.AXLE_LEN = 7 #10 #7
    D.WHEEL_RADIUS = 2
    # Simulator settings
    D.W_HEIGHT = 840#588#640
    D.W_WIDTH =  1480#1036#1280

    D.SIDEPIXEL_ARUCO = 100#100

    D.SIM_ERROR =  0.1*D.W_WIDTH/D.AREA_WIDTH_REAL
    
elif D.TRACKER_TYPE is D.ARUCCO_ENUM:
    # Robot settings 
    D.ROB_CNTR = (50, 25) # x, y
    D.HEADING = 0
    D.DIAMETER = 20 #20#15#10 
    D.AXLE_LEN = 14 #17#10 #7
    D.WHEEL_RADIUS = 2
    # Simulator settings
    D.W_HEIGHT = 840#588#640
    D.W_WIDTH =  1480#1036#1280

    D.SIDEPIXEL_ARUCO = 100#100
    D.ARUCO_SIDE_PIXELS = 80

    D.SIM_ERROR = 3

#############
D.D_MARGIN_HORIZONTAL = (150, 10) #(L,R)
D.D_MARGIN_VERTICAL = (10, 10)
D.FONT = cv.FONT_HERSHEY_SIMPLEX
  
D.D_WIDTH = D.W_WIDTH - D.D_MARGIN_HORIZONTAL[0] - D.D_MARGIN_HORIZONTAL[1] #Wielkosc symulacji, potrzebne do policzenia skali 
D.D_HEIGHT = D.W_HEIGHT - D.D_MARGIN_VERTICAL[0] - D.D_MARGIN_VERTICAL[1]   # w odniesieniu do wielkosci wykrytego oknaprzez kamere

D.LED_RADIUS = 12#15#7#8 #px
D.LED_THICKNES = -1#8 
D.ROBOT_THICKNESS = 3

D.AREA_POINTS = [(10,10), (-10,-10)] #punkty pola dodawane marginesy wys szer
D.AREA_THICKNESS = 4

#Settings for arruco markers and enums
D.ARUCO_DICT = aruco.DICT_ARUCO_ORIGINAL #aruco.DICT_4X4_50
D.ROBOT_ID = 0
D.UPPER_LEFT_ID = 1
D.UPPER_RIGHT_ID = 2
D.BOTTOM_RIGHT = 3
D.BOTTOM_LEFT = 4
D.CORNER_IDS = [D.UPPER_LEFT_ID, D.UPPER_RIGHT_ID, D.BOTTOM_RIGHT, D.BOTTOM_LEFT]
D.MARGIN_ARUCO = 40 #30

#Settings for PID controller
#angular controll



D.PROPORTIONAL1 = 1.0 #proporcjonalny
D.INTEGRAL1 = 1.3 #całka
D.DERIVATIVE1 = 0.001 #pochodna

D.PROPORTIONAL2 = 1.0
D.INTEGRAL2 = 1.4
D.DERIVATIVE2  = 0.001

D.VEL = 500

 
#Choose leds order, when LEFT_LD = 0 that refer to led on the side wihich robot is turing going forward-left 
D.LEFT_LD = 0

D.RIGHT_LD = 1

######################## 
#D.VIDEO_PATH = 0 #1 eeye3 mch faster
#D.VIDEO_PATH = normpath(r'C:/Users/barte/Documents/Studia VII/Image_processing/Assets/Green_Blue_Led.avi')
D.VIDEO_PATH = 1

D.NUM_FRAMES_TO_SKIP = 0

D.PLAY_IN_LOOP = False

D.FRAME_RATE = 0

D.SHOW_PATH = False

D.MARKER_PREVIEW = True

######################## 
D.AUTO_LOAD_THRESHOLDS = True

D.THRESHOLDS_FILE_PATH = r"C:\Users\barte\Documents\Studia VII\Image_processing\TadroBeaconTracker\tadro-tracker\thresh.txt"

D.SAVE_POSNS = True
######################## 
D.CAMERA_CALIBRATION_UNDISTORT = False

D.CAMERA_CALIBRATION_PATH = r'C:\Users\barte\Documents\Studia VII\Image_processing\TadroBeaconTracker\tadro-tracker\2Led\calibration_images\cam_calibration_data.p'

D.NUM_CALIBRATION_TO_SKIP = 0

######################## 
D.ADAPTIVE_THRESHOLD = True

D.HALF_SIZE = False

D.THR_WIND_OFFSET = (640, 0)

D.THR_WIND_SLF_OFFSET = 320

D.SLD_WIND_OFFSET = (640, 150) #1280

D.SLD_WIND_SLF_OFFSET = 320
