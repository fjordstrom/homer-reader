import cv2
import numpy as np
import Image
import pytesseract
import pyttsx

import VisionTools as vt
import SurrogateBoxPoints as sbp

voiceRate = 120
camera = 2
focusFramesTime = 10

kernel = np.ones((5,5),np.uint8)

termination_criteria = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )


#init
cap = cv2.VideoCapture(camera)

engine = pyttsx.init()

engine.setProperty('voice', 'romanian')

rate = engine.getProperty('rate')
engine.setProperty('rate', voiceRate)


focus = 0
camTrack = False

windowHistogram = None
originalWindow = None


engine.startLoop(False)

#looop
while True:

	ret, image = cap.read()
	#cv2.imshow('frame',image)
	image = cv2.flip(cv2.transpose(image), 1)

	
	if not camTrack:

		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray,(5,5),0)

		
		blur = cv2.dilate(blur,kernel,iterations = 1)
		#blur = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)

		#cv2.imshow('t2',blur)

		thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)

	   
		#cv2.imshow('t',thresh)

		contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE )


		for contour in contours:
			[x,y,w,h] = cv2.boundingRect(contour)
			# if cv2.contourArea(contour)>5000:
			if(w > 300 and h > 400):
				cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
				
				trackWindow = vt.getRect((x,y),(x+w,y+h))
				if trackWindow[2]>0 and trackWindow[3]>0:
					windowHistogram = vt.getHistByWindow(image, trackWindow)
					
					camTrack = True
					originalWindow = trackWindow


					
					break


	else:
		#HSV
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		#backprojection
		dst = cv2.calcBackProject([hsv], [0], windowHistogram, [0,180], 1)

		#apply meanshift
		ret, trackWindow = cv2.CamShift(dst, trackWindow, termination_criteria)

		focus = focus + 1

		if trackWindow[2] < originalWindow[2]*0.5 or \
			trackWindow[2] > originalWindow[2]*1.5 or \
			trackWindow[3] < originalWindow[3]*0.5 or \
			trackWindow[3] > originalWindow[3]*1.5:
			print("Lost camtrack!")
			camTrack = False


		if trackWindow[0]+trackWindow[2]==0 or trackWindow[1]+trackWindow[3]==0:
			print("Lost camtrack!")
			camTrack = False
		else:
			pts = sbp.boxPoints(ret)
			pts = np.int0(pts)
			cv2.polylines(image, [pts], isClosed=True, color=(255,0,0), thickness=2)

			cent = ret[0]
			sze = ret[1]
			pA = map(int, (cent[0]-sze[0]/2, cent[1]-sze[1]/2))
			pB = map(int, (cent[0]+sze[0]/2, cent[1]+sze[1]/2))
			cv2.rectangle(image, (pA[0], pA[1]), (pB[0], pB[1]), (0, 0, 255), 2)


			if focus > focusFramesTime:
				focus = 0

				img = Image.fromarray(image, 'RGB')
				text = pytesseract.image_to_string(img, lang='ron')
				
				if(text):
					print text
					engine.say(text.decode('utf-8'))


					engine.iterate()


		if not camTrack:
			focus = 0
			engine.stop()


	cv2.imshow('frame',image)
	


	if cv2.waitKey(1) & 0xFF == ord('q'):
		break



#endloop

engine.endLoop()
cap.release()
cv2.destroyAllWindows()






