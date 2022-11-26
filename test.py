import cv2
import mediapipe as mp
import time
import math
 
cap = cv2.VideoCapture(0)
 
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
 
pTime = 0
cTime = 0

success, img = cap.read()
h, w, c = img.shape

ballx=int(w/2)
bally=int(h/2)
balldx=int(0)
balldy=int(0)
fdx=[0,0]
fdy=[0,0]
fox=[0,0]
foy=[0,0]
leftscore=0
rightscore=0

lose=False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    
    
    fx=[]
    fy=[]

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                if id == 8:
                    fx.append(cx)
                    fy.append(cy)

                    cv2.circle(img, (cx, cy), 20, (255, 0, 255), cv2.FILLED)
 
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    
    # draw ball
    cv2.circle(img, (ballx, bally), 20, (255, 0, 255), cv2.FILLED)

    
    
    # calculate ball movement
    print(fx)
    if len(fx)>2:
        fx=fx[0:1]
        fy=fy[0:1]
    for i in range(len(fx)):
        if math.sqrt((fx[i]-ballx)*(fx[i]-ballx) + (fy[i]-bally)*(fy[i]-bally)) < 50:
            fdx[i] = fx[i]-fox[i]
            fdy[i] = fy[i]-foy[i]
        else:
            fdx[i] = 0
            fdy[i] = 0

        balldx = 0.99*(balldx + fdx[i])
        balldy = 0.99*(balldy + fdy[i]) 

        fox[i]=fx[i]
        foy[i]=fy[i]

    if (ballx + balldx) < 0 and bally > h/3 and bally < 2*h/3:
        ballx=int(w/2)
        bally=int(h/2)
        balldx=0
        balldy=0
        rightscore+=1

    if (ballx + balldx) > w and bally > h/3 and bally < 2*h/3:
        ballx=int(w/2)
        bally=int(h/2)
        balldx=0
        balldy=0
        leftscore+=1

    if int(ballx+balldx) < 0 or int(ballx+balldx) > w:
        balldx = -balldx

    if int(bally+balldy) < 0 or int(bally+balldy) > h:
        balldy = -balldy

    ballx = int(ballx+balldx)
    bally = int(bally+balldy)

    # draw lines
    cv2.line(img, ((int(w/2),0)), (int(w/2),int(h)), (255, 255, 255), 2)
    cv2.line(img, (0,int(h/3)), (0,int(2*h/3)), (255, 255, 255), 2)
    cv2.line(img, (w,int(h/3)), (w,int(2*h/3)), (255, 255, 255), 2)

    

    pTime = cTime

    cv2.putText(img, str(int(leftscore)), (int(w/10), int(h/10)), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.putText(img, str(int(rightscore)), (int(w-(w/10)), int(h/10)), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 255), 3)
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)