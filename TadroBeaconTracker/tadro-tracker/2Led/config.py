from os.path import normpath

class Data:
    def __init__(self):
        pass
        
D = Data()

######################## SET D CONSTANTS CONFIG OBJECT ######################## 
#Settings for PID controller
D.PROPORTIONAL = 0.2 #proporcjonalny
D.INTEGRAL = 0.0 #całka
D.DERIVATIVE  = 0.0 #pochodna
 
#Choose leds order, when LEFT_LD = 0 that refer to led on the side wihich robot is turing going forward-left 
D.LEFT_LD = 0

D.RIGHT_LD = 1

######################## 
#D.VIDEO_PATH = 0 #1 eeye3 mch faster
D.VIDEO_PATH = normpath(r'C:/Users/barte/Documents/Studia VII/Image_processing/Assets/Green_Blue_Led.avi')

D.NUM_FRAMES_TO_SKIP = 0

D.PLAY_IN_LOOP = True

D.FRAME_RATE = 0

######################## 
D.AUTO_LOAD_THRESHOLDS = False

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
