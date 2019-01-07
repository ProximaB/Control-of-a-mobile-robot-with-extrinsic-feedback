import numpy as np
import argparse
import cv2
import os
from datetime import datetime
from PIL import Image
import pickle

def save_img(file_name, img, saveTo):
    if not os.path.exists(saveTo):
        os.makedirs(saveTo)
    img = img[:,:,::-1]
    img = Image.fromarray(img)

    try:
        img.save(saveTo + "/" + file_name + ".jpg", resolution=100.0)
    except Exception as ex:
        print("Error while saving file.")
        print(ex)
        return False
    else: return True


def capture_save_calibrate_images(camId = 0, name_prefix = 'Checkerboard_', path = f'{os.path.abspath(os.curdir)}\\checkerboards_cal'): 
    font                   = cv2.FONT_HERSHEY_DUPLEX
    position               = (15,50)
    fontScale              = 1.3
    fontColor              = (255,255,255)
    lineType               = 2

    cap = cv2.VideoCapture(camId)
    
    while True:
        ret, frame = cap.read()
        if ret is False: 
            return
        img = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (8, 6), None)
        
        if corners is not None:
            for i in corners:
                x,y = i.ravel()
                cv2.circle(frame,(x,y),5,(0,0,255),-1)
                
        key =  cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            print('quited')
            break
        elif key == ord('s'):
            cv2.putText(frame,'To save click S, to pass P', 
                position, 
                font, 
                fontScale,
                fontColor,
                lineType)
            cv2.imshow('frame', frame)
            doSave = cv2.waitKey(0)  & 0xFF
            if doSave == ord('s'):
                gene_name = f'{name_prefix}{datetime.now():%Y%m%d_%H%M%S}'
                res = save_img(gene_name, img, path) 
                if res is True: print(f"Saved: {os.path.abspath(os.curdir)}\\checkerboards_cal\\{gene_name}")
            else: continue
        cv2.imshow('frame', frame)
    cap.release
    cv2.destroyAllWindows()
                
def cal_undistort(img, objpoints, imgpoints):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)
    undist = cv2.undistort(img, mtx, dist, None, mtx)
    return undist, mtx, dist


def capture_save_undistort_img(camId = 0, name_prefix = 'work_space_photo', path = f'{os.path.abspath(os.curdir)}\work_space',
                                  calib_data_file = None): 
    font                   = cv2.FONT_HERSHEY_DUPLEX
    position               = (15,50)
    fontScale              = 1.3
    fontColor              = (255,255,255)
    lineType               = 2

    cap = cv2.VideoCapture(camId)
    
    do_undistort = False
    if calib_data_file is not None:
        try:
            data_file = open(calib_data_file, 'rb')
        except: 
                print('Calibration data Not loaded.')
                return
            
        calib_data = pickle.load(data_file)
        data_file.close()
        mtx = calib_data['mtx'][0]
        dist = calib_data['dist'][0]
        do_undistort = True
        print('Calibration data loaded.')
            
    while True:
        ret, frame = cap.read()
        if ret is False: 
            return
        if do_undistort is True:
            frame = cv2.undistort(frame,mtx,dist,None,mtx)
        img = frame.copy()
                
        key =  cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            print('quited')
            break
        elif key == ord('s'):
            cv2.putText(frame,'To save click S, to pass P', 
                position, 
                font, 
                fontScale,
                fontColor,
                lineType)
            cv2.imshow('frame', frame)
            doSave = cv2.waitKey(0)  & 0xFF
            if doSave == ord('s'):
                gene_name = f'{name_prefix}{datetime.now():%Y%m%d_%H%M%S}'
                res = save_img(gene_name, img, path) 
                if res is True: print(f"Saved: {os.path.abspath(os.curdir)}\\checkerboards_cal\\{gene_name}")
            else: continue
        cv2.imshow('frame', frame)
    cap.release
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print(f'Abs Path: {os.path.abspath(os.curdir)}')
    path = r'.\TadroBeaconTracker\tadro-tracker\2Led\calibration_images'
    capture_save_undistort_img(1, calib_data_file='cam_calibration_data.p')
    