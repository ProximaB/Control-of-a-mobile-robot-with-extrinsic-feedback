from os.path import normpath

class Data:
    def __init__(self):
        pass
        
D = Data()

######################## SET D CONSTANTS CONFIG OBJECT ######################## 

#Choose leds order, when LEFT_LD = 0 that refer to led on the side wihich robot is turing going forward-left 
D.LEFT_LD = 0

D.RIGHT_LD = 1

######################## 
D.VIDEO_PATH = 0 #1 eeye3 mch faster

D.NUM_FRAMES_TO_SKIP = 0

D.PLAY_IN_LOOP = False

D.FRAME_RATE = 0

######################## 
D.AUTO_LOAD_THRESHOLDS = False

D.THRESHOLDS_FILE_PATH = r"C:\Users\barte\Documents\Studia VII\Image_processing\TadroBeaconTracker\tadro-tracker\thresh.txt"

D.USE_GUI = False

D.SAVE_POSNS = True
######################## 
D.CAMERA_CALIBRATION_SUBSTRACT = False

D.CAMERA_CALIBRATION_PATH = r'.\TadroBeaconTracker\tadro-tracker\2Led\calibration_images\cam_calibration_data.p'

D.NUM_CALIBRATION_TO_SKIP = 0

######################## 
D.ADAPTIVE_THRESHOLD = False

D.BACKGROUND_EXTRACTION = False

D.HALF_SIZE = False

D.THR_WIND_OFFSET = (640, 0)

D.THR_WIND_SLF_OFFSET = 320

D.SLD_WIND_OFFSET = (640, 150) #1280

D.SLD_WIND_SLF_OFFSET = 320
