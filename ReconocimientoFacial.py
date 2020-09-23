def reconocimientoRostro():
	import cv2
	import time
	import os
	import pdb 
	from datetime import datetime

	# Path donde guardo las imagenes
	dataPath = r'C:\Users\feder\Documents\server\Reconocimiento-Facial-Python\Data'
	registroPath = r'C:\Users\feder\Documents\server\Reconocimiento-Facial-Python\Registros'

	# Array con los nombres de las carpetas
	imagePaths = os.listdir(dataPath)

	# Imprimo las carpetas
	print('imagePaths=',imagePaths)
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()

	# Variable que utilizo para saber cuando retornar
	ficho = 0

	# Leyendo el modelo
	face_recognizer.read('modeloLBPHFace.xml')

	# Nombre de la ventana
	cv2.namedWindow('Reconocimiento',cv2.WINDOW_NORMAL)

	# Opciones para leer rotros: Camara o Video.
	cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
	#cap = cv2.VideoCapture('Video.mp4')

	faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

	while True:
		print(ficho)
		ret,frame = cap.read()
		if frame is not None:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			auxFrame = gray.copy()
			faces = faceClassif.detectMultiScale(gray,1.3,5)
			for (x,y,w,h) in faces:
				rostro = auxFrame[y:y+h,x:x+w]
				rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
				result = face_recognizer.predict(rostro)
				cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)

				# LBPHFace
				if result[1] < 80:
					cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
					ficho += 1
					if ficho == 5:
						dt_string = datetime.now().replace(microsecond=0).isoformat()
						dt_path = dt_string.replace(':','-')
						
						cap.release()
						cv2.destroyAllWindows()
						
						personPath = registroPath + '/' + '{}'.format(imagePaths[result[0]])
						person = '{}'.format(imagePaths[result[0]])

						if not os.path.exists(personPath):
							os.makedirs(personPath)	
						
						cv2.imwrite('Registros/'+person+'/'+person+'_'+dt_path+'.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
						ruta_imagen = 'Registros/'+person+'/'+person+'_'+dt_path+'.jpg'
						
						return {'status': 'OK', 'code': '200','body': person, 'time': {}, 'ruta_imagen': ruta_imagen, 'date': dt_path}
				else:
					cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
					ficho -= 1
					if ficho < -5:
						cap.release()
						cv2.destroyAllWindows()	
						return {'status': 'ERROR', 'code': '404'}

			cv2.imshow('Reconocimiento',frame)	
		if cv2.waitKey(1) & 0xFF == ord('q'):
			return {'status': 'FORCE END', 'code': '404'}

	cap.release()
	cv2.destroyAllWindows()	
	
	