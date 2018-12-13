import cv2
import numpy as np

# Daha duzgun cember bulma algoritmasi
# A better circle detecting algorithm

# TO DO LIST:
# nothing here!


def close(a, b, thr):       # close check
    if abs(a - b) < thr:
        return 1
    return 0

eski_c=0

diz = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
old_diz = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fin_diz = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

print("BASLANGIC")
cap = cv2.VideoCapture('test_vid.mp4')
thr = 10  # yakinlik derecesi

fr = 1  # bool first run
while 1:
    nc_c=0  
    circles = 0
    print("detecting")
    while 1:
        ret, frame = cap.read()
        if ret is False:
             print("failed load video")
        imgOriginal = frame
        img = frame

        img = cv2.medianBlur(img, 5)
        cimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1.1, 85, param1=40, param2=70, minRadius=50,
                                   maxRadius=75)  # 90

        # Param 1 will set the sensitivity; how strong the edges of the circles need to be. Too high and it won't detect anything, too low and it will find too much clutter.
        # Param 2 will set how many edge points it needs to find to declare that it's found a circle. Again, too high will detect nothing, too low will declare anything to be a circle.
        # The ideal value of param 2 will be related to the circumference of the circles.

        if (circles is None) != 1:
            break

    c = 0
    print("yeniler:")
    for i in circles[0, :]:


        diz[c] = i
        if fr == 1:  # if first run
            print("Ilk calisma")
            old_diz[c] = i
            fin_diz[c] = i
            eski_c=c
        print(diz[c])

        c += 1  #bulunan cember sayisi


    sayac = 0
    fr = 0   # baslangic degiskeni 0 oldu

    print("Eski dizi")
    while (sayac < eski_c):
        print(old_diz[sayac])

        sayac += 1

    sayac = 0
    sayac2 = 0

    while sayac2 < c:
        while sayac < eski_c:
            if (close(old_diz[sayac][0], diz[sayac2][0], thr) and close(old_diz[sayac][1], diz[sayac2][1], thr)):
                nc_c=1               # not close counter
            sayac += 1
        if (nc_c == 0):
            print("eslesme yok")  #no match
            print(diz[sayac2][:])
            fin_diz[sayac2] = diz[sayac2]
        nc_c=0
        sayac2 += 1
        sayac = 0

    print(" ")

    sayac = 0
    sayac2 = 0

    while sayac < c:
        while sayac2 < eski_c:
            if (close(old_diz[sayac2][0], diz[sayac][0], thr) and close(old_diz[sayac2][1], diz[sayac][1], thr)) and (
                diz[sayac][2] > old_diz[sayac2][2]):
                # update
                print("update new: ", diz[sayac][0],"old: ", old_diz[sayac2][0])
                print("update new: ", diz[sayac][2], "old: ", old_diz[sayac2][2])
                fin_diz[sayac2][:] = diz[sayac][:]



            sayac2 += 1
        sayac += 1
        sayac2 = 0

    sayac = 0
#
    while (sayac < c):
         old_diz[sayac] = fin_diz[sayac]

         sayac += 1


    sayac = 0
    print("count",c)
    print("Yenilenen dizi")
    while (sayac < c):
        print(fin_diz[sayac])
        # draw the outer circle
        cv2.circle(imgOriginal, (fin_diz[sayac][0], fin_diz[sayac][1]), fin_diz[sayac][2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(imgOriginal, (fin_diz[sayac][0], fin_diz[sayac][1]), 2, (0, 0, 255), 3)
        sayac += 1
    eski_c=c
    print(" ")
    font = cv2.FONT_HERSHEY_SIMPLEX
    sayac=0
    while sayac < c:
        cv2.putText(imgOriginal,
                    str(int(fin_diz[sayac][0])) + "," + str(int(fin_diz[sayac][1])) + "," + str(int(fin_diz[sayac][2])),
                    (fin_diz[sayac][0], fin_diz[sayac][1]), font, 2,
                    (255, 255, 255), 2, cv2.LINE_AA) #coordinates
        sayac += 1

    cv2.imshow('detected circles', imgOriginal)
    cv2.waitKey(3)

cv2.destroyAllWindows()