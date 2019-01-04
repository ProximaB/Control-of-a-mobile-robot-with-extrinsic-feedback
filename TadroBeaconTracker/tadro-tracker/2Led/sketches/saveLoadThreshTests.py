    testPath = r"C:\Users\barte\Documents\Studia VII\Image_processing\TaeedroBeaconTracker\tadro-tracker\2Led\thresh.pickle"
    #save_thresholds({1:"TEST",2:"TEST"}, testPath)

    thresh = [{},{}]
    class klasa: pass

    thresh = load_thresholds(thresh, testPath)
    print(f'Loaded thresh: {thresh}')
    cv.waitKey(0)