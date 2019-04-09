""#line:1
import numpy as np #line:2
import cv2 as cv #line:3
import math #line:4
from math import cos ,sin #line:5
import copy #line:6
import sys #line:7
from os .path import normpath #line:8
from functools import partial #line:9
import pickle #line:10
from datetime import datetime #line:11
import time #line:12
import matplotlib .pyplot as plt #line:13
from scipy .interpolate import interp1d #line:14
from scipy .interpolate import BSpline ,make_interp_spline #line:15
from skimage import exposure #line:16
import cv2 .aruco as aruco #line:17
''' Import custom modules '''#line:18
sys .path .insert (0 ,r'./TadroBeaconTracker/tadro-tracker/2Led/')#line:20
from config import D as CFG #line:22
sys .path .insert (0 ,r'./TadroBeaconTracker/tadro-tracker/2Led/trackers')#line:24
from tracker2Led import Track2Led #line:26
from trackerArruco import TrackArruco #line:28
from robot import Robot ,Robot2Led ,RobotAruco ,Robot2LedBicycle #line:30
from logger import *#line:32
from utils import *#line:34
from statusWindow import statusWindow #line:36
from PID import PID as pid #line:38
sys .path .insert (0 ,r'./TadroBeaconTracker/tadro-tracker/2Led/Symulator')#line:40
from robotSimulator2Led import robotSimulationEnv2Led ,robotSimulationEnv2LedBicycle #line:43
from robotSimulatorAruco import robotSimulationEnvAruco #line:45
from RobotModel2Wheels import RobotModel2Wheels #line:48
from BicyclePCtrl import BicyclePCtrl ,DiffCtrl #line:50
class Settings (object ):#line:52
    pass #line:53
class Data (object ):#line:55
    pass #line:56
class TrackerBootstrap :#line:58
    def __init__ (OO00O000OOOO00OOO ,OOOO0O000O0O0O0OO ,O000OO0O00O0O0O00 ):#line:59
        OO00O000OOOO00OOO .SETTINGS =OOOO0O000O0O0O0OO #line:60
        OO00O000OOOO00OOO .DATA =O000OO0O00O0O0O00 #line:61
    def setup_thresholds_sliders (OOO0O0000000O0000 ):#line:63
        OO0OOO00OO0OO0000 =OOO0O0000000O0000 .SETTINGS #line:64
        OO00OOOO00000O00O =OOO0O0000000O0000 .DATA #line:65
        """Create windows, and set thresholds, Tracking and recognition, Threshold_i, Sliders_i, i->[0,1] or more"""#line:67
        OO0OOO00OO0OO0000 .thresholds [CFG .LEFT_LD ]={'low_red':0 ,'high_red':255 ,'low_green':0 ,'high_green':255 ,'low_blue':0 ,'high_blue':255 }#line:70
        OO0OOO00OO0OO0000 .thresholds [CFG .RIGHT_LD ]={'low_red':0 ,'high_red':255 ,'low_green':0 ,'high_green':255 ,'low_blue':0 ,'high_blue':255 }#line:77
        cv .namedWindow ('Tracking and recognition');cv .moveWindow ('Tracking and recognition',0 ,0 )#line:82
        cv .createTrackbar ('0 : OFF \n1 : ON','Tracking and recognition',0 ,1 ,OOO0O0000000O0000 .switch )#line:85
        for OOOO0OOO0O000000O in range (len (OO0OOO00OO0OO0000 .thresholds )):#line:88
            cv .namedWindow (f'Threshold_{OOOO0OOO0O000000O}')#line:89
            if CFG .HALF_SIZE :#line:90
                CFG .THR_WIND_OFFSET /=2 #line:91
            cv .moveWindow (f'Threshold_{OOOO0OOO0O000000O}',CFG .THR_WIND_OFFSET [0 ]+(OOOO0OOO0O000000O *CFG .THR_WIND_SLF_OFFSET ),CFG .THR_WIND_OFFSET [1 ])#line:93
            cv .namedWindow (f'Sliders_{OOOO0OOO0O000000O}')#line:95
            if CFG .HALF_SIZE :#line:96
                CFG .SLD_WIND_OFFSET /=2 #line:97
            cv .moveWindow (f'Sliders_{OOOO0OOO0O000000O}',CFG .SLD_WIND_OFFSET [0 ]+(OOOO0OOO0O000000O *CFG .SLD_WIND_SLF_OFFSET ),CFG .SLD_WIND_OFFSET [1 ])#line:99
            for O000O00OO0OO00OOO in OO0OOO00OO0OO0000 .thresholds [OOOO0OOO0O000000O ].keys ():#line:102
                cv .createTrackbar (O000O00OO0OO00OOO ,'Sliders_%d'%OOOO0OOO0O000000O ,OO0OOO00OO0OO0000 .thresholds [OOOO0OOO0O000000O ][O000O00OO0OO00OOO ],255 ,partial (OOO0O0000000O0000 .change_slider ,OO0OOO00OO0OO0000 .thresholds ,OOOO0OOO0O000000O ,O000O00OO0OO00OOO ))#line:104
        """
        # jeden ze sposobów stworzenia wielu sliderów
            def create_slider_callback(thresholds, i, thresh_name):
                return lambda x: change_slider(thresholds, i, thresh_name, x)

            for thresh_name in thresholds[i].keys():
                cv.createTrackbar(thresh_name, 'Sliders_%d' % i, thresholds[i][thresh_name], 255,
            (lambda x: create_slider_callback(thresholds, i, thresh_name))(i))
            #domknciecie, zachowuje context dla i
        """#line:114
        cv .setMouseCallback ('Tracking and recognition',OOO0O0000000O0000 .onMouse ,OO00OOOO00000O00O )#line:116
        OO0OOO00OO0OO0000 .last_key_pressed =255 #line:117
    def onMouse (O0O0O0OO000000000 ,O000OOO0O0OOO0OOO ,OOO0OO00OO0OO00O0 ,O0O0O0OOO0O0OO0OO ,OOO0OOOO0O00O0OO0 ,OO0OOO00OO000OO00 ):#line:122
        ""#line:123
        if O000OOO0O0OOO0OOO ==cv .EVENT_LBUTTONDOWN :#line:125
            OOO0OO0OO0O00OO00 ,OO0OOOOOO00O0000O ,O0OOOOO0O00OOO0OO =O0O0O0OO000000000 .DATA .base_image .shape #line:126
            O0O0000O0OOOOOO0O =map_img_to_real (OOO0OO00OO0OO00O0 ,OO0OOOOOO00O0000O ,CFG .AREA_WIDTH_REAL )#line:127
            OOO000OO0O00OOOO0 =map_img_to_real (O0O0O0OOO0O0OO0OO ,OOO0OO0OO0O00OO00 ,CFG .AREA_HEIGHT_REAL )#line:128
            O0O0O0OO000000000 .DATA .target =(O0O0000O0OOOOOO0O ,OOO000OO0O00OOOO0 )#line:129
            log_print ('X, Y:',O0O0000O0OOOOOO0O ,OOO000OO0O00OOOO0 ,"    ",end =' ')#line:130
            (O00O00OOO0O000OO0 ,OOO0000O0OO0OOOO0 ,OOO0O00O00000O0O0 )=O0O0O0OO000000000 .DATA .processed_image [O0O0O0OOO0O0OO0OO ,OOO0OO00OO0OO00O0 ]#line:131
            log_print ('R, G, B: ',int (OOO0O00O00000O0O0 ),int (OOO0000O0OO0OOOO0 ),int (O00O00OOO0O000OO0 ),"    ",end =' ')#line:132
            (OOO0OO0OO0O00OO00 ,O0OO00000OOOO0OO0 ,O0OO00OOOOO0OO000 )=O0O0O0OO000000000 .DATA .hsv [O0O0O0OOO0O0OO0OO ,OOO0OO00OO0OO00O0 ]#line:133
            log_print ('H, S, V',int (OOO0OO0OO0O00OO00 ),int (O0OO00000OOOO0OO0 ),int (O0OO00OOOOO0OO000 ))#line:134
            O0O0O0OO000000000 .DATA .down_coord =(OOO0OO00OO0OO00O0 ,O0O0O0OOO0O0OO0OO )#line:135
        if O000OOO0O0OOO0OOO ==cv .EVENT_RBUTTONDOWN :#line:136
            (O00O00OOO0O000OO0 ,OOO0000O0OO0OOOO0 ,OOO0O00O00000O0O0 )=O0O0O0OO000000000 .DATA .processed_image [O0O0O0OOO0O0OO0OO ,OOO0OO00OO0OO00O0 ]#line:137
            OOOO0OO00O000O0OO =O0O0O0OO000000000 .SETTINGS .thresholds [0 ]#line:138
            if 0 <(O00O00OOO0O000OO0 )<255 :#line:139
                if 0 <(OOO0000O0OO0OOOO0 )<255 :#line:140
                    if 0 <(OOO0O00O00000O0O0 )<255 :#line:141
                        OOOO0OO00O000O0OO =O0O0O0OO000000000 .SETTINGS .thresholds [0 ]#line:142
                        O0000OO0000OOOO00 =CFG .MOUSE_CALIB_DIST #line:143
                        OOOO0OO00O000O0OO ['low_red']=int ((OOO0O00O00000O0O0 -O0000OO0000OOOO00 )%256 )#line:144
                        OOOO0OO00O000O0OO ['high_red']=int ((OOO0O00O00000O0O0 +O0000OO0000OOOO00 )%256 )#line:145
                        OOOO0OO00O000O0OO ['low_green']=int ((OOO0000O0OO0OOOO0 -O0000OO0000OOOO00 )%256 )#line:146
                        OOOO0OO00O000O0OO ['high_green']=int ((OOO0000O0OO0OOOO0 +O0000OO0000OOOO00 )%256 )#line:147
                        OOOO0OO00O000O0OO ['low_blue']=int ((O00O00OOO0O000OO0 -O0000OO0000OOOO00 )%256 )#line:148
                        OOOO0OO00O000O0OO ['high_blue']=int ((O00O00OOO0O000OO0 +O0000OO0000OOOO00 )%2556 )#line:149
            for O0O0O000O0OO000OO in range (len (O0O0O0OO000000000 .SETTINGS .thresholds )):#line:153
                for OOO0OO00OO0OO00O0 in ['low_red','high_red','low_green','high_green','low_blue','high_blue']:#line:156
                    cv .setTrackbarPos (OOO0OO00OO0OO00O0 ,f'Sliders_{O0O0O000O0OO000OO}',O0O0O0OO000000000 .SETTINGS .thresholds [O0O0O000O0OO000OO ][OOO0OO00OO0OO00O0 ])#line:157
            log_info ("Thresholds for left led updated.")#line:158
        if O000OOO0O0OOO0OOO ==cv .EVENT_RBUTTONUP :#line:160
            (O00O00OOO0O000OO0 ,OOO0000O0OO0OOOO0 ,OOO0O00O00000O0O0 )=O0O0O0OO000000000 .DATA .processed_image [O0O0O0OOO0O0OO0OO ,OOO0OO00OO0OO00O0 ]#line:161
            OOOO0OO00O000O0OO =O0O0O0OO000000000 .SETTINGS .thresholds [1 ]#line:162
            if 0 <(O00O00OOO0O000OO0 )<255 :#line:163
                if 0 <(OOO0000O0OO0OOOO0 )<255 :#line:164
                    if 0 <(OOO0O00O00000O0O0 )<255 :#line:165
                        OOOO0OO00O000O0OO =O0O0O0OO000000000 .SETTINGS .thresholds [1 ]#line:166
                        O0000OO0000OOOO00 =25 #line:167
                        OOOO0OO00O000O0OO ['low_red']=int ((OOO0O00O00000O0O0 -O0000OO0000OOOO00 )%256 )#line:168
                        OOOO0OO00O000O0OO ['high_red']=int ((OOO0O00O00000O0O0 +O0000OO0000OOOO00 )%256 )#line:169
                        OOOO0OO00O000O0OO ['low_green']=int ((OOO0000O0OO0OOOO0 -O0000OO0000OOOO00 )%256 )#line:170
                        OOOO0OO00O000O0OO ['high_green']=int ((OOO0000O0OO0OOOO0 +O0000OO0000OOOO00 )%256 )#line:171
                        OOOO0OO00O000O0OO ['low_blue']=int ((O00O00OOO0O000OO0 -O0000OO0000OOOO00 )%256 )#line:172
                        OOOO0OO00O000O0OO ['high_blue']=int ((O00O00OOO0O000OO0 +O0000OO0000OOOO00 )%256 )#line:173
            for O0O0O000O0OO000OO in range (len (O0O0O0OO000000000 .SETTINGS .thresholds )):#line:176
                for OOO0OO00OO0OO00O0 in ['low_red','high_red','low_green','high_green','low_blue','high_blue']:#line:179
                    cv .setTrackbarPos (OOO0OO00OO0OO00O0 ,f'Sliders_{O0O0O000O0OO000OO}',O0O0O0OO000000000 .SETTINGS .thresholds [O0O0O000O0OO000OO ][OOO0OO00OO0OO00O0 ])#line:180
            log_info ("Thresholds for right led updated.")#line:181
    def change_slider (O00O0OOO0OO00OOO0 ,O0O0OOOO0000O0OOO ,O00O0OOO00OOO00O0 ,O00O0O00OOO0OOOO0 ,OO00OOOOOOO0OO000 ):#line:185
        ""#line:186
        O0O0OOOO0000O0OOO [O00O0OOO00OOO00O0 ][O00O0O00OOO0OOOO0 ]=OO00OOOOOOO0OO000 #line:187
        log_print ('{name}: {val}'.format (name =O00O0O00OOO0OOOO0 ,val =O0O0OOOO0000O0OOO [O00O0OOO00OOO00O0 ][O00O0O00OOO0OOOO0 ]))#line:188
    def change_heading (O00O00O0OOOO0O0OO ,OO00O0000000O000O ):#line:190
        OO00OO00O0O00000O =OO00O0000000O000O *np .pi /180.0 #line:191
        O00O00O0OOOO0O0OO .DATA .targetHeading =OO00OO00O0O00000O #line:192
        log_print (f'targetHeading: {OO00O0000000O000O}')#line:193
    def switch (O0OO0O00O0O000OOO ,O0000O000OO00000O ):#line:195
        O0OO0O00O0O000OOO .SETTINGS .START =O0000O000OO00000O #line:196
        log_print (f'Settings.START: {O0000O000OO00000O}')#line:197
    def change_brighteness (O0O0000O000OOOO00 ,O00OO0OO00000000O ):#line:199
        O0O0000O000OOOO00 .SETTINGS .BRIGHTNESS =O00OO0OO00000000O #line:200
        log_print (f'Settings.Brightennes: {O00OO0OO00000000O}')#line:201
    def play_in_loop (O0O00O00000OO0000 ,O0OOO00000OOOOO0O ,OO0O0O0O0OOOOOOO0 ):#line:204
        ""#line:205
        OO0O0O0O0OOOOOOO0 +=1 #line:206
        O0OOO000OOOO000OO =7 #line:208
        if OO0O0O0O0OOOOOOO0 !=O0OOO00000OOOOO0O .get (O0OOO000OOOO000OO ):#line:209
            return False #line:210
        for _OO00OO000O0OOO000 in range (0 ,CFG .NUM_FRAMES_TO_SKIP ):#line:213
            O0OOO00000OOOOO0O .grab ()#line:214
        OO0O0O0O0OOOOOOO0 =CFG .NUM_FRAMES_TO_SKIP #line:215
        O0O00000OOO0OOO0O =1 #line:217
        O0OOO00000OOOOO0O .set (O0O00000OOO0OOO0O ,OO0O0O0O0OOOOOOO0 )#line:218
        return True #line:219
class ArucoTrackerBootstrap :#line:221
    def __init__ (OOOO0OO0O0OO000OO ,OO00OO0OOO0O00O0O ,O0O0O00OOO00O00O0 ):#line:222
        OOOO0OO0O0OO000OO .SETTINGS =OO00OO0OOO0O00O0O #line:223
        OOOO0OO0O0OO000OO .DATA =O0O0O00OOO00O00O0 #line:224
    def setup_thresholds_sliders (OO0OOOOOO000O0O0O ):#line:226
        OO0OO00O000OOOOOO =OO0OOOOOO000O0O0O .SETTINGS #line:227
        O000O0OOO0O0000O0 =OO0OOOOOO000O0O0O .DATA #line:228
        cv .namedWindow ('Tracking and recognition');cv .moveWindow ('Tracking and recognition',0 ,0 )#line:230
        cv .createTrackbar ('0 : OFF \n1 : ON','Tracking and recognition',0 ,1 ,OO0OOOOOO000O0O0O .switch )#line:232
        cv .setMouseCallback ('Tracking and recognition',OO0OOOOOO000O0O0O .onMouse ,O000O0OOO0O0000O0 )#line:234
        OO0OO00O000OOOOOO .last_key_pressed =255 #line:235
    def onMouse (OOO0000OO0OO0O0O0 ,OO0OOO0OO0000OOO0 ,OO00O00000O00O0OO ,OO000O00000OO0000 ,O00O0OO0O0OO00OOO ,O00OO00000O0OO0O0 ):#line:240
        ""#line:241
        if OO0OOO0OO0000OOO0 ==cv .EVENT_LBUTTONDOWN :#line:243
            O000OOO00OO0OOOOO ,OO0O0OOOOO00OO000 ,O00O00OO00O00000O =O00OO00000O0OO0O0 .base_image .shape #line:244
            O0OO0O00O00OO0O00 =map_img_to_real (OO00O00000O00O0OO ,OO0O0OOOOO00OO000 ,CFG .AREA_WIDTH_REAL )#line:245
            OO00O0000OO000OOO =map_img_to_real (OO000O00000OO0000 ,O000OOO00OO0OOOOO ,CFG .AREA_HEIGHT_REAL )#line:246
            OOO0000OO0OO0O0O0 .DATA .target =(O0OO0O00O00OO0O00 ,OO00O0000OO000OOO )#line:247
            log_print ('X, Y:',O0OO0O00O00OO0O00 ,OO00O0000OO000OOO ,"    ",end =' ')#line:248
            (OO00O0OO00OOO0OO0 ,O000OOO0OO0OOO00O ,OOO00OO0OO000OO0O )=OOO0000OO0OO0O0O0 .DATA .processed_image [OO000O00000OO0000 ,OO00O00000O00O0OO ]#line:249
            log_print ('R, G, B: ',int (OOO00OO0OO000OO0O ),int (O000OOO0OO0OOO00O ),int (OO00O0OO00OOO0OO0 ),"    ",end =' ')#line:250
            (O000OOO00OO0OOOOO ,OO000OO00OOOO0O00 ,OO0O000O0OOO0O0O0 )=OOO0000OO0OO0O0O0 .DATA .hsv [OO000O00000OO0000 ,OO00O00000O00O0OO ]#line:251
            log_print ('H, S, V',int (O000OOO00OO0OOOOO ),int (OO000OO00OOOO0O00 ),int (OO0O000O0OOO0O0O0 ))#line:252
            OOO0000OO0OO0O0O0 .DATA .down_coord =(OO00O00000O00O0OO ,OO000O00000OO0000 )#line:253
    def switch (OO00OOO00O0OO0O00 ,O000O0O0OO00OOOOO ):#line:255
        OO00OOO00O0OO0O00 .SETTINGS .START =O000O0O0OO00OOOOO #line:256
        log_print (f'Settings.START: {O000O0O0OO00OOOOO}')#line:257
import matplotlib .patches as mpatches #line:259
import matplotlib .pyplot as plt #line:260
def draw_plot (O0OO0OO00O00O000O ,OO000000O000O00OO ,O0O00O000O0OO0O0O ,OOO0OOOO0000O0O0O ,O0O0O0O0O00OO00OO ,xlabel ='time (s)',ylabel ='PID (PV)'):#line:262
    OO0O0O0O0OOOO000O =mpatches .Patch (color ='orange',label ='set point')#line:263
    OOOO0O000OO0O0OO0 =mpatches .Patch (color ='blue',label ='error')#line:264
    OOO000O0OO000O0O0 =np .array (O0O00O000O0OO0O0O )#line:266
    O000OO0OO0O00000O =np .linspace (OOO000O0OO000O0O0 .min (),OOO000O0OO000O0O0 .max (),300 )#line:267
    O0O000OOO0O0O0O0O =make_interp_spline (O0O00O000O0OO0O0O ,O0OO0OO00O00O000O )#line:271
    OOO0O0OO0000000OO =O0O000OOO0O0O0O0O (O000OO0OO0O00000O )#line:272
    O00OO00OO00000O0O =len (O0O00O000O0OO0O0O )#line:274
    O000OOO00000OO0OO =plt .figure (OOO0OOOO0000O0O0O )#line:275
    plt .plot (O000OO0OO0O00000O ,OOO0O0OO0000000OO )#line:276
    plt .plot (O0O00O000O0OO0O0O ,OO000000O000O00OO )#line:277
    plt .xlabel (xlabel )#line:280
    plt .ylabel (ylabel )#line:281
    plt .title (O0O0O0O0O00OO00OO )#line:282
    plt .legend (handles =[OO0O0O0O0OOOO000O ,OOOO0O000OO0O0OO0 ])#line:283
    plt .grid (True )#line:286
    return O000OOO00000OO0OO #line:287
def draw_path (O0O0O000OO000000O ,OOO0O0O0OO000OOO0 ,O0OOOOOOO00O0OOOO ,O0000OO00OOOOO00O ,xlabel ='time (s)',ylabel ='PID (PV)'):#line:289
    O0OO0OOO0O0O00O0O =plt .figure (O0OOOOOOO00O0OOOO )#line:290
    O0OOOOO00OO0O0O0O =O0OO0OOO0O0O00O0O .add_subplot (111 )#line:291
    O0OOOOO00OO0O0O0O .set_xlim (-5 ,105 )#line:292
    O0OOOOO00OO0O0O0O .set_ylim (55 ,-5 )#line:293
    plt .semilogy (OOO0O0O0OO000OOO0 ,O0O0O000OO000000O )#line:295
    plt .xlabel (xlabel )#line:297
    plt .ylabel (ylabel )#line:298
    plt .title (O0000OO00OOOOO00O )#line:299
    plt .grid (True )#line:301
    plt .show ()#line:302
    return O0OO0OOO0O0O00O0O #line:303
def warp_iamge_aruco (O00OOOOOOOO0O0OO0 ,OO00OOOOOO000000O ):#line:305
    O0OO0O00000OOO000 =O00OOOOOOOO0O0OO0 .copy ()#line:306
    OOOO0000OO00O0O00 =cv .cvtColor (O00OOOOOOOO0O0OO0 ,cv .COLOR_RGB2GRAY )#line:307
    OOOO0000OO00O0O00 =cv .bilateralFilter (OOOO0000OO00O0O00 ,15 ,15 ,15 )#line:308
    O0O0O0O0O000O0OOO =aruco .Dictionary_get (CFG .ARUCO_DICT )#line:311
    OO0O000OO000O000O =aruco .DetectorParameters_create ()#line:312
    OOO000O00OO000000 ,OOO000O00OOO0000O ,OOO00O0OOOO000O0O =aruco .detectMarkers (OOOO0000OO00O0O00 ,O0O0O0O0O000O0OOO ,parameters =OO0O000OO000O000O )#line:313
    if len (OOO000O00OO000000 )<4 :#line:315
       if len (OO00OOOOOO000000O .prevCorners )<4 :#line:316
           OO0OO00O00O0OO0O0 ,O0000OO0OO0O0O000 ,OOOO0OO000O00O00O =O0OO0O00000OOO000 .shape #line:317
           return O0OO0O00000OOO000 ,OO0OO00O00O0OO0O0 ,O0000OO0OO0O0O000 ,None #line:318
       OOO000O00OO000000 =OO00OOOOOO000000O .prevCorners #line:319
    O0OO0OO000O000O00 =0 #line:321
    if (len (OO00OOOOOO000000O .prevCorners )!=0 ):#line:322
        for O0000O0OOOOO000OO in range (4 ):#line:323
            O0OO0O0O00OOO0O0O ,O0OOO00O00O0O000O =sub_t (OOO000O00OO000000 [O0000O0OOOOO000OO ][0 ][0 ],OO00OOOOOO000000O .prevCorners [O0000O0OOOOO000OO ][0 ][0 ])#line:324
            O0OO0OO000O000O00 +=math .sqrt (O0OO0O0O00OOO0O0O **2 +O0OOO00O00O0O000O **2 )#line:325
        if O0OO0OO000O000O00 <CFG .WARP_TOLERANCE :#line:326
           OOO000O00OO000000 =OO00OOOOOO000000O .prevCorners #line:327
        else :#line:328
            log_print ("Movement affected affine trans.")#line:329
    OO00OOOOOO000000O .prevCorners =OOO000O00OO000000 #line:331
    O0O0OOO00000O00OO =aruco .drawDetectedMarkers (O00OOOOOOOO0O0OO0 ,OOO000O00OO000000 )#line:332
    O000000OOO0OO00O0 =(OOOOO0OO000OO00OO [0 ][0 ]for OOOOO0OO000OO00OO in OOO000O00OO000000 )#line:339
    OOOOOOO0OOO0O000O =np .stack (O000000OOO0OO00O0 )#line:340
    OOO0O00000O00O0O0 =np .zeros ((4 ,2 ),dtype ="float32")#line:341
    if len (OOOOOOO0OOO0O000O )==4 :#line:342
        OO000O0OOOO00000O =OOOOOOO0OOO0O000O .tolist ()#line:343
        OOO0O00O0O0O0OOOO =np .array ([OO000O0OOOO00000O [2 ],OO000O0OOOO00000O [0 ],OO000O0OOOO00000O [1 ],OO000O0OOOO00000O [3 ]],dtype ="int32"),#line:344
        for O0000O0OOOOO000OO in np .stack (OOOOOOO0OOO0O000O ):#line:345
            O0OO0O0O00OOO0O0O ,O0OOO00O00O0O000O =O0000O0OOOOO000OO .ravel ()#line:346
            cv .circle (O0O0OOO00000O00OO ,(O0OO0O0O00OOO0O0O ,O0OOO00O00O0O000O ),7 ,(255 ,0 ,0 ),-1 )#line:347
        cv .polylines (O0O0OOO00000O00OO ,OOO0O00O0O0O0OOOO ,True ,(0 ,255 ,0 ),2 )#line:348
    if CFG .MARKER_PREVIEW is True :cv .imshow (OO00OOOOOO000000O .markerPreviewWinName ,O0O0OOO00000O00OO )#line:350
    O000000O000O00OOO =OOOOOOO0OOO0O000O .sum (axis =1 )#line:352
    OOO0O00000O00O0O0 [0 ]=OOOOOOO0OOO0O000O [np .argmin (O000000O000O00OOO )]#line:353
    OOO0O00000O00O0O0 [2 ]=OOOOOOO0OOO0O000O [np .argmax (O000000O000O00OOO )]#line:354
    O00OOO00OOOO0000O =np .diff (OOOOOOO0OOO0O000O ,axis =1 )#line:356
    OOO0O00000O00O0O0 [1 ]=OOOOOOO0OOO0O000O [np .argmin (O00OOO00OOOO0000O )]#line:357
    OOO0O00000O00O0O0 [3 ]=OOOOOOO0OOO0O000O [np .argmax (O00OOO00OOOO0000O )]#line:358
    (O000O0O0OOO0O000O ,O00OO000OO0OOO0O0 ,O000000OO000O0O00 ,O0O000OO000OOO0OO )=OOO0O00000O00O0O0 #line:360
    O0O000000OOO000OO =np .sqrt (((O000000OO000O0O00 [0 ]-O0O000OO000OOO0OO [0 ])**2 )+((O000000OO000O0O00 [1 ]-O0O000OO000OOO0OO [1 ])**2 ))#line:362
    OOOOOOOOOOO000000 =np .sqrt (((O00OO000OO0OOO0O0 [0 ]-O000O0O0OOO0O000O [0 ])**2 )+((O00OO000OO0OOO0O0 [1 ]-O000O0O0OOO0O000O [1 ])**2 ))#line:363
    OO000O0OOOO000O00 =np .sqrt (((O00OO000OO0OOO0O0 [0 ]-O000000OO000O0O00 [0 ])**2 )+((O00OO000OO0OOO0O0 [1 ]-O000000OO000O0O00 [1 ])**2 ))#line:365
    O000OO00000000000 =np .sqrt (((O000O0O0OOO0O000O [0 ]-O0O000OO000OOO0OO [0 ])**2 )+((O000O0O0OOO0O000O [1 ]-O0O000OO000OOO0OO [1 ])**2 ))#line:366
    O0O00O0OO0O000000 =max (int (O0O000000OOO000OO ),int (OOOOOOOOOOO000000 ))#line:368
    OOOO0OO0OOOOO0OOO =max (int (OO000O0OOOO000O00 ),int (O000OO00000000000 ))#line:369
    O0O0000O00OO0OOO0 =np .array ([[0 ,0 ],[O0O00O0OO0O000000 -1 ,0 ],[O0O00O0OO0O000000 -1 ,OOOO0OO0OOOOO0OOO -1 ],[0 ,OOOO0OO0OOOOO0OOO -1 ]],dtype ="float32")#line:375
    O0OOOOOOOO0O00O00 =cv .getPerspectiveTransform (OOO0O00000O00O0O0 ,O0O0000O00OO0OOO0 )#line:377
    O0O0O00OOO0OO0O00 =cv .warpPerspective (O0OO0O00000OOO000 ,O0OOOOOOOO0O00O00 ,(O0O00O0OO0O000000 ,OOOO0OO0OOOOO0OOO ))#line:378
    return (O0O0O00OOO0OO0O00 ,OOOO0OO0OOOOO0OOO ,O0O00O0OO0O000000 ,O0OOOOOOOO0O00O00 )#line:380
def main_default ():#line:382
    OO0O0O000O0O0O0OO =Settings ()#line:388
    OO0O0O000O0O0O0OO .thresholds =[{},{}]#line:389
    OO0O0O000O0O0O0OO .START =0 #line:390
    OO0O0O000O0O0O0OO .BRIGHTNESS =CFG .BRIGHTNESS #line:391
    O0OO00O00OOO0O000 =Data ()#line:393
    O0OO00O00OOO0O000 .robot_data =[]#line:394
    O0OO00O00OOO0O000 .target =(0 ,0 )#line:395
    O0OO00O00OOO0O000 .targetHeading =0 #line:396
    O0OO00O00OOO0O000 .prevCorners =[]#line:397
    O0OO00O00OOO0O000 .area_height_captured =None #line:398
    O0OO00O00OOO0O000 .area_width_captured =None #line:399
    O0OO00O00OOO0O000 .doWarpImage =True #line:401
    OO0OO0O00O000OO00 ='Robot Path'#line:403
    cv .namedWindow (OO0OO0O00O000OO00 )#line:404
    cv .moveWindow (OO0OO0O00O000OO00 ,0 ,100 )#line:405
    O0OO0O0O0OO000O0O =O0OO00O00OOO0O000 .markerPreviewWinName ='Preview markers detect'#line:407
    cv .namedWindow (O0OO0O0O0OO000O0O )#line:408
    cv .moveWindow (O0OO0O0O0OO000O0O ,0 ,400 )#line:409
    if CFG .TRACKER_TYPE is CFG .LED_ENUM :#line:411
        O0O0OO0OOO0O00000 =Track2Led (O0OO00O00OOO0O000 )#line:412
        OOOOO0O00O0O00O00 =TrackerBootstrap (OO0O0O000O0O0O0OO ,O0OO00O00OOO0O000 )#line:413
    else :#line:414
        O0O0OO0OOO0O00000 =TrackArruco (O0OO00O00OOO0O000 )#line:415
        OOOOO0O00O0O00O00 =ArucoTrackerBootstrap (OO0O0O000O0O0O0OO ,O0OO00O00OOO0O000 )#line:416
    OOO00000OOOOO000O =None #line:417
    if CFG .SIMULATION :#line:422
        if CFG .TRACKER_TYPE is CFG .LED_ENUM :#line:424
            OOO00000OOOOO000O =Robot2Led (0 ,CFG .ROB_CNTR ,None ,None ,CFG .HEADING ,CFG .DIAMETER ,CFG .AXLE_LEN ,CFG .WHEEL_RADIUS )#line:426
            OOO00000OOOOO000O .calculate_led_pos ()#line:427
            OOOOO0O000OO0O000 =Robot2Led (0 ,CFG .ROB_CNTR ,None ,None ,CFG .HEADING ,CFG .DIAMETER ,CFG .AXLE_LEN ,CFG .WHEEL_RADIUS )#line:430
            OOOOO0O000OO0O000 .calculate_led_pos ()#line:431
            O00000O0OOOO0OO00 =RobotModel2Wheels (OOOOO0O000OO0O000 )#line:434
            OO000O0O0O0O0O00O =robotSimulationEnv2Led (O00000O0OOOO0OO00 )#line:435
            log_info ('Inicjalizacja sliderow do thresholdingu.')#line:439
            OOOOO0O00O0O00O00 .setup_thresholds_sliders ()#line:440
            if (CFG .AUTO_LOAD_THRESHOLDS ):#line:442
                load_thresholds (OO0O0O000O0O0O0OO .thresholds ,CFG .THRESHOLDS_FILE_PATH )#line:443
        else :#line:445
            OOO0OO0OOO0O000OO =aruco .Dictionary_get (CFG .ARUCO_DICT )#line:446
            OOO0OOO00O00OO00O =aruco .drawMarker (OOO0OO0OOO0O000OO ,id =CFG .ROBOT_ID ,sidePixels =CFG .ARUCO_SIDE_PIXELS )#line:447
            OOO00000OOOOO000O =RobotAruco (0 ,CFG .ROB_CNTR ,CFG .HEADING ,CFG .DIAMETER ,CFG .AXLE_LEN ,CFG .WHEEL_RADIUS )#line:450
            OOOOO0O000OO0O000 =RobotAruco (0 ,CFG .ROB_CNTR ,CFG .HEADING ,CFG .AXLE_LEN ,CFG .WHEEL_RADIUS )#line:452
            O00000O0OOOO0OO00 =RobotModel2Wheels (OOOOO0O000OO0O000 )#line:453
            OO000O0O0O0O0O00O =robotSimulationEnvAruco (O00000O0OOOO0OO00 ,OOO0OOO00O00OO00O )#line:454
            log_info ('Inicjalizacja sliderow do thresholdingu.')#line:456
            OOOOO0O00O0O00O00 .setup_thresholds_sliders ()#line:457
        if CFG .CAMERA_FEEDBACK :#line:459
            OO000O0O0O0O0O00O .simulate_return_image (0 ,0 ,0.01 )#line:460
            OO0O000OOO0000OO0 =cv .VideoCapture (CFG .VIDEO_PATH )#line:461
        else :#line:462
            OO0O000OOO0000OO0 =OO000O0O0O0O0O00O .simulate_return_image (0 ,0 ,0.01 )#line:463
    else :#line:464
        OO0O000OOO0000OO0 =cv .VideoCapture (CFG .VIDEO_PATH )#line:465
        if OO0O000OOO0000OO0 .isOpened ()is False :#line:467
            log_error ("Błąd podczas otwarcia filmu lub inicjalizacji kamery")#line:468
            return #line:469
        else :#line:470
            log_info ("Plik został poprawnie otwarty / Kamera zostala poprawnie zainicjalizowana.")#line:471
        for _OOO00OOO00O0OO000 in range (0 ,CFG .NUM_FRAMES_TO_SKIP ):#line:475
            OO0O000OOO0000OO0 .grab ()#line:476
        O000O0OOO00000000 =CFG .NUM_FRAMES_TO_SKIP #line:479
    O00000O0000OOOOO0 =pid (CFG .PROPORTIONAL1 ,CFG .INTEGRAL1 ,CFG .DERIVATIVE1 )#line:481
    O0O0O0OOO000OO000 =pid (CFG .PROPORTIONAL2 ,CFG .INTEGRAL2 ,CFG .DERIVATIVE2 )#line:482
    O00OOO00OO0OO0O0O =DiffCtrl (O00000O0000OOOOO0 ,O0O0O0OOO000OO000 ,OOO00000OOOOO000O )#line:484
    O00000O0000OOOOO0 .SetPoint =0 #line:486
    O00000O0000OOOOO0 .setSampleTime (0.02 )#line:487
    O00000O0000OOOOO0 .update (0 )#line:488
    O00000O0000OOOOO0 .setWindup (3.0 )#line:489
    O0O0O0OOO000OO000 .SetPoint =0 #line:491
    O0O0O0OOO000OO000 .setSampleTime (0.02 )#line:492
    O0O0O0OOO000OO000 .update (0 )#line:493
    O0O0O0OOO000OO000 .setWindup (3.0 )#line:494
    O0O000O0000OO0O0O =[[],[]]#line:496
    O0O0OOO000OO0OOO0 =[[],[]]#line:497
    O0000O00OO0O0OOOO =[[],[]]#line:498
    OOO000OO0000O0OOO =[[],[]]#line:499
    O0OOOO000O0O00O00 =True #line:501
    O0OO00O0OOOO0O000 =CFG .VEL #line:502
    OO0O0OO0O0O0O0O0O =False #line:503
    OOOOOOO0O00O0OOO0 =0.0 #line:505
    OO0OO00000OOO0OOO =0.0 #line:506
    while (True ):#line:508
        if CFG .SIMULATION :#line:509
            if OO0O0O000O0O0O0OO .START ==0 :#line:510
                if CFG .CAMERA_FEEDBACK :#line:511
                    OO000O0O0O0O0O00O .simulate_return_image (0 ,0 ,0.01 )#line:512
                    O0000O0O000000000 ,O000O00OO0000O000 =OO0O000OOO0000OO0 .read ()#line:513
                else :#line:514
                    O000O00OO0000O000 =OO000O0O0O0O0O00O .simulate_return_image (0 ,0 ,0.01 )#line:515
                if O0OO00O00OOO0O000 .doWarpImage is True :O0OO00O00OOO0O000 .base_image ,O0OO00O00OOO0O000 .area_height_captured ,O0OO00O00OOO0O000 .area_width_captured ,O00O00O00O0OO00O0 =warp_iamge_aruco (O000O00OO0000O000 ,O0OO00O00OOO0O000 )#line:517
                else :O0OO00O00OOO0O000 .base_image =cv .warpPerspective (O000O00OO0000O000 ,O00O00O00O0OO00O0 ,(O0OO00O00OOO0O000 .area_width_captured ,O0OO00O00OOO0O000 .area_height_captured ))#line:518
                """
                Podwyższenie jasności
                
                hsv = cv.cvtColor(DATA.base_image, cv.COLOR_BGR2HSV)
                max = np.max(hsv[:,:,2])
                
                dif = 255-max
                bright = SETTINGS.BRIGHTNESS
                bright = bright if dif-bright > 0 else dif

                hsv[:,:,2] += bright

                DATA.base_image = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
                
                """#line:535
                O0O0OO0OOO0O00000 .detectAndTrack (OO0O0O000O0O0O0OO ,O0OO00O00OOO0O000 ,OOO00000OOOOO000O )#line:536
                if cv .waitKey (1 )&0xFF ==ord ('q'):#line:537
                    break #line:538
                continue #line:539
        else :#line:540
            O0000O0O000000000 ,O000O00OO0000O000 =OO0O000OOO0000OO0 .read ()#line:541
            if not O0000O0O000000000 :#line:542
                log_warn ('Frame not grabbed. Continue...')#line:543
                continue #line:545
        """################## Zmienne wykorzystywane na potrzeby sterowania ###############"""#line:550
        OO00O0O000O00OOO0 ,OOO0OOOOOO0OOO0OO =O0OO00O00OOO0O000 .base_image .shape [:2 ]#line:551
        OO00OO0OOO0OO0O0O =math .sqrt (OO00O0O000O00OOO0 **2 +OOO0OOOOOO0OOO0OO **2 )#line:552
        O00OOOOO00O00OO00 =-O00000O0000OOOOO0 .output #line:553
        OOO0OO00000O00OO0 =float (O0O0O0OOO000OO000 .output /OO00OO0OOO0OO0O0O *O0OO00O0OOOO0O000 )#line:554
        OOO0OO00000O00OO0 =OOO0OO00000O00OO0 if OOO0OO00000O00OO0 <O0OO00O0OOOO0O000 else O0OO00O0OOOO0O000 #line:555
        OOO0OOOO00O000O00 =OOO00000OOOOO000O .diamater /2 +CFG .DIST #line:557
        OO000O0O00O0OO0OO =[(OOO0OOOO00O000O00 ,OOO0OOOO00O000O00 ),(CFG .AREA_WIDTH_REAL -OOO0OOOO00O000O00 ,CFG .AREA_HEIGHT_REAL -OOO0OOOO00O000O00 )]#line:558
        OO00OOOO000OO0000 ,O00000OO0O0OOO000 =OO000O0O00O0OO0OO [0 ]#line:559
        O0O000000OO00OO0O ,O0O00O00O000OO0OO =OO000O0O00O0OO0OO [1 ]#line:560
        O000OOOO0O00O0000 ,OO00OOO0OOOO0OO00 =OOO00000OOOOO000O .robot_center #line:561
        O0OOO0OOO00000O0O ,O00O0O00O0000OOOO =O0OO00O00OOO0O000 .target #line:562
        """################## Wyliczanie prędkości kół ###############"""#line:564
        if not O0OO00O00OOO0O000 .detected :#line:565
            O00O000O000000O0O =0 #line:566
            O0O0OOO0OOOOOOO0O =0 #line:567
        elif (O00000OO0O0OOO000 <OO00OOO0OOOO0OO00 <O0O00O00O000OO0OO and OO00OOOO000OO0000 <O000OOOO0O00O0000 <O0O000000OO00OO0O or OO0O0OO0O0O0O0O0O ):#line:568
            ''' Tutaj wyliczane są predkość kątowe dla każdego z kół robota. 
                Feedback od odlegosci i headingu, działający na kolejno prekość forward i prędkość rotational
            '''#line:573
            """ Następujące równania, zostały wyznaczone w pracy, zapewniają one odpowiednie sterowanie, pozwalające dotrzeć do celu w zależności
            od odchylenia i odelgłości do celu.
                outTheta wpływa na keirunek jazdy, outVel na wielkość prędkośći. 
            """#line:577
            O00O000O000000O0O =(-(2 *OOO0OO00000O00OO0 )-(O00OOOOO00O00OO00 *CFG .AXLE_LEN ))/2 *CFG .WHEEL_RADIUS #line:578
            O0O0OOO0OOOOOOO0O =(-(2 *OOO0OO00000O00OO0 )+(O00OOOOO00O00OO00 *CFG .AXLE_LEN ))/2 *CFG .WHEEL_RADIUS #line:579
            OO0O0OO0O0O0O0O0O =False #line:581
        else :#line:583
            O00O000O000000O0O =0 ;O0O0OOO0OOOOOOO0O =0 #line:585
            if O00000OO0O0OOO000 <O00O0O00O0000OOOO <O0O00O00O000OO0OO and OO00OOOO000OO0000 <O0OOO0OOO00000O0O <O0O000000OO00OO0O :#line:586
                if OO0OO00000OOO0OOO >20 *np .pi /180 :#line:588
                    O00O000O000000O0O =OOO0OO00000O00OO0 *0.5 ;O0O0OOO0OOOOOOO0O =-OOO0OO00000O00OO0 *0.5 #line:589
                elif OO0OO00000OOO0OOO <-20 *np .pi /180 :#line:590
                    O00O000O000000O0O =-OOO0OO00000O00OO0 *0.5 ;O0O0OOO0OOOOOOO0O =OOO0OO00000O00OO0 *0.5 #line:591
                else :OO0O0OO0O0O0O0O0O =True #line:592
        """################## Symulowanie stanowiska roboczego ###############"""#line:594
        if CFG .SIMULATION :#line:596
            if CFG .CAMERA_FEEDBACK :#line:597
                    OO000O0O0O0O0O00O .simulate_return_image (O00O000O000000O0O ,O0O0OOO0OOOOOOO0O ,0.01 )#line:598
                    O0000O0O000000000 ,O000O00OO0000O000 =OO0O000OOO0000OO0 .read ()#line:599
            else :#line:600
                O000O00OO0000O000 =OO000O0O0O0O0O00O .simulate_return_image (O00O000O000000O0O ,O0O0OOO0OOOOOOO0O ,0.01 )#line:601
        if O0OO00O00OOO0O000 .doWarpImage is True :#line:603
            O0OO00O00OOO0O000 .base_image ,O0OO00O00OOO0O000 .area_height_captured ,O0OO00O00OOO0O000 .area_width_captured ,O0OO00O00OOO0O000 .M =warp_iamge_aruco (O000O00OO0000O000 ,O0OO00O00OOO0O000 )#line:604
        else :#line:605
            O0OO00O00OOO0O000 .base_image =cv .warpPerspective (O000O00OO0000O000 ,O0OO00O00OOO0O000 .M ,(O0OO00O00OOO0O000 .area_width_captured ,O0OO00O00OOO0O000 .area_height_captured ))#line:606
        """################## Transformacja affiniczna dla prostokąta, określającego pole roboczese ###############"""#line:608
        """################## ROBOT DETECTION AND TRACKING ######################"""#line:612
        """
        Podwyższenie jasności
        """#line:615
        OO00OOO00000OOO00 =cv .cvtColor (O0OO00O00OOO0O000 .base_image ,cv .COLOR_BGR2HSV )#line:616
        OO00OOO00000OOO00 [:,:,2 ]+=OO0O0O000O0O0O0OO .BRIGHTNESS #line:617
        O0OO00O00OOO0O000 .base_image =cv .cvtColor (OO00OOO00000OOO00 ,cv .COLOR_HSV2BGR )#line:618
        O0O0OO0OOO0O00000 .detectAndTrack (OO0O0O000O0O0O0OO ,O0OO00O00OOO0O000 ,OOO00000OOOOO000O )#line:622
        """###################### ROBOT PID CONTROLLING #########################"""#line:624
        """ KW nazywa tą część PREPROCESOREM """#line:626
        OOOOOOO0O00O0OOO0 =math .hypot (O0OO00O00OOO0O000 .target [0 ]-OOO00000OOOOO000O .robot_center [0 ],O0OO00O00OOO0O000 .target [1 ]-OOO00000OOOOO000O .robot_center [1 ])#line:627
        OO0OO00000OOO0OOO =OOO00000OOOOO000O .heading -np .pi -math .atan2 (OOO00000OOOOO000O .robot_center [1 ]-O0OO00O00OOO0O000 .target [1 ],OOO00000OOOOO000O .robot_center [0 ]-O0OO00O00OOO0O000 .target [0 ])#line:628
        OO0OO00000OOO0OOO =-1 *math .atan2 (math .sin (OO0OO00000OOO0OOO ),math .cos (OO0OO00000OOO0OOO ))#line:629
        """ KONIEC """#line:630
        if (OOOOOOO0O00O0OOO0 <CFG .SIM_ERROR ):O0OO00O0OOOO0O000 =0.0 ;OO0O0OO0O0O0O0O0O =False #line:636
        else :O0OO00O0OOOO0O000 =CFG .VEL #line:638
        log_print (f'error: {OOOOOOO0O00O0OOO0}')#line:639
        log_print (f'heading_error: {OO0OO00000OOO0OOO}')#line:640
        O00000O0000OOOOO0 .update (OO0OO00000OOO0OOO )#line:642
        O0O0O0OOO000OO000 .update (OOOOOOO0O00O0OOO0 )#line:643
        """######################## OTHER ACTIONS ###############################"""#line:645
        OO0000OOO00O00O00 =statusWindow ('Status')#line:648
        if (OOOOOOO0O00O0OOO0 >CFG .SIM_ERROR ):#line:649
            O0O000O0000OO0O0O [0 ].append (OO0OO00000OOO0OOO )#line:651
            O0O000O0000OO0O0O [1 ].append (OOOOOOO0O00O0OOO0 )#line:652
            O0000O00OO0O0OOOO [0 ].append (O00000O0000OOOOO0 .SetPoint )#line:654
            O0000O00OO0O0OOOO [1 ].append (O0O0O0OOO000OO000 .SetPoint )#line:655
            O0O0OOO000OO0OOO0 [0 ].append (O00000O0000OOOOO0 .current_time )#line:657
            O0O0OOO000OO0OOO0 [1 ].append (O0O0O0OOO000OO000 .current_time )#line:658
            OO00OOO0OOOO0OO00 ,O000OOOO0O00O0000 =OOO00000OOOOO000O .robot_center #line:660
            OOO000OO0000O0OOO [0 ].append (O000OOOO0O00O0000 )#line:661
            OOO000OO0000O0OOO [1 ].append (OO00OOO0OOOO0OO00 )#line:662
            if CFG .SHOW_PATH is True :#line:665
                OOO0O00OO00OOOO00 =generate_path_image (O0OO00O00OOO0O000 ,step =5 )#line:666
                cv .imshow (OO0OO0O00O000OO00 ,OOO0O00OO00OOOO00 )#line:667
            O0OOOO000O0O00O00 =False #line:669
        elif O0OOOO000O0O00O00 ==False :#line:671
            try :#line:672
                O0OOOO0000000OOO0 =draw_plot (O0O000O0000OO0O0O [0 ],O0000O00OO0O0OOOO [0 ],O0O0OOO000OO0OOO0 [0 ],1 ,'Orientacja robota względem celu','time [s]','heading [rad]')#line:673
                O0O000O0OO0OO00OO =draw_plot (O0O000O0000OO0O0O [1 ],O0000O00OO0O0OOOO [1 ],O0O0OOO000OO0OOO0 [1 ],2 ,'Odleglość robota do celu','time [s]','distance [mm]')#line:674
            except :pass #line:676
            O0OOOO0000000OOO0 .show ()#line:678
            O0O000O0OO0OO00OO .show ()#line:679
            O0O000O0000OO0O0O =[[],[]]#line:682
            O0000O00OO0O0OOOO =[[],[]]#line:683
            O0O0OOO000OO0OOO0 =[[],[]]#line:684
            OOO000OO0000O0OOO =[[],[]]#line:685
            O0OO00O00OOO0O000 .robot_data =[]#line:687
            O0OOOO000O0O00O00 =True #line:689
        if cv .waitKey (1 )&0xFF ==ord ('m'):#line:691
            try :#line:692
                O0OOOO0000000OOO0 =draw_plot (O0O000O0000OO0O0O [0 ],O0000O00OO0O0OOOO [0 ],O0O0OOO000OO0OOO0 [0 ],1 ,'Orientacja robota względem celu','time [s]','heading [rad]')#line:693
                O0O000O0OO0OO00OO =draw_plot (O0O000O0000OO0O0O [1 ],O0000O00OO0O0OOOO [1 ],O0O0OOO000OO0OOO0 [1 ],2 ,'Odleglość robota do celu','time [s]','distance [mm]')#line:694
            except :pass #line:695
            O0OOOO0000000OOO0 .show ()#line:697
            O0O000O0OO0OO00OO .show ()#line:698
            O0O000O0000OO0O0O =[[],[]]#line:700
            O0000O00OO0O0OOOO =[[],[]]#line:701
            O0O0OOO000OO0OOO0 =[[],[]]#line:702
            O0OO00O00OOO0O000 .robot_data =[]#line:704
            O0OOOO000O0O00O00 =True #line:706
            cv .waitKey (0 )#line:708
        if CFG .SIMULATION :#line:710
            pass #line:711
        else :#line:712
            O000O0OOO00000000 +=1 #line:714
            if CFG .PLAY_IN_LOOP ==True :#line:717
                if OOOOO0O00O0O00O00 .play_in_loop (OO0O000OOO0000OO0 ,O000O0OOO00000000 )is True :#line:718
                    pass #line:719
                for _OOO00OOO00O0OO000 in range (0 ,CFG .FRAME_RATE ):#line:722
                    OO0O000OOO0000OO0 .grab ()#line:723
                    O000O0OOO00000000 +=1 #line:724
        OO0000OOO00O00O00 .drawData (OOO00000OOOOO000O .robot_center ,OOO00000OOOOO000O .heading ,OOOOOOO0O00O0OOO0 ,OO0OO00000OOO0OOO ,O0OO00O00OOO0O000 .doWarpImage ,O0OO00O00OOO0O000 .detected )#line:731
        OO0000O00O00OOO0O ,OO000O0OO0O000000 ,_OOO00OOO00O0OO000 =O0OO00O00OOO0O000 .base_image .shape #line:733
        if CFG .SHOW_PATH :O0OO00O00OOO0O000 .robot_data .append (OOO00000OOOOO000O .unpackImg (OO0000O00O00OOO0O ,CFG .AREA_HEIGHT_REAL ,OO000O0OO0O000000 ,CFG .AREA_WIDTH_REAL ))#line:735
        OOOO00O0OOOOOO0O0 =cv .waitKey (2 )&0xFF #line:737
        if OOOO00O0OOOOOO0O0 ==ord ('p'):#line:738
            O0OO00O00OOO0O000 .doWarpImage =not O0OO00O00OOO0O000 .doWarpImage #line:739
            log_info ("doWarp-changed")#line:740
        elif OOOO00O0OOOOOO0O0 ==ord ('q'):#line:741
            break #line:742
        elif OOOO00O0OOOOOO0O0 ==ord ('r'):#line:743
            OOOOO0O000OO0O000 .robot_center =(50 ,25 )#line:744
            OOOOO0O000OO0O000 .calculate_led_pos ()#line:745
    OOO0O0O0O00000O00 =r'C:\Users\barte\Documents\Studia VII\Image_processing\TadroBeaconTracker\tadro-tracker\2Led\paths'#line:749
    save_image (path_img ,f'RobotPath_'+f'{datetime.now():%Y%m%d_%H%M%S}',OOO0O0O0O00000O00 )#line:750
    OO0O000OOO0000OO0 .release ()#line:751
    cv .destroyAllWindows ()#line:752
if __name__ =='__main__':#line:903
    main_default ()#line:905
log_info ("Exit")#line:906
