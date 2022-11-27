import cv2
import mediapipe as mp
import time
import math
 
cap = cv2.VideoCapture(0)
 
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2)
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

joint7x = [0,0]
joint7y = [0,0]
thumbx = [0,0]
thumby = [0,0]
middlex = [0,0]
middley = [0,0]
distance=[0,0]
click=[False,False]

hold=False
holdx=0
holdy=0

def getdistance(x1,x2,y1,y2):
    return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    
    fx=[]
    fy=[]
    joint7x = []
    joint7y = []
    thumbx = []
    thumby = []
    middlex = []
    middley = []
    click=[False,False]


    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                if id == 4:
                    thumbx.append(cx)
                    thumby.append(cy)
                    
                if id == 7:
                    joint7x.append(cx)
                    joint7y.append(cy)

                if id == 8:
                    fx.append(cx)
                    fy.append(cy)
                    cv2.circle(img, (cx, cy), 20, (255, 0, 255), cv2.FILLED)
        
                if id == 12:
                    middlex.append(cx)
                    middley.append(cy)
                    
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
 
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    
    # draw ball
    cv2.circle(img, (ballx, bally), 20, (255, 0, 255), cv2.FILLED)
    
    
    # calculate ball movement
    if len(fx)>2:
        fx=fx[0:1]
        fy=fy[0:1]
    for i in range(len(fx)):
        holdx=int((fx[i]+thumbx[i])/2)
        holdy=int((fy[i]+thumby[i])/2)
        if getdistance(middlex[i],fx[i],middley[i],fy[i]) < 20 and getdistance(joint7x[i],fx[i],joint7y[i],fy[i]) < 20:
            click[i] = True
        if math.sqrt((fx[i]-ballx)*(fx[i]-ballx) + (fy[i]-bally)*(fy[i]-bally)) < 50:
            fdx[i] = fx[i]-fox[i]
            fdy[i] = fy[i]-foy[i]
            
            hold=False
            if math.sqrt((fx[i]-thumbx[i])*(fx[i]-thumbx[i]) + (fy[i]-thumby[i])*(fy[i]-thumby[i])) < 20:
                hold=True
                
        else:
            fdx[i] = 0
            fdy[i] = 0

        #balldx = 0.99*(balldx + fdx[i])
        #balldy = 0.99*(balldy + fdy[i]) 

        fox[i]=fx[i]
        foy[i]=fy[i]
        
        #calculate distance
        distance[i] = math.sqrt((fx[i]-joint7x[i])*(fx[i]-joint7x[i]) + (fy[i]-joint7y[i])*(fy[i]-joint7y[i]))
    

    

    if int(ballx+balldx) < 0 or int(ballx+balldx) > w:
        balldx = -balldx

    if int(bally+balldy) < 0 or int(bally+balldy) > h:
        balldy = -balldy
    
    if hold:
        ballx = holdx
        bally = holdy
    else:
        ballx = int(ballx+balldx)
        bally = int(bally+balldy)
    



    pTime = cTime
    
 
    cv2.imshow("Image", img)
    cv2.waitKey(1)