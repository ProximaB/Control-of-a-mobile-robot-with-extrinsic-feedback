import cv2
import numpy as np


class MyCam():
    def __init__(self, frameSize=(480, 640), focus=600, avgPointPos=np.array([0, 0, 3]), sigma=.5, pointNum=300):
        self.pointCloud = sigma * np.random.randn(pointNum, 3)
        self.pointCloud = map(lambda pnt: pnt + avgPointPos, self.pointCloud)
        self.t = np.zeros(3)
        self.R = np.identity(3)
        self.frameSize = frameSize
        self.focus = focus

    def read(self):
        pnts = np.array(self.projectPoints())
        frame = np.zeros(self.frameSize + (3,))

        for pnt in pnts.astype(int):
            if pnt[0] > 0 and pnt[1] > 1 and pnt[0] < self.frameSize[0] and pnt[1] < self.frameSize[1]:
                cv2.circle(frame, tuple(pnt), 5, [0, 0, 255], -1)
        return frame

    def addVecToPoint(self, points, vec):
        return map(lambda pnt: pnt + vec, points)

    def transformPoints(self):
        rotated = np.dot(self.pointCloud, self.R.T)
        translated = self.addVecToPoint(rotated, self.t)
        return translated

    def projectPoints(self):
        transformed = self.transformPoints()
        inFrontofCameraPoints = filter(lambda pnt: pnt[2] > 0, transformed)
        return map(lambda pnt: self.focus * pnt[:2]/pnt[2] + np.array(self.frameSize)/2, inFrontofCameraPoints)


cam = MyCam()
'''
frame = cam.read()
cv2.imshow('frame',frame)
k = cv2.waitKey(0)
'''

angle = .1

rotateZ = np.array([[np.cos(angle), np.sin(angle), 0],
                    [-np.sin(angle), np.cos(angle), 0],
                    [0, 0, 1]])
while(1):
    frame = cam.read()
    cv2.imshow('frame', frame)
    cam.R = np.dot(rotate, cam.R)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

rotateX = np.array([[np.cos(angle), np.sin(angle), 0],
                    [-np.sin(angle), np.cos(angle), 0],
                    [0, 0, 1]])

cv2.destroyAllWindows()
