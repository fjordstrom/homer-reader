import cv2
import numpy as np
import Image
import pytesseract
import pyttsx

import VisionTools as vt

voiceRate = 120
camera = 2

#init
cap = cv2.VideoCapture(camera)

engine = pyttsx.init()

engine.setProperty('voice', 'romanian')

rate = engine.getProperty('rate')
engine.setProperty('rate', voiceRate)



engine.startLoop(False)

#looop
while True:

    ret, image = cap.read()
    #cv2.imshow('frame',image)
    image = cv2.flip(cv2.transpose(image), 1)

    

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)

    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE )


    for contour in contours:
        [x,y,w,h] = cv2.boundingRect(contour)
        # if cv2.contourArea(contour)>5000:
        if(w > 100 and h > 400):
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)



    cv2.imshow('frame',image)
    
    if(False):
        img = Image.fromarray(image, 'RGB')
        text = pytesseract.image_to_string(img, lang='ron')
        

        if(False): #@TODO
            print text
            engine.say(text.decode('utf-8'))


            engine.iterate()

            #cv2.waitKey(0)

            #engine.runAndWait()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



#endloop

engine.endLoop()
cap.release()
cv2.destroyAllWindows()






