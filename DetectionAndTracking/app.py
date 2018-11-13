import cv2

CAM_ID = 1

for i in range(10):
    cap = cv2.VideoCapture(i)
    isOpened = cap.isOpened()
    cap.release()
    print(f"Camera: {i}: {isOpened}")

cap = cv2.VideoCapture(0)
cv2.waitKey(0)
while True:
    retval, img = cap.read()
    print(f"Retval: {retval}")
    cv2.imshow('Camera{0}'.format(CAM_ID), img)

    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break

cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
print("[Program finished]")
