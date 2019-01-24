from os.path import normpath
import cv2.aruco as aruco

class Data:
    def __init__(self):
        pass
        
D = Data()

######################## SET D CONSTANTS CONFIG OBJECT ######################## 
#Settings for arruco markers and enums
D.ARUCO_DICT = aruco.DICT_4X4_50
D.ROBOT_ID = 0
D.UPPER_LEFT_ID = 1
D.UPPER_RIGHT_ID = 2
D.BOTTOM_RIGHT = 3
D.BOTTOM_LEFT = 4
D.CORNER_IDS = [D.UPPER_LEFT_ID, D.UPPER_RIGHT_ID, D.BOTTOM_RIGHT, D.BOTTOM_LEFT]
D.SIDEPIXEL_ARUCO = 50
D.SIDEPIXEL_ARUCO_ROBOT = 30
D.MARGIN_ARUCO = 15

#Settings for PID controller
#angular controll

D.LED_ENUM = 1
D.ARUCCO_ENUM = 2

D.SIMULATION = True
D.CAMERA_FEEDBACK = False # czy obraz przechwycic z kamery czy wprost z symulatora
# Choose tracker algorithm: 2 Led -> 0, Arruco marker -> 1
D.TRACKER_TYPE = D.LED_ENUM



D.PROPORTIONAL1 = 1.0 #proporcjonalny
D.INTEGRAL1 = 1.0 #całka
D.DERIVATIVE1 = 0.001 #pochodna

D.PROPORTIONAL2 = 1
D.INTEGRAL2 = 1.4
D.DERIVATIVE2  = 0.001

D.VEL = 1000
D.SIM_ERROR = 5
 
#Choose leds order, when LEFT_LD = 0 that refer to led on the side wihich robot is turing going forward-left 
D.LEFT_LD = 1

D.RIGHT_LD = 0

######################## 
#D.VIDEO_PATH = 0 #1 eeye3 mch faster
#D.VIDEO_PATH = normpath(r'C:/Users/barte/Documents/Studia VII/Image_processing/Assets/Green_Blue_Led.avi')
D.VIDEO_PATH = 1
D.NUM_FRAMES_TO_SKIP = 0

D.PLAY_IN_LOOP = True

D.FRAME_RATE = 0

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
