import cv2 as cv
import sys
import numpy as np
import pickle
import math
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
from logger import *

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
            for x in ['low_red', 'high_red', 'low_green', 'high_green', 'low_blue', 'high_blue',
                            'low_hue', 'high_hue', 'low_sat', 'high_sat', 'low_val', 'high_val']:
                cv.setTrackbarPos(x, f'Sliders_{j}', thresholds[j][x])

    
def generate_path_image(DATA):
    #makes the output image produce RGBA (A for Alpha, allowing for transparent pixels)
    #instead of just RBG like the input image. 4 channels instead of three
    shape = (DATA.processed_image.shape[0], DATA.processed_image.shape[1], 3)
    path_image = np.zeros(shape)
    col = (0,0,0)
    counter = 0
    for i, robot in enumerate(DATA.robot_data):
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
                
        back = robot.led2_pos
        front = robot.led1_pos
        #angle of arrow in radians
        arrow_angle = .3
        #rotating the back LED about the front LED to make an arrow
        right_shift_back_x = int(front[0] + (back[0] - front[0])*math.cos(arrow_angle) - (back[1] - front[1])*math.sin(arrow_angle))
        right_shift_back_y = int(front[1] + (back[1] - front[1])*math.cos(arrow_angle) - (back[0] - front[0])*math.sin(arrow_angle))

        left_shift_back_x = int(front[0] + (back[0] - front[0])*math.cos(-1*arrow_angle) - (back[1] - front[1])*math.sin(-1*arrow_angle))
        left_shift_back_y = int(front[1] + (back[1] - front[1])*math.cos(-1*arrow_angle) - (back[0] - front[0])*math.sin(-1*arrow_angle))

        cv.line(path_image, back, front, col, 2)
        cv.circle(path_image, front, 5, (255,255,0), 2)
        cv.line(path_image, (right_shift_back_x, right_shift_back_y), front, col, 2)
        cv.line(path_image, (left_shift_back_x, left_shift_back_y), front, col, 2)        
        #print col
        #cv.circle(path_image, x[1], 1, copy.copy(col))
    cv.imshow('Path_Image', path_image)
    return path_image