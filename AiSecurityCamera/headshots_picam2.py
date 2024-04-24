#importerer nødvendige pakker

import cv2
import os
from picamera2 import Picamera2


# Definer konstantene som et dictionary
constants = {
    "COUNT_LIMIT": 30,
    "POS": (30, 60),
    "FONT": cv2.FONT_HERSHEY_COMPLEX,
    "HEIGHT": 1.5,
    "TEXTCOLOR": (0, 0, 255),
    "BOXCOLOR": (255, 0, 255),
    "WEIGHT": 3  # Dette må være et heltall
}

# Bruker konstantene etter behov
COUNT_LIMIT = constants["COUNT_LIMIT"]
POS = constants["POS"]
FONT = constants["FONT"]
HEIGHT = constants["HEIGHT"]
TEXTCOLOR = constants["TEXTCOLOR"]
BOXCOLOR = constants["BOXCOLOR"]
WEIGHT = constants["WEIGHT"]  # Pass på at WEIGHT er et heltall


#laster inn haarcascade classifier filen for ansiktsgjenskjenning
FACE_DETECTOR = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Bruker input av bruke-Id må være et helt tall
face_id = input('\n----Skriv inn bruker-id og trykk <enter>----')

# Opprett et instans av Picamera2-objektet
cam = Picamera2()
cam.preview_configuration.main.size = (1280, 720)
cam.preview_configuration.main.format = "RGB888"
cam.preview_configuration.controls.FrameRate = 30
cam.preview_configuration.align()
cam.configure("preview")
cam.start() #start forhåndsvisning 

# Hjelpefunksjoner
def capture_faces():
    count = 0 #start å telle fra null
    while True:
        frame = cam.capture_array()# Fang et bilde fra kameraet
        cv2.putText(frame, 'Antall:' + str(int(count)), POS, FONT, HEIGHT, TEXTCOLOR, WEIGHT)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_DETECTOR.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), BOXCOLOR, 3)
            count += 1 #Øk telleren med +1
            
            #lagrer filene i datasette for senere trening av ansiktene

            if not os.path.exists("dataset"):
                os.makedirs("dataset")
            file_path = os.path.join("dataset", f"User.{face_id}.{count}.jpg")
            if os.path.exists(file_path):
                old_file_path = file_path.replace("dataset", "old_dataset")
                os.rename(file_path, old_file_path)
            cv2.imwrite(file_path, frame_gray[y:y + h, x:x + w])

        cv2.imshow('Ansiktsfangst', frame) #viser ansikter med rektangeler rundt
        key = cv2.waitKey(100) & 0xff
        if key == 27 or key == 113 or count >= COUNT_LIMIT: #Avslutter ved å trykke på ESC
            break

    print("\n Programmet er avsluttet")
    cam.stop() #Stopp kamera
    cv2.destroyAllWindows()#lukk alle åpne filer

# Kjør ansiktsfangsten
if __name__ == "__main__":
    capture_faces()
