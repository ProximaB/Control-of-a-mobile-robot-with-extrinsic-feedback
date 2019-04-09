import cv2 as cv
import sys
import numpy as np
import pickle
import math
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
from logger import *
import operator

def add_t(a, b):
    '''dodanie dwoch punktow, tuple '''
    return tuple(map(operator.add, a, b))

def sub_t(a, b):
    '''dodanie dwoch punktow, tuple '''
    return tuple(map(operator.sub, a, b))

def save_image(image, fileName, path):
    try:
        cv.imwrite(f'{path}\\{fileName}.png', image)
        log_info('Zapis obrazu zakończony powodzeniem.\n'
                f'File path: {path}\{fileName}.bmp')
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
    finally:
        # aktualizacja pozycji sliderów
        for j in range(len(thresholds)):
            for x in ['low_red', 'high_red', 'low_green', 'high_green', 'low_blue', 'high_blue']:
                            #'low_hue', 'high_hue', 'low_sat', 'high_sat', 'low_val', 'high_val']:
                cv.setTrackbarPos(x, f'Sliders_{j}', thresholds[j][x])

    
def generate_path_image(DATA, step = 1):
    #makes the output image produce RGBA (A for Alpha, allowing for transparent pixels)
    #instead of just RBG like the input image. 4 channels instead of three
    shape = (DATA.processed_image.shape[0], DATA.processed_image.shape[1], 3)
    path_image = np.ones(shape)
    col = (0,0,0)
    counter = 0
   # for i, unpackedRobot in enumerate(DATA.robot_data):
    for i in range(0, len(DATA.robot_data), step):
        unpackedRobot = DATA.robot_data[i]
        if len(unpackedRobot) == 7:
            led1_pos, led2_pos, time, robot_center, heading, diamater, axle_len = unpackedRobot
        else:
            time, robot_center, heading, diamater, axle_len = unpackedRobot

        if (robot_center== None):
            continue
        '''
        if (counter == 0):
            col = np.array([255, 255, x[0]%256], copy=True)
        elif(counter == 1):
            col = np.array([x[0]%256, 255, 255], copy=True)
        elif(counter == 2):
            col = np.array([255, x[0]%256, 255], copy=True)
            
        if (x[0]%256 == 0):
                counter += 1
                counter = counter%3
        '''

        if (counter == 0):
            col = (255, 0, i%256)
        elif(counter == 1):
            col = (i%256, 0, 255)
        elif(counter == 2):
            col = (0, i%256, 255)
            
        if (i%256 == 0):
                counter += 1
                counter = counter%3
                
        #led2 = led2_pos
        #led1 = led1_pos
        #angle of arrow in radians
        #arrow_angle = .3
        #rotating the led1 LED about the front LED to make an arrow
        #right_shift_led1_x = int(led2[0] + (led1[0] -right_shift_led1_x = int(led2[0] + (led1[0] -right_shift_led1_x = int(led2[0] + (led1[0] - led2[0])*math.cos(arrow_angle) - (led1[1] - led2[1])*math.sin(arrow_angle))
        #right_shift_led1_y = int(led2[1] + (led1[1] - led2[1])*math.cos(arrow_angle) - (led1[0] - led2[0])*math.sin(arrow_angle))

        #left_shift_led1_x = int(led2[0] + (led1[0] - led2[0])*math.cos(-1*arrow_angle) - (led1[1] - led2[1])*math.sin(-1*arrow_angle))
        #left_shift_led1_y = int(led2[1] + (led1[1] - led2[1])*math.cos(-1*arrow_angle) - (led1[0] - led2[0])*math.sin(-1*arrow_angle))
        
        centre = robot_center
        head_point = add_t(centre, (20*math.cos(heading), 20*math.sin(heading)))
        head_point = tuple(map(round, head_point))
        cv.line(path_image, centre, head_point, col, 2)
        cv.circle(path_image, centre, 5, (255,255,0), 2)
        #cv.line(path_image, (right_shift_led1_x, right_shift_led1_y), led2, col, 2)
        #cv.line(path_image, (left_shift_led1_x, left_shift_led1_y), led2, col, 2)        
        #log_print col
        #cv.circle(path_image, x[1], 1, copy.copy(col))
        #cv.imshow('Path_Image', path_image)
    return path_image

def draw_path_image(image, data):
    #makes the output image produce RGBA (A for Alpha, allowing for transparent pixels)
    #instead of just RBG like the input image. 4 channels instead of three
    shape = (image.shape[0], image.shape[1], 3)
    path_image = np.zeros(shape)
    col = (0,0,0)
    counter = 0
    for i, robot in enumerate(data):
        if (robot.robot_center == None):
            continue
        '''
        if (counter == 0):
            col = np.array([255, 255, x[0]%256], copy=True)
        elif(counter == 1):
            col = np.array([x[0]%256, 255, 255], copy=True)
        elif(counter == 2):
            col = np.array([255, x[0]%256, 255], copy=True)
            
        if (x[0]%256 == 0):
                counter += 1
                counter = counter%3
        '''

        if (counter == 0):
            col = (255, 0, i%256)
        elif(counter == 1):
            col = (i%256, 0, 255)
        elif(counter == 2):
            col = (0, i%256, 255)
            
        if (i%256 == 0):
                counter += 1
                counter = counter%3
                
        led2 = robot.led2_pos
        led1 = robot.led1_pos
        #angle of arrow in radians
        arrow_angle = .3
        #rotating the led2 LED about the led1 LED to make an arrow
        right_shift_led2_x = int(led1[0] + (led2[0] - led1[0])*math.cos(arrow_angle) - (led2[1] - led1[1])*math.sin(arrow_angle))
        right_shift_led2_y = int(led1[1] + (led2[1] - led1[1])*math.cos(arrow_angle) - (led2[0] - led1[0])*math.sin(arrow_angle))

        left_shift_led2_x = int(led1[0] + (led2[0] - led1[0])*math.cos(-1*arrow_angle) - (led2[1] - led1[1])*math.sin(-1*arrow_angle))
        left_shift_led2_y = int(led1[1] + (led2[1] - led1[1])*math.cos(-1*arrow_angle) - (led2[0] - led1[0])*math.sin(-1*arrow_angle))

        cv.line(path_image, led2, led1, col, 2)
        cv.circle(path_image, led1 - led2, 5, (255,255,0), 2)
        #cv.line(path_image, (right_shift_led2_x, right_shift_led2_y), led1, col, 2)
        #cv.line(path_image, (left_shift_led2_x, left_shift_led2_y), led1, col, 2)        
        #log_print col
        #cv.circle(path_image, x[1], 1, copy.copy(col))
    #cv.imshow('Path_Image', image)
    return path_image

def map_real_to_img(valueReal, imgMax, realMax):
    # x = xR * k
    # k = xw / xRw
    return round(valueReal * imgMax/float(realMax))

def map_point_to_img(pointReal, imgMaxTuple, realMaxTuple):
    x = round(pointReal[0] * imgMaxTuple[1]/float(realMaxTuple[1])) # x * imgW / realW
    y = round(pointReal[1] * imgMaxTuple[0]/float(realMaxTuple[0]))
    return (x, y)

def map_img_to_real(valueImg, imgMax, realMax):
    # x = xR * k
    # k = xw / xRw
    return valueImg * realMax/float(imgMax)

def map_point_to_real(pointImg, imgMaxTuple, realMaxTuple):
    x = round(pointImg[0] * realMaxTuple[1]/float(imgMaxTuple[1]))
    y = round(pointImg[1] * realMaxTuple[0]/float(imgMaxTuple[0]))
    return (x, y)