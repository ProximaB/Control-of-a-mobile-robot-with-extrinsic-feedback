import cv2
from imutils.video import FPS


cap = cv2.VideoCapture(1)
cap.set(3, 320)#640
cap.set(4, 240)#480)
out = cv2.VideoWriter('output.avi', -1, 20.0, (320,240))
cap.set(cv2.CAP_PROP_FPS, 446)
print('Started..')
imgs = []
fps = FPS().start()
while(fps._numFrames < 300):
    fps.update()
    ret, img = cap.read()
    #cv2.imshow('img', img)
    #cv2.waitKey(1)
    #if((cv2.waitKey(1) & 0xFF) == ord('q')):
    #   break

    fps.update()
    imgs.append(img)
fps.stop()

for im in imgs:
    out.write(im)

print("[INFO] counted frames: {:.2f}".format(fps._numFrames))
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cap.release()
out.release()
cv2.destroyAllWindows()