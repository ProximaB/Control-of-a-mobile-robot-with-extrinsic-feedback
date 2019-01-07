''' Import packages '''
import numpy as np
import cv2 as cv
import math
import copy
import sys
from os.path import normpath
from functools import partial 
import pickle
import datetime
''' Import custom modules '''
# add local path to make interpreter able to obtain custom modules. (when u run  py from glob scope)
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
# load Config
from config import D as CFG
# import Robot class
from robot import *
# custom simpl logger
from logger import *
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
    
    # własny pomysł na rejestrowanie sliderow z wykorzystaiem partial
        for thresh_name in thresholds[i].keys():
           cv.createTrackbar(thresh_name, 'Sliders_%d' % i, thresholds[i][thresh_name], 255,
           partial(change_slider, thresholds, i, thresh_name))
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
    cv.setMouseCallback('Preview', onMouse, data)
    """
        # We have not created our "scratchwork" images yet
        created_images = False

        # Variable for key presses
        last_key_pressed = 255

        last_posn = (0,0)
        velocity = 40
    """
def save_image(image, fileName, path):
    try:
        cv.imwrite(f'{path}/{fileName}.bmp', image);
        log_info('Zapis obrazu zakończony powodzeniem.\n'
                f'File path: {path}/{fileName}.bmp')
    except Exception as error:
        log_warn(f'Obraz nie został zapisany do pliku.', error)
        pass

def save_thresholds(thresholds : dict, pathToFile):
    with open(pathToFile, 'wb') as file:
        try:
            pickle.dump(thresholds, file)
            log_info('Thresholds has been saved to file.\n'
                    f'File path: {pathToFile}')
        except Exception as error:
            log_warn(f'Thresholds nie został zapisany do pliku.', error)
            pass

def load_thresholds(thresholds, pathToFile):
    try:
        with open(pathToFile, 'rb') as file:
            thresholds = pickle.load(file)
        log_info('Thresholds został załadowany.')
        return thresholds
    except Exception as error:
        log_warn(f'Thresholds nie został załadowany.', error)
        return thresholds

    if (CFG.USE_GUI):
    # aktualizacja pozycji sliderów
        for j in range(len(thresholds)):
            for x in ['low_red', 'high_red', 'low_green', 'high_green', 'low_blue', 'high_blue',
                          'low_hue', 'high_hue', 'low_sat', 'high_sat', 'low_val', 'high_val']:
                cv.setTrackbarPos(x, f'Sliders_{j}', thresholds[j][x])

def generate_path_image(data):
    pass
    return 
class Track2Led:
   # def __init__(self, SETTINGS, DATA):
   #     self.SETTINGS = SETTINGS
   #    self.DATA = DATA

    def init_images(self, DATA):
        DATA.size = DATA.processed_image.shape
        # Create images for each color channel
        DATA.red_image = np.zeros(DATA.size)
        DATA.blue_image = np.zeros(DATA.size)
        DATA.green_image = np.zeros(DATA.size)
        DATA.hue_image = np.zeros(DATA.size)
        DATA.sat_image = np.zeros(DATA.size)
        DATA.val_image = np.zeros(DATA.size)

        # The final thresholded result
        DATA.threshed_images = [None, None] # tablca przechowująca wynikowe thresholdy, [object, objct]
        DATA.threshed_images[DATA.LEFT_LD] = np.zeros(*DATA.size) #operator unpacking
        DATA.threshed_images[DATA.RIGHT_LD] = np.zeros(*DATA.size)
        # Create an hsv image and a copy for contour-finding
        DATA.hsv = np.zeros(*DATA.size)
        DATA.copy = np.zeros(*DATA.size)
        #DATA.storage = cv.CreateMemStorage(0) # Create memory storage for contours

        # bunch of keypress values
        # So we know what to show, DATAepenDATAing on which key is presseDATA
        DATA.key_dctionary = {
            ord('0'): DATA.threshed_images,
            ord('1'): DATA.red,
            ord('2'): DATA.green,
            ord('3'): DATA.blue,
            ord('q'): DATA.red_threshed,
            ord('w'): DATA.green_threshed,
            ord('e'): DATA.blue_threshed,
            ord('a'): DATA.hue,
            ord('s'): DATA.sat,
            ord('d'): DATA.val,
            ord('z'): DATA.hue_threshed,
            ord('x'): DATA.sat_threshed,
            ord('c'): DATA.val_threshed,
        }
        #wyrzucic, kalibracja w osobnym programie ze zdjec i zapis od pliku pickle i odczyt rownie, metody juz gotowe w tym module od odcz/zaps
        #Obtain the image from the camera calibration to subtract from the captured image
        if DATA.CAMERA_CALIBRATION_SUBTRACT:
            data_file = open(CFG.CAMERA_CALIBRATION_PATH, 'rb')
            calib_data = pickle.load(data_file)
            SETTINGS.mtx = calib_data['mtx']
            SETTINGS.dist = calib_data['dist']
            SETTINGS.data_file.close()

            """ cap = cv.VideoCapture(DATA.CAMERA_CALIBRATION_PATH)
            #cap = cv.VideoCapture('C:/Users/barte/DATAocuments/Studia VII/Image_processing/Assets/Green_Blue_Led.avi')
            if(not cap.isOpened()):
                raise NameError("Invalid camera calibration file path. Turn off camera calibration subtraction or correct.")
            else:
                print("Camera calibration path exists.")
            for i in range(0, DATA.NUM_CALIBRATION_FRAMES_TO_SKIP):
                cap.read()
            ret, frame = cap.read()

            if (DATA.PLAY_IN_LOOP == True):
                frame_counter += 1
                #If the last frame is reached, reset the capture and the frame_counter
                CV_CAP_PROP_FRAME_COUNT = 7
                if frame_counter == cap.get(CV_CAP_PROP_FRAME_COUNT):
                    frame_counter = 0 #Or whatever as long as it is the same as next line
                    CV_CAP_PROP_POS_FRAMES = 1
                    cap.set(CV_CAP_PROP_POS_FRAMES, 0)

            DATA.calibration_image = frame
            
            R = Robot2Led(30, (12,32), np.pi/2,24.52,423.342) 
            return R.print()"""
            pass

    def threshold_image(self, DATA, SETTINGS):
    """ runs the image processing in order to create a 
        black and white thresholded image out of DATA.image
        into DATA.threshed_images.
    """
    if DATA.CAMERA_CALIBRATION_SUBTRACT:
        DATA.image = cv.subtract(DATA.image, DATA.calibration_image)

    if DATA.ADAPTIVE_THRESHOLD:
        DATA.grey = cv.cvtColor(DATA.image, cv.COLOR_RGB2GRAY)
        #DATA.grey = np.array(DATA.grey, np.int32)
        DATA.adaptive_thresh = cv.adaptiveThreshold(
            DATA.grey, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

    # DATA.image.shape[2] gives the number of channels
    DATA.BGRchannels = cv.split(DATA.image)
    #print DATA.BGRchannels
    DATA.blue = DATA.BGRchannels[0]
    DATA.green = DATA.BGRchannels[1]
    DATA.red = DATA.BGRchannels[2]

    # This line creates a hue-saturation-value image
    DATA.hsv = cv.cvtColor(DATA.image, cv.COLOR_BGR2HSV)
    #print DATA.image.shape
    #print DATA.hsv
    #print DATA.hsv.shape
    #print cv.split(DATA.hsv)
    DATA.HSVchannels = cv.split(DATA.hsv)
    #print DATA.HSVchannels
    DATA.hue = DATA.HSVchannels[0]
    DATA.sat = DATA.HSVchannels[1]
    DATA.val = DATA.HSVchannels[2]

    for i in range(len(DATA.thresholds)):
        DATA.red_threshed = np.eye(*DATA.size)
        DATA.blue_threshed = np.eye(*DATA.size)
        DATA.green_threshed = np.eye(*DATA.size)
        DATA.hue_threshed = np.eye(*DATA.size)
        DATA.sat_threshed = np.eye(*DATA.size)
        DATA.val_threshed = np.eye(*DATA.size)

        DATA.threshed_images[i] = np.eye(*DATA.size)

        DATA.red_threshed = cv.inRange(
            DATA.red, DATA.thresholds[i]["low_red"], DATA.thresholds[i]["high_red"], DATA.red_threshed)
        DATA.blue_threshed = cv.inRange(
            DATA.blue, DATA.thresholds[i]["low_blue"], DATA.thresholds[i]["high_blue"], DATA.blue_threshed)
        DATA.green_threshed = cv.inRange(
            DATA.green, DATA.thresholds[i]["low_green"], DATA.thresholds[i]["high_green"], DATA.green_threshed)
        DATA.hue_threshed = cv.inRange(
            DATA.hue, DATA.thresholds[i]["low_hue"], DATA.thresholds[i]["high_hue"], DATA.hue_threshed)
        DATA.sat_threshed = cv.inRange(
            DATA.sat, DATA.thresholds[i]["low_sat"], DATA.thresholds[i]["high_sat"], DATA.sat_threshed)
        DATA.val_threshed = cv.inRange(
            DATA.val, DATA.thresholds[i]["low_val"], DATA.thresholds[i]["high_val"], DATA.val_threshed)

        #mnożenie do wynikowego threshold_iamges
        DATA.threshed_images[i] = cv.multiply(
            DATA.red_threshed, DATA.green_threshed, DATA.threshed_images[i])
        DATA.threshed_images[i] = cv.multiply(
            DATA.threshed_images[i], DATA.blue_threshed, DATA.threshed_images[i])
        DATA.threshed_images[i] = cv.multiply(
            DATA.threshed_images[i], DATA.hue_threshed, DATA.threshed_images[i])
        DATA.threshed_images[i] = cv.multiply(
            DATA.threshed_images[i], DATA.sat_threshed, DATA.threshed_images[i])
        DATA.threshed_images[i] = cv.multiply(
            DATA.threshed_images[i], DATA.val_threshed, DATA.threshed_images[i])

        if(DATA.ADAPTIVE_THRESHOLD):
            DATA.threshed_images[i] = cv.multiply(
                DATA.threshed_images[i], DATA.adaptive_thresh, DATA.threshed_images[i])

    #DATA.threshed_images = cv.dilate(DATA.threshed_images, None, iterations=2)

    #cv.imshow(DATA.threshed_images)
    # erozja dylatacja w zaleznosci od potrzeb
    #cv.Erode(DATA.threshed_images, DATA.threshed_images, iterations = 1)
    #cv.Dilate(DATA.threshed_images, DATA.threshed_images, iterations = 1)

def check_leds(x1, y1, x2, y2):
    #sprawdzenie, czy led są w rozsądniej odległości

    #later, it would be nice to know exactly how far apart they should be based on the skew grid
    #and build a stronger heuristic from that
    MAX_DIST = 500
    MIN_DIST = 1
    dist = math.sqrt(abs(int(x2) - int(x1))**2 + abs(int(y2) - int(y1))**2)

    result = MIN_DIST < dist < MAX_DIST

    return result

    def find_2Led(self, DATA, SETTINGS):
        """ finds all the contours in threshed image, finds the largest of those,
            and then marks in in the main image
        """
        # initialize list of LED posns to len of thresholds
        LEDs = [0 for k in range(len(DATA.thresholds))]

        for i in range(len(DATA.threshed_images)):
            # Create a copy image of thresholds then find contours on that image
            DATA.copy = DATA.threshed_images[i].copy() # copy threshed image

            

            # this is OpenCV's call to find all of the contours:
            _, contours, _ = cv.findContours(DATA.copy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            # Next we want to find the *largest* contour
            # this is the standard algorithm:
            #    walk the list of all contours, remembering the biggest so far:
            if len(contours) > 0:
                biggest = contours[0]
                second_biggest = contours[0]
                biggestArea = cv.contourArea(contours[0]) #get first contour
                secondArea = cv.contourArea(contours[0])
                for x in contours:
                    nextArea = cv.contourArea(x)
                    if biggestArea < nextArea:
                        second_biggest = biggest
                        biggest = x
                        secondArea = biggestArea
                        biggestArea = nextArea

                #does the same: cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

                # Use OpenCV to get a bounding rectangle for the largest contour
                br = cv.boundingRect(biggest)

                # Make a bounding box around the biggest blob
                upper_left = (br[0], br[1])
                lower_left = (br[0], br[1] + br[3])
                lower_right = (br[0] + br[2], br[1] + br[3])
                upper_right = (br[0] + br[2], br[1])
                cv.polylines(DATA.image, [np.array([upper_left,lower_left,lower_right,upper_right], dtype=np.int32)],
                            1, (255, 0, 0))
                cv.polylines(DATA.threshed_images[i], [np.array([upper_left,lower_left,lower_right,upper_right], dtype=np.int32)],
                            1, (255, 0, 0))

                #Store the contour info for the biggest blob, which we assume is the LED based on thresholding
                LEDs[i] = biggest

        #print biggest
        #print second_biggest
        #calculate moments for biggest and second biggest blobs
        moment0 = cv.moments(LEDs[0])
        moment1 = cv.moments(LEDs[1])

        if (moment0['m00'] > 0):
            center_x = moment0['m10']/moment0['m00']
            center_y = moment0['m01']/moment0['m00']
            DATA.blue_pos = (int(center_x), int(center_y))
        else:
            DATA.blue_pos = None

        if (moment1['m00'] > 0):
            second_center_x = moment1['m10']/moment1['m00']
            second_center_y = moment1['m01']/moment1['m00']
            DATA.green_pos = (int(second_center_x), int(second_center_y))
        else:
            DATA.green_pos = None


        #if these blobs have areas > 0, then calculate the average of their centroids
        if (moment0['m00'] > 0 and moment1['m00'] > 0):

            led_check = are_these_leds(center_x, center_y, second_center_x, second_center_y)

            if (led_check):
                DATA.tadro_center = (int((center_x + second_center_x)/2), int((center_y + second_center_y)/2))
                cv.circle(DATA.image, DATA.tadro_center, 10, (255, 255, 0))
                cv.circle(DATA.threshed_images[0], DATA.tadro_center, 10, (255, 255, 0))
            else:
                DATA.tadro_center = None
            
        #else simply calculate the centroid of the largest blob
        else:
            DATA.tadro_center = None

        # Draw matching contours in white with inner ones in green
        # cv.DrawContours(DATA.image, biggest, cv.RGB(255, 255, 255), 
        #               cv.RGB(0, 255, 0), 1, thickness=2, lineType=8, 
        #               offset=(0,0))


    def detectAndTrack2LedRobot(self, SETTINGS, DATA):
        """ this function organizes all of the processing
            done for each image from a camera type 2Led robot """

        if DATA.base_image is None:
            raise Exception("No base_iamge provided. {->detectAndTrack2LedRobot}")
        DATA.processed_image = DATA.base_image
        
        if DATA.created_images == False:
            self.init_images(DATA)
            DATA.created_images = True
        
        self.threshold_image(DATA, SETTINGS)
        self.find_2Led(DATA, SETTINGS)

        key_press_raw = cv.waitKey(5) # gets a raw key press
        key_press = key_press_raw & 0xFF # same as 255# sets all but the low 8 bits to 0
        
        # Handle key presses only if it's a real key (255 = "no key pressed")
        if key_press != 255:
            pass #check_key_press(key_press)

        if (DATA.USE_GUI):
            # Update the displays:
            # Main image:
            cv.imshow('Preview', DATA.image)

            # Currently selected threshold image:
            for i in range(len(DATA.threshed_images)):
                cv.imshow('Threshold_%d' % i, DATA.threshed_images[i])#D.current_threshold )


###################### CALLBACK FUNCTIONS #########################

def onMouse(event, x, y, flags, data):
    """ Callback dla kliknięcia myszy na okno Previw"""
    # clicked the left button
    if event==cv.EVENT_LBUTTONDOWN: 
        print('X, Y:', x, y, "    ", end=' ')
        (b,g,r) = data.image[y,x]
        print('R, G, B: ', int(r), int(g), int(b), "    ", end=' ')
        (h,s,v) = data.hsv[y,x]
        print('H, S, V', int(h), int(s), int(v))
        data.down_coord = (x,y)

# Function for changing the slider values
def change_slider(thresholds, i, name, new_threshold):
    """ Callback do zmiany wartośći sliderów i wyświetlenia ustawionej wartości w konsoli."""
    thresholds[i][name] = new_threshold
    print('{name}: {val}'.format(name=name, val = thresholds[i][name]))

# Callback zachowanie dla przycisków i ze pętlą dla przyciskow ustawiajacy wyswietlany thresh
def check_key_press(key_press, DATA, SETTINGS):
    """ this handler is called when a real key press has been
        detected, and updates everything appropriately
    """

    DATA.last_key_pressed = key_press

    # if it was ESC, make it 'q'
    if key_press == 27:
        key_press = ord('q')

    # if a 'q' or ESC was pressed, we quit
    if key_press == ord('q'): 
        print("quitting")
        return

    # help menu
    if key_press == ord('h'):
        print(" Keyboard Command Menu")
        print(" ==============================")
        print(" q    : quit")
        print(" ESC  : quit")
        print(" h    : help menu")
        print(" w    : show total threshold image in threshold window")
        print(" r    : show red image in threshold window")
        print(" t    : show green image in threshold window")
        print(" y    : show blue image in threshold window")
        print(" f    : show thresholded red image in threshold window")
        print(" g    : show thresholded blue image in threshold window")
        print(" h    : show thresholded green image in threshold window")
        print(" a    : show hue image in threshold window")
        print(" s    : show saturation image in threshold window")
        print(" o    : save path data")
        print(" p    : draw robot path")
        print(" d    : show value image in threshold window")
        print(" z    : show thresholded hue image in threshold window")
        print(" x    : show thresholded saturation image in threshold window")
        print(" c    : show thresholded value image in threshold window")
        print(" v    : saves threshold values to file (overwriting)")
        print(" b    : loads threshold values from file")
        print(" u    : mousedrags no longer set thresholds")
        print(" i    : mousedrag set thresholds to area within drag")

    elif key_press == ord('v'):
        thresh = SETTINGS.thresholds
        f = open( "./thresh.txt", "w" ) # open the file "thresh.txt" for writing
        print(x, file=f) # print x to the file object f
        f.close() # it's good to close the file afterwards
        print("(v) Wrote thresholds to thresh.txt. Use 'b' to load them.")

    elif key_press == ord('b'):
        load_thresholds(SETTINGS.thresholds, CFG.THRESHOLDS_FILE_PATH)
        
    elif key_press == ord('o'):
        print("saving position data to posns.txt...")
        x = DATA.tadro_data
        f = open( "./posns.txt", "w" ) # open the file "thresh.txt" for writing
        print(x, file=f) # print x to the file object f
        f.close() # it's good to close the file afterwards
        print("save complete.")

    elif key_press == ord('p'):
        print('Drawing path of robot')
        make_tadro_path_image()
        
    # threshold keypresses:
    elif key_press in list(DATA.key_dictionary.keys()):
        DATA.current_threshold = DATA.key_dictionary[key_press]
   


####################### UTILITY ClASS / FUNCTIONS ##########################


def play_in_loop(capture, frame_counter):
    ''' Here should be explenation how it work'''
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
    tracker = Track2Led()

    log_info('Inicjalizacja sliderow do thresholdingu.')
    setup_thresholds_sliders(SETTINGS.thresholds, DATA)

    capture = cv.VideoCapture(CFG.VIDEO_PATH)
    if capture.isOpened() is False:
        log_error("Błąd podczas otwarcia filmu lub inicjalizacji kamery")
        return
    else:
        log_info("Plik został poprawnie otwarty / Kamera zostala poprawnie zainicjalizowana.")

    
    if CFG.BACKGROUND_EXTRACTION:
        #extract_background()
        pass

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
            continue

        if CFG.BACKGROUND_EXTRACTION:
            pass# frame = DATA.backgrnd_extractor.apply(frame)
        
        DATA.base_image = frame
        ##################### ROBOT DETECTION AND TRACKING #######################
        #handle_image() wtf?! retval -> Rbot([time], postion, heading(orient))
        #nadrzedna klasa robot i podrzeden z dodatkowymi inforamcjami dla szegolengo rodzaju robota z metodami rysowania path i inne dla podklas
        
        result = Track2Led.detectAndTrack2LedRobot(SETTINGS, DATA)

        #################### ROBOT PID CONTROLLING ########################


        ########################### OTHER ACTIONS ################################


        
        #zapis danych ruchu robota,. rejestracja ruchu wtf?!
        #DATA.robot_data.append((frame_counter, DATA.tadro_center, DATA.blue_pos, DATA.green_pos))   
            
        #zwiększenei licznika klatek o jeden
        frame_counter += 1

        # Jeżeli chcemy aby film był przetwarany w pętli, dla celów testowych.
        if CFG.PLAY_IN_LOOP == True:
            if play_in_loop(capture, frame_counter) is True:
                continue

        # pominiętych określonej ilości klatek na cykl
        for _ in range(0, CFG.FRAME_RATE):
            capture.grab()
            frame_counter += 1
        #done abowe
        #increment the frame counter, domyslnie = 0
        #frame_counter += CFG.FRAME_RATE

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    #path_img = generate_path_image(DATA.)
    #zapis path image na dysk
    #file_path = r'C:\Users\barte\Documents\Studia VII\Image_processing\TadroBeaconTracker\tadro-tracker\2Led'
    #save_image(path_img, f'Robot_{str(datetime.datetime.now().isoformat())}', file_path)
    capture.release()
    cv.destroyAllWindows()

main()

log_info("Exit")
