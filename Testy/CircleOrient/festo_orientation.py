import cv2
import numpy as np
from array import array


imgOriginal = cv2.imread('Testy/CircleOrient/gri2.jpg', 1)
img = cv2.imread('Testy/CircleOrient/gri2.jpg', 0)
img = cv2.medianBlur(img, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
hsv = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

circles1 = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.1, 85, param1=40, param2=70, minRadius=20,
                                   maxRadius=90)   # small circle

circles2 = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.1, 85, param1=40, param2=70, minRadius=146,
                                   maxRadius=160)  # bigger circle

#Parameters 1 and 2 don't affect accuracy as such, more reliability.
# Param 1 will set the sensitivity; how strong the edges of the circles need to be. Too high and it won't detect anything, too low and it will find too much clutter.
# Param 2 will set how many edge points it needs to find to declare that it's found a circle. Again, too high will detect nothing, too low will declare anything to be a circle.
# The ideal value of param 2 will be related to the circumference of the circles.

for i in circles1[0, :]:    # small circle
    # draw the outer circle
    cv2.circle(imgOriginal, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(imgOriginal, (i[0], i[1]), 2, (0, 0, 255), 3)


for i in circles2[0, :]:  #for bigger circ.
    # draw the outer circle

    cv2.circle(imgOriginal, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(imgOriginal, (i[0], i[1]), 2, (0, 0, 255), 3)

t=0
yenicount=0
egim=0



cv2.circle(hsv, (int(circles1[0][0][0]),int(circles1[0][0][1])), int(circles1[0][0][2]), [255,255,255], -1)  # fills inside of the little circle
renk_i=0
renk_j=0

lowh = 0
high = 157
lows = 0
higs = 140
lowv = 0
higv = 255
font = cv2.FONT_HERSHEY_SIMPLEX


d = np.array([lowh, lows, lowv])
t = np.array([high, higs, higv])
filt = cv2.inRange(hsv, d, t)

im1 = np.zeros(filt.shape, np.uint8)
cv2.circle(im1, (int(circles2[0][0][0]),int(circles2[0][0][1])), int(circles2[0][0][2]), [255,255,255], -1)
res = np.zeros(filt.shape, np.uint8)

cv2.bitwise_and(filt,im1,res)
rows,cols=res.shape

i=0
j=0
d=0
cv2.imwrite("Testy/CircleOrient/imgOrg.jpg",imgOriginal)
#dikey arama, dikeyde soldan ilk bulunan pikseli secer
while (j < cols-10 ) and ( d==0 ):
    while (i < rows-10 ) and (d==0):
        if (res[i,j] > 5) and (res[i+5,j]>5) and (res[i+2,j+1]>5) and (res[i+1,j]>5):

            renk_i = i
            renk_j = j
            imgOriginal[i,j]=[255,255,0]


            j+=2
            i+=2
            d=1

        i += 2
    j += 2
    i = 0

counter=0
kernel = np.ones((3,3),np.uint8)
res = cv2.erode(res,kernel,iterations = 1)


yeni=res[(renk_i-10):(renk_i+80),(renk_j-10):(renk_j+80)]
i=0
j=0

renk_i_yeni=0
renk_j_yeni=0
yrows,ycols=yeni.shape
while (i < yrows - 3):
    while (j < ycols - 3):
        if (yeni[i, j] > 5):
            renk_i_yeni = i + renk_i_yeni
            renk_j_yeni = j + renk_j_yeni
            counter += 1
        j += 1
    i += 1
    j = 0
cv2.imwrite("Testy/CircleOrient/res.jpg",res)

i = 0
j = 0

buli = renk_i_yeni / counter
bulj = renk_j_yeni / counter

buli=buli+renk_i-10
bulj=bulj+renk_j-10

cv2.line(imgOriginal, (int(bulj),int(buli)), (int(circles2[0][0][0]), int(circles2[0][0][1])), (255,0,0),3)
egimust=float(circles2[0][0][1]-buli)
egimalt = -float(circles2[0][0][0]-bulj)
egim=(np.arctan(egimust / egimalt))*(180/np.pi)
egim=egim+180
print("egim=", egim)

if egim>150:

    deg=210-egim
else:
    deg=90-egim

M = cv2.getRotationMatrix2D((cols/2,rows/2),deg,1)
dst = cv2.warpAffine(imgOriginal,M,(cols,rows))


print(renk_i)
print(renk_j)
cv2.putText(imgOriginal,
            str(int(egim)),
            (200, 350), font, 2,
            (255, 255, 255), 2, cv2.LINE_AA)  

cv2.imshow('detected circles',imgOriginal)
cv2.imwrite("Testy/CircleOrient/cizili.jpg",imgOriginal)
cv2.imshow('map',res)

cv2.imshow('rotated circles',dst)
cv2.imwrite("Testy/CircleOrient/cevrili.jpg",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()