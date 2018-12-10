"""
BOOSTING Tracker: Based on the same algorithm used to power the machine learning behind Haar cascades (AdaBoost), but like Haar cascades, is over a decade old. This tracker is slow and doesn’t work very well. Interesting only for legacy reasons and comparing other algorithms. (minimum OpenCV 3.0.0)
MIL Tracker: Better accuracy than BOOSTING tracker but does a poor job of reporting failure. (minimum OpenCV 3.0.0)
KCF Tracker: Kernelized Correlation Filters. Faster than BOOSTING and MIL. Similar to MIL and KCF, does not handle full occlusion well. (minimum OpenCV 3.1.0)
CSRT Tracker: Discriminative Correlation Filter (with Channel and Spatial Reliability). Tends to be more accurate than KCF but slightly slower. (minimum OpenCV 3.4.2)
MedianFlow Tracker: Does a nice job reporting failures; however, if there is too large of a jump in motion, such as fast moving objects, or objects that change quickly in their appearance, the model will fail. (minimum OpenCV 3.0.0)
TLD Tracker: I’m not sure if there is a problem with the OpenCV implementation of the TLD tracker or the actual algorithm itself, but the TLD tracker was incredibly prone to false-positives. I do not recommend using this OpenCV object tracker. (minimum OpenCV 3.0.0)
MOSSE Tracker: Very, very fast. Not as accurate as CSRT or KCF but a good choice if you need pure speed. (minimum OpenCV 3.4.1)
GOTURN Tracker: The only deep learning-based object detector included in OpenCV. It requires additional model files to run (will not be covered in this post). My initial experiments showed it was a bit of a pain to use even though it reportedly handles viewing changes well (my initial experiments didn’t confirm this though). I’ll try to cover it in a future post, but in the meantime, take a look at Satya’s writeup. (minimum OpenCV 3.2.0)


Use CSRT when you need higher object tracking accuracy and can tolerate slower FPS throughput
Use KCF when you need faster FPS throughput but can handle slightly lower object tracking accuracy
Use MOSSE when you need pure speed
"""


# import the necessary packages
import cv2
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import argparse
import time
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', type=str, help='path to input vieo file')
ap.add_argument('-t', '--tracker', type=str, default='kcf',
                help='OpenCV object tracker type')
args = vars(ap.parse_args())
print(args)

current_tracker = args['tracker']

# extract the OpenCV version info
(major, minor) = cv2.__version__.split('.')[:2]

if int(major) == 3 and int(minor) < 3:
    tracker = cv2.Tracker_create(args['tracker'].upper())
else:
    OPENCV_OBJECT_TRACKERS = {
        'csrt': cv2.TrackerCSRT_create,
        'kcf': cv2.TrackerKCF_create,
        'boosting': cv2.TrackerBoosting_create,
        'mil': cv2.TrackerMIL_create,
        'medianflow': cv2.TrackerMedianFlow_create,
        'mosse': cv2.TrackerMOSSE_create
    }

    tracker = OPENCV_OBJECT_TRACKERS[args['tracker']]()

initBB = None
coreFrame = None

if not args.get('video', False):
    print('[INFO] starting video stream...')
    vs = VideoStream(src=1).start()
    time.sleep(1.0)
else:
    vs = cv2.VideoCapture(args['video'])

fps = None

while True:
    frame = vs.read()
    frame = frame[1] if args.get('video', False) else frame
    if frame is None:
        break

    frame = imutils.resize(frame, width=500)
    frame = cv2.bilateralFilter(frame,9,45,45)

    (H, W) = frame.shape[:2]

    if initBB is not None:
        (success, box) = tracker.update(frame)
        print('Does succes: {}'.format(success))
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            fps.update()
            fps.stop()

            info = [
                ('Tracker', current_tracker),
                ('Succes', 'Yes' if success else 'No'),
                ('FPS', "{:.2f}".format(fps.fps())),
                ]
 
            cv2.rectangle(
                frame, 
                (10, H - ((0 * 20) + 18)),
                (130, H - ((3 * 20) + 20)),
                (0, 0, 0),
                -1
            )
            for (i, (k, v)) in enumerate(info):
                text = '{}: {}'.format(k, v)
                
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 0), 2)

    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        coreFrame = frame.copy()
        initBB = cv2.selectROI('Frame', coreFrame, fromCenter=False,
                            showCrosshair=True)
        tracker = OPENCV_OBJECT_TRACKERS[current_tracker]() 
        tracker.init(coreFrame, initBB)

        x, y, w, h = initBB
        cv2.imshow('ROI', frame[y:y+h+1 , x:x+w+1]) 
        fps = FPS().start()

    elif key == ord('n'):
        trackers_name_list = list(OPENCV_OBJECT_TRACKERS)
        index = None
        for i, x in enumerate(trackers_name_list):
            if x == current_tracker:
                index = i
                break
        index = (index+1) % len(trackers_name_list)
        current_tracker = trackers_name_list[index]
        print("Index:{}: Name:{}".format(index, current_tracker))
        # REVERSE_DICT = {v: k for k, v in OPENCV_OBJECT_TRACKERS.items()}
        tracker = OPENCV_OBJECT_TRACKERS[current_tracker]() 
        tracker.init(coreFrame, initBB)
        
        fps = FPS().start()
    elif key == ord('q'):
        break

if not args.get('video', False):
    vs.stop()
else:
    vs.release()

cv2.destroyAllWindows()

print('good ;)')
