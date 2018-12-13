import numpy as np
import cv2
font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)

ret,frame=cap.read()

#select Object of Interest
r = cv2.selectROI(frame)
crop=frame[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0]+r[2])]

r,h,c,w = int(r[1]),int(r[3]),int(r[0]),int(r[2]) 
track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x,y,w,h = track_window
        img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        xc=(int)(x+w/2)
        yc=(int)(y+h/2)
        cv2.circle(img2,(xc,yc), 5, (0,255,0), -1)
        #assumed frame size 640 X 480
        dy=480-yc
        dx=640-xc
        cv2.putText(img2,('dx='+str(dx)),(10,400), font, 1,(0,0,255),1,cv2.LINE_AA)
        cv2.putText(img2,('dy='+str(dy)),(10,425), font, 1,(0,0,255),1,cv2.LINE_AA)
        cv2.imshow('img2',img2)

        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg",img2)

    else:
        break

cv2.destroyAllWindows()
cap.release()
