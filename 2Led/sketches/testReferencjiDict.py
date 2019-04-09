while(True):
    if (cv.waitKey(20) & 0xFF) == ord('q'):
        break
    print(SETTINGS.thresholds)