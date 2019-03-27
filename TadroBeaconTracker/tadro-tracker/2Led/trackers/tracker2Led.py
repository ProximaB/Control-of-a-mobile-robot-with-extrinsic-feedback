import time
import numpy as np
import cv2 as cv
import sys
import math
import pickle
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
# load Config
from config import D as CFG
from utils import *

class Track2Led:
   # def __init__(self, SETTINGS, DATA):
   #     self.SETTINGS = SETTINGS
   #    self.DATA = DATA
    def __init__(self, DATA):
        DATA.created_images = False
        self.time = time.clock()

    def init_images(self, DATA, SETTINGS):
        shape = DATA.processed_image.shape

        # Create images for each color channel
        DATA.red_image = np.zeros(shape)
        DATA.blue_image = np.zeros(shape)
        DATA.green_image = np.zeros(shape)
        DATA.hue_image = np.zeros(shape)
        DATA.sat_image = np.zeros(shape)
        DATA.val_image = np.zeros(shape)

        DATA.red_image_threshed = np.eye(*shape)
        DATA.green_image_threshed = np.eye(*shape)
        DATA.blue_threshed_image = np.eye(*shape)
        DATA.hue_threshed_image = np.eye(*shape)
        DATA.sat_threshed_image = np.eye(*shape)
        DATA.val_threshed_image = np.eye(*shape)
        # The final thresholded result
        DATA.threshed_images = [None, None] # tablca przechowująca wynikowe thresholdy, [object, objct]
        DATA.current_threshold = DATA.threshed_images
        DATA.threshed_images[CFG.LEFT_LD] = np.eye(*shape) #operator unpacking
        DATA.threshed_images[CFG.RIGHT_LD] = np.eye(*shape)
        # Create an hsv image and a copy for contour-finding
        DATA.hsv = np.eye(*shape)
        DATA.copy = np.eye(*shape)
        #DATA.storage = cv.CreateMemStorage(0) # Create memory storage for contours

        # bunch of keypress values
        # So we know what to show, DATAepenDATAing on which key is presseDATA
        DATA.key_dictionary = {
            ord('w'): DATA.threshed_images,
            ord('u'): DATA.red_image,
            ord('i'): DATA.green_image,
            ord('o'): DATA.blue_image,
            ord('j'): DATA.red_image_threshed,
            ord('k'): DATA.green_image_threshed,
            ord('l'): DATA.blue_threshed_image,
            ord('a'): DATA.hue_image,
            ord('s'): DATA.sat_image,
            ord('d'): DATA.val_image,
            ord('z'): DATA.hue_threshed_image,
            ord('x'): DATA.sat_threshed_image,
            ord('c'): DATA.val_threshed_image,
        }
        #wyrzucic, kalibracja w osobnym programie ze zdjec i zapis od pliku pickle i odczyt rownie, metody juz gotowe w tym module od odcz/zaps
        #Obtain the image from the camera calibration to subtract from the captured image
        if CFG.CAMERA_CALIBRATION_UNDISTORT:
            data_file = open(CFG.CAMERA_CALIBRATION_PATH, 'rb')
            calib_data = pickle.load(data_file)
            SETTINGS.mtx = calib_data['mtx']
            SETTINGS.dist = calib_data['dist']
            data_file.close()

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
            black and white thresholded image out of DATA.processed_image
            into DATA.threshed_images.
        """

        if CFG.CAMERA_CALIBRATION_UNDISTORT:
            #DATA.processed_image = cv.subtract(DATA.processed_image, DATA.calibration_image)
            DATA.processed_image = cv.undistort(DATA.processed_image, SETTINGS.mtx, SETTINGS.dist, None, SETTINGS.mtx)

        # DATA.processed_image.shape[2] gives the number of channels
        DATA.BGRchannels = cv.split(DATA.processed_image)
        #print DATA.BGRchannels
        DATA.blue_image= DATA.BGRchannels[0]
        DATA.green_image = DATA.BGRchannels[1]
        DATA.red_image = DATA.BGRchannels[2]

        # This line creates a hue-saturation-value image
        DATA.hsv = cv.cvtColor(DATA.processed_image, cv.COLOR_BGR2HSV)
        #print DATA.processed_image.shape
        #print DATA.hsv
        #print DATA.hsv.shape
        #print cv.split(DATA.hsv)
        DATA.HSVchannels = cv.split(DATA.hsv)
        #print DATA.HSVchannels
        DATA.hue_image = DATA.HSVchannels[0]
        DATA.sat_image = DATA.HSVchannels[1]
        DATA.val_image = DATA.HSVchannels[2]

        shape = DATA.hue_image.shape
        for i in range(len(SETTINGS.thresholds)):
            DATA.red_threshed_image = np.eye(*shape)
            DATA.blue_threshed_image = np.eye(*shape)
            DATA.green_threshed_image = np.eye(*shape)
            DATA.hue_threshed_image = np.eye(*shape)
            DATA.sat_threshed_image = np.eye(*shape)
            DATA.val_threshed_image = np.eye(*shape)

            DATA.threshed_images[i] = np.eye(*shape)

            try:
                DATA.red_threshed_image = cv.inRange(
                    DATA.red_image, SETTINGS.thresholds[i]["low_red"], SETTINGS.thresholds[i]["high_red"], DATA.red_threshed_image)
                DATA.blue_threshed_image = cv.inRange(
                    DATA.blue_image, SETTINGS.thresholds[i]["low_blue"], SETTINGS.thresholds[i]["high_blue"], DATA.blue_threshed_image)
                DATA.green_threshed_image = cv.inRange(
                    DATA.green_image, SETTINGS.thresholds[i]["low_green"], SETTINGS.thresholds[i]["high_green"], DATA.green_threshed_image)
                DATA.hue_threshed_image = cv.inRange(
                    DATA.hue_image, SETTINGS.thresholds[i]["low_hue"], SETTINGS.thresholds[i]["high_hue"], DATA.hue_threshed_image)
                DATA.sat_threshed_image = cv.inRange(
                    DATA.sat_image, SETTINGS.thresholds[i]["low_sat"], SETTINGS.thresholds[i]["high_sat"], DATA.sat_threshed_image)
                DATA.val_threshed_image = cv.inRange(
                    DATA.val_image, SETTINGS.thresholds[i]["low_val"], SETTINGS.thresholds[i]["high_val"], DATA.val_threshed_image)
            except:
                pass

            #mnożenie do wynikowego threshold_iamges
            DATA.threshed_images[i] = cv.multiply(
                DATA.red_threshed_image, DATA.green_threshed_image, DATA.threshed_images[i])
            DATA.threshed_images[i] = cv.multiply(
                DATA.threshed_images[i], DATA.blue_threshed_image, DATA.threshed_images[i])
            DATA.threshed_images[i] = cv.multiply(
                DATA.threshed_images[i], DATA.hue_threshed_image, DATA.threshed_images[i])
            DATA.threshed_images[i] = cv.multiply(
                DATA.threshed_images[i], DATA.sat_threshed_image, DATA.threshed_images[i])
            DATA.threshed_images[i] = cv.multiply(
                DATA.threshed_images[i], DATA.val_threshed_image, DATA.threshed_images[i])

        #DATA.threshed_images = cv.dilate(DATA.threshed_images, None, iterations=2)

        #cv.imshow(DATA.threshed_images)
        # erozja dylatacja w zaleznosci od potrzeb
        #cv.erode(DATA.threshed_images, DATA.threshed_images, iterations = 1)
        #cv.dilate(DATA.threshed_images, DATA.threshed_images, iterations = 1)
        #kernel = np.ones((5,5),np.uint8)
        #for i in range(len(DATA.threshed_images)):
        #    erosion = cv.erode(DATA.threshed_images[i],kernel,iterations = 1)
        #    dilation = cv.dilate(DATA.threshed_images[i],kernel,iterations = 1)

    def check_LED(self, x1, y1, x2, y2):
        #sprawdzenie, czy led są w bliskiej odległości

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
        LED = [0 for k in range(len(SETTINGS.thresholds))]

        for i in range(len(DATA.threshed_images)):
            # Create a copy image of thresholds then find contours on that image
            DATA.copy = DATA.threshed_images[i].copy() # copy threshed image

            # find all of the contours
            _, contours, _ = cv.findContours(DATA.copy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            # znajdz najwiekszy kontur
            # this is the standard algorithm: #zastąpic sortowaniem np.sort() lub sorted
            
            if len(contours) > 0:
                """ biggest = contours[0]
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
                """
                #to samo : cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
                cnts = sorted(contours, key=cv.contourArea, reverse=True)
                biggest = cnts[0]

                # umieszczenie bouding rect na konturze
                br = cv.boundingRect(biggest)

                # Make a bounding box around the biggest blob
                upper_left = (br[0], br[1])
                lower_left = (br[0], br[1] + br[3])
                lower_right = (br[0] + br[2], br[1] + br[3])
                upper_right = (br[0] + br[2], br[1])
                cv.polylines(DATA.base_image, [np.array([upper_left,lower_left,lower_right,upper_right], dtype=np.int32)],
                            1, (255, 0, 0))
                cv.polylines(DATA.threshed_images[i], [np.array([upper_left,lower_left,lower_right,upper_right], dtype=np.int32)],
                            1, (255, 0, 0))
                cv.polylines(DATA.threshed_images[i], [np.array([upper_left,lower_left,lower_right,upper_right], dtype=np.int32)],
                            1, (255, 0, 0))

                #zachowaj blob( contour ) dla diody
                LED[i] = biggest
        #print biggest
        #print second_biggest
        # liczenie momentu dla każdego z konturów
        moment0 = cv.moments(LED[0])
        moment1 = cv.moments(LED[1])
        #h, w, c = DATA.base_image.shape
        if (moment0['m00'] > 0):
            center_x = moment0['m10']/moment0['m00']
            center_x = map_img_to_real(center_x, DATA.area_width_captured, CFG.AREA_WIDTH_REAL)

            center_y = moment0['m01']/moment0['m00']
            center_y = map_img_to_real(center_y, DATA.area_height_captured, CFG.AREA_HEIGHT_REAL)
            DATA.led1_pos = (center_x, center_y)
        else:
            DATA.led1_pos = None

        if (moment1['m00'] > 0):
            second_center_x = moment1['m10']/moment1['m00']
            second_center_x = map_img_to_real(second_center_x, DATA.area_width_captured, CFG.AREA_WIDTH_REAL)

            second_center_y = moment1['m01']/moment1['m00']
            second_center_y = map_img_to_real(second_center_y, DATA.area_height_captured, CFG.AREA_HEIGHT_REAL)
            DATA.led2_pos = (second_center_x, second_center_y)
        else:
            DATA.led2_pos = None


        #if these blobs have areas > 0, then calculate the average of their centroids
        if (moment0['m00'] > 0 and moment1['m00'] > 0):

            #led_check = self.check_LED(center_x, center_y, second_center_x, second_center_y)
            #led_check was inside
            if (True):
                DATA.robot_center = ((center_x + second_center_x)/2.0, (center_y + second_center_y)/2.0)
                h, w, c = DATA.base_image.shape
                robot_centre_img = map_point_to_img(DATA.robot_center, (h, w), (CFG.AREA_HEIGHT_REAL, CFG.AREA_WIDTH_REAL))
                led1_pos_img = map_point_to_img(DATA.led1_pos, (h, w), (CFG.AREA_HEIGHT_REAL, CFG.AREA_WIDTH_REAL))
                led2_pos_img = map_point_to_img(DATA.led2_pos, (h, w), (CFG.AREA_HEIGHT_REAL, CFG.AREA_WIDTH_REAL))
                cv.circle(DATA.base_image, robot_centre_img, 10, (255, 255, 0))
                cv.circle(DATA.threshed_images[0], robot_centre_img, 10, (255, 255, 0))
                DATA.heading =  math.atan2(led1_pos_img[0]-led2_pos_img[0], led1_pos_img[1]-led2_pos_img[1]) + -np.pi
                DATA.heading = -1 * math.atan2(math.sin(DATA.heading), math.cos(DATA.heading))
                DATA.detected = True
            else:
                DATA.robot_center = None
                DATA.heading = None
                DATA.detected = False

        else:
            DATA.robot_center = None
            DATA.heading = None
            DATA.detected = False

    def detectAndTrack(self, SETTINGS, DATA, ROBOT):
        """ this function organizes all of the processing
            done for each image from a camera type 2Led robot """

        if DATA.base_image is None:
            raise Exception("No base_iamge provided. {->detectAndTrack2LedRobot}")
        DATA.processed_image = DATA.base_image
        #DATA.processed_image = cv.bilateralFilter(DATA.processed_image, 25, 25, 25)
        
        if DATA.created_images == False:
            self.init_images(DATA, SETTINGS)
            DATA.created_images = True
        
        self.threshold_image(DATA, SETTINGS)
        self.find_2Led(DATA, SETTINGS)

        key_press_raw = cv.waitKey(1) # gets a raw key press
        key_press = key_press_raw & 0xFF # same as 255# sets all but the low 8 bits to 0
        
        # Handle key presses only (255 = "no key pressed")
        if key_press != 255:
            self.check_key_press(key_press, DATA, SETTINGS)

        h, w, c = DATA.base_image.shape
        x, y = DATA.target
        # updatee the displays:
        xI = map_real_to_img(x, w, CFG.AREA_WIDTH_REAL)
        yI = map_real_to_img(y, h, CFG.AREA_HEIGHT_REAL)
        target = (xI, yI)

        cv.circle(DATA.base_image, target, 3, (255,0,0), 2, -1)
        cv.imshow('Tracking and recognition', DATA.base_image)
        # Currently selected threshold image:
        for i in range(len(DATA.threshed_images)):
            cv.imshow('Threshold_%d' % i, DATA.current_threshold[i])
        if (DATA.robot_center and DATA.led2_pos) != None:
            return ROBOT.update(time.clock() - self.time, DATA.robot_center, DATA.led1_pos, DATA.led2_pos, DATA.heading)
        else: return ROBOT

    # Callback zachowanie dla przycisków i z pętlą dla przyciskow ustawiajacy wyswietlany thresh
    def check_key_press(self, key_press, DATA, SETTINGS):

        SETTINGS.last_key_pressed = key_press

        # if it was ESC, make it 'q'
        if key_press == 27:
            key_press = ord('q')

        # if a 'q' or ESC was pressed, we quit
        if key_press == ord('q'): 
            print("Quitting")
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
            print(" a    : show hue_image image in threshold window")
            print(" s    : show saturation image in threshold window")
            print(" p    : draw robot path")
            print(" d    : show value image in threshold window")
            print(" z    : show thresholded hue_image image in threshold window")
            print(" x    : show thresholded saturation image in threshold window")
            print(" c    : show thresholded value image in threshold window")
            print(" v    : saves threshold values to file")
            print(" b    : loads threshold values from pikle file")

        elif key_press == ord('v'):
            save_thresholds(SETTINGS.thresholds, CFG.THRESHOLDS_FILE_PATH)

        elif key_press == ord('b'):
            load_thresholds(SETTINGS.thresholds, CFG.THRESHOLDS_FILE_PATH)

        elif key_press == ord('p'):
            generate_path_image(DATA)
            
        # threshold keypresses:
        elif key_press in list(DATA.key_dictionary.keys()):
            DATA.current_threshold = DATA.key_dictionary[key_press]
    
