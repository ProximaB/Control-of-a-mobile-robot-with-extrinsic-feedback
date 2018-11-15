import cv2
import numpy as np
from collections import deque
from math import sqrt

refPt:list = []
cropping = False

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping
    global img, p0, cap, ret, old_gray, p1m, st, err, feature_params, old_frame, frame, frame_gray, good_old, p1, st, err
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        if cropping is True:            
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            refPt.append((x, y))
            cropping = False

            # draw a rectangle around the region of interest
            cv2.rectangle(img, refPt[0], refPt[1], (0, 255, 0), 2)
            cv2.imshow("image", img)
            ret, old_frame = cap.read()
            xs, ys = refPt[0]
            xk, yk = refPt[1]
            ROI = old_frame[ys:yk,xs:xk]
            ROI_region = np.zeros((480,640,1), dtype='uint8')
            print(f"ROI_REGION_PO_KOPI_Z_OLD_FRAME:{type(ROI_region)}, {ROI_region.shape}, {ROI_region.dtype}")
            print(f"old_frame_REGION_PO_KOPI_Z_OLD_FRAME:{type(old_frame)}, {old_frame.shape}, {old_frame.dtype}")
            ROI_region[ys:yk,xs:xk] = 255
            #ROI_region = cv2.cvtColor(ROI_region, cv2.COLOR_BGR2GRAY)
            old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('ROI_region', ROI_region)
            old_gray = cv2.bitwise_and(old_gray, old_gray, mask = ROI_region)
            old_frame = cv2.bitwise_and(old_frame, old_frame, mask = ROI_region)
            #ROI_gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
            cv2.imshow('ROI', ROI)
            cv2.imshow('old_gray', old_gray)
            cv2.imshow('old_frame', old_frame)
            p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
            good_old = p1[st == 1]
            good_new = good_old

            p0 = good_old.reshape(-1, 1, 2)
            #p1 = good_new.reshape(-1, 1, 2)
            print(p0)
            #cv2.waitKey(0)
    

cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)



cap = cv2.VideoCapture(1)
#cap = cv2.VideoCapture('side.avi')
# params for ShiTomasi corner detection
feature_params = dict(maxCorners=100,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)
# Parameters for lucas kanade optical flow
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Create some random colors
color = np.random.randint(0, 255, (120, 3))
# Take first frame and find corners in it
ret, old_frame = cap.read()
for i in range(60):
    ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
print(p0)
# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
pts: deque = deque(maxlen=120)
while(1):
    global p1
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_no = cap.get(cv2.CAP_PROP_POS_FRAMES)
   # if int(frame_no) % 5 == 0:
    #    p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(
        old_gray, frame_gray, p0, None, **lk_params)
    # Select good points
    good_new = p1[st == 1]
    good_old = p0[st == 1]
    # draw the tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        mask = np.zeros_like(old_frame)
        a, b = new.ravel()
        c, d = old.ravel()

        # derivative a b in time give us velocity
        #dist = sqrt((a-c)*(a-c)-(b-d)*(b-d))
        cv2.line(mask, (c, d), (int(c+10), int(d+10)),
                 color=(122, 0, 0), thickness=4)

        #mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        #frame = cv2.circle(frame,(a,b),5, color[i].tolist(),-1)
        points = (a, b, c, d)
        pts.appendleft(points)
        # loop over the set of tracked points

        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            a, b, c, d = pts[i]
            mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
        frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)

    # reinit features
    if cv2.waitKey(1) & 0xFF == ord('f'):
        ret, old_frame = cap.read()
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
        print(p0)

    img = cv2.add(frame, mask)
    cv2.imshow('image', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # Now update the previous frame and previous points
    if cropping is True:
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)
    else:
        old_gray = old_gray.copy()
        p0 = good_old.reshape(-1, 1, 2)
        cropping = False

cv2.destroyAllWindows()
cap.release()
