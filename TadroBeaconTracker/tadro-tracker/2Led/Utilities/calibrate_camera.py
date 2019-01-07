import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import pickle
import sys
import os
sys.path.insert(0, os.path.abspath + r'TaddroBeaconTracker/2Led')
from config import D as CFG

def cal_undistort(objpoints, imgpoints):
    _, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)
    return mtx, dist

def collect_callibration_points():
    objpoints = []
    imgpoints = []

    images = glob.glob('./checkerboards_cal/Checkerboard_*.jpeg')
    objp = np.zeros((8*6, 3), np.float32)
    objp[:, :2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)
    
    for fname in images:
        img = mpimg.imread(fname) #[::-1,:,::-1]
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (8, 6), None)

        if ret is True:
            imgpoints.append(corners)
            objpoints.append(objp)

    return imgpoints, objpoints

if __name__ == '__main__':
    # CameraCalibration
    imgpoints, objpoints = collect_callibration_points()
    cameraMatrix, distCoeffs = cal_undistort(objpoints, imgpoints)
    # Save the camera calibration result for later use (we won't worry about rvecs / tvecs)
    dist_pickle = {}
    dist_pickle["mtx"] = cameraMatrix,
    dist_pickle["dist"] = distCoeffs,
    dist_pickle['objpoints'] = objpoints
    dist_pickle['imgpoints'] = imgpoints
    pickle.dump( dist_pickle, open(CFG.CAMERA_CALIBRATION_PATH, 'wb') )