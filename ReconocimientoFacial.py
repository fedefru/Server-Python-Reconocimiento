import cv2
import time
import os
from datetime import datetime

dataPath = r'C:\Users\feder\Documents\server\Reconocimiento-Facial-Python\Data'


def reconocimientoRostro():
	imagePaths = os.listdir(dataPath)
	print('imagePaths=',imagePaths)
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()
	ficho = 0
	# Leyendo el modelo
	face_recognizer.read('modeloLBPHFace.xml')

	cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
	#cap = cv2.VideoCapture('Video.mp4')

	faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

	while True:
		print(ficho)
		ret,frame = cap.read()
		if ret == False: break
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		auxFrame = gray.copy()
		faces = faceClassif.detectMultiScale(gray,1.3,5)

		for (x,y,w,h) in faces:
			rostro = auxFrame[y:y+h,x:x+w]
			rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
			result = face_recognizer.predict(rostro)
			cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
			
			# LBPHFace
			if result[1] < 65:
				cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
				cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
				ficho += 1
				if ficho == 30:
					now = datetime.now()
					dt_string = now.strftime('%d/%m/%Y %H:%M:%S')
					return {'status': 'OK', 'code': '200','body': '{}'.format(imagePaths[result[0]]), 'time': dt_string}
				
			else:
				cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
				cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
				ficho -= 1
				if ficho < -30:
					return {'status': 'ERROR', 'code': '404'}
			
		cv2.imshow('frame',frame)
		k = cv2.waitKey(1)
		if k == 27:
			break

	cap.release()
	cv2.destroyAllWindows()
	
	