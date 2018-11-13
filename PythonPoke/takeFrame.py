import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--fileName", required=True,
                help="Path to where the frame will be saved")
ap.add_argument("-p", "--path", required=False,
                help="Path to where the frame will be saved")
args = vars(ap.parse_args())

cap = cv2.VideoCapture(1)

while True:
    _, frame = cap.read()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        if args['path'] is None:
            cv2.imwrite(args['fileName'], frame)
        else:
            cv2.imwrite(args['path'] + '\\' + args['fileName'], frame)
        break
