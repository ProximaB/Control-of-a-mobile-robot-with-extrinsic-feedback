import cv2 as cv
import numpy as np
import sys
sys.path.insert(0, r'./TadroBeaconTracker/tadro-tracker/2Led/')
from logger import *
from statusWindow import statusWindowText
from robot import Robot2Led

# class robotSimulator:
#Przekształcić do klasy, która będzie przechowywała stan i na wywołanie nextframe(input values for model)
# zwróci kolejną klatkę,
W_HEIGHT = 640
W_WIDTH = 1280
D_PADDING_HORIZONTAL = (150, 10) #(L,R)
D_PADDING_VERTICAL = (10, 10)
FONT = cv.FONT_HERSHEY_SIMPLEX
    
D_WIDTH = W_WIDTH - D_PADDING_HORIZONTAL[0] - D_PADDING_HORIZONTAL[1]
D_HEIGHT = W_HEIGHT - D_PADDING_VERTICAL[0] - D_PADDING_VERTICAL[1]

LED_RADIUS = 5
LED_THICKNES = 7
ROBOT_THICKENES = 3

def draw_robot_position(robot : Robot2Led, frame):
    sw = statusWindowText(frame)
    sw.drawData((50,50), 1.23, 10, 1.42, (255,0,0))
    
    led1_pos, led2_pos, time, robot_center, heading, diamater = robot.unpack()
    #leds
    cv.circle(frame, led1_pos, LED_RADIUS, (0, 255, 0), LED_THICKNES)
    cv.circle(frame, led2_pos, LED_RADIUS, (0, 0, 255), LED_THICKNES)
    #robot circle
    cv.circle(frame, robot_center, diamater, (0, 0, 0), ROBOT_THICKENES)

    

win_frame = np.ones((W_HEIGHT, W_WIDTH, 3), dtype='uint8')
display_frame = np.ones((D_HEIGHT, D_WIDTH, 3), dtype='uint8') *255 # white plane

#Symulacja Robota
# -> wrzucamy model z potrzebnymi parametrami, ktory zwraca pozycje w danym czasie
robot = Robot2Led(20, (500, 500), (480, 480), (520, 520), np.pi/2, 45)
#rysowanie_pozycji robota
draw_robot_position(robot, display_frame)

# nakładanie display_frame na win_frame
win_frame[D_PADDING_VERTICAL[0] : - D_PADDING_VERTICAL[1], D_PADDING_HORIZONTAL[0] : - D_PADDING_HORIZONTAL[1], ] = display_frame
# wypisywanie statusu
sw = statusWindowText(win_frame)
sw.drawData((100,200), 1.23, 10, 1.42)

cv.imshow('result', win_frame)
cv.waitKey(0)