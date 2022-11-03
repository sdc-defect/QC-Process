import cv2
import time

cap = cv2.VideoCapture(0)
timeCheck=time.time()
while 1:
    ret,frame=cap.read()
    frame=frame[15:465,85:535]
    frame=cv2.resize(frame,(300,300))
    cv2.imshow('test.jpg',frame)
    if time.time()-timeCheck>=3:
        timeCheck=time.time()
        print('captured')
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()