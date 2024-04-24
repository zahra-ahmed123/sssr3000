from gpiozero import MotionSensor, DistanceSensor
from picamera2 import Picamera2
from signal import pause
import cv2
import numpy as np
import os

# Initialiser PIR-bevegelsessensor
pir = MotionSensor(4)

# Initialiser kamera
cam = Picamera2()

# Initialiser avstandssensor
sensor = DistanceSensor(echo=17, trigger=22, max_distance=1)

# Parametere for ansiktsgjenkjenning
font = cv2.FONT_HERSHEY_COMPLEX
height = 1
boxColor = (0, 255, 0)       # BGR - Grønn
nameColor = (0, 255, 255)    # BGR - Gul
confColor = (255, 0, 255)    # BGR - Magenta

# Last inn forhåndstrengt ansiktsgjenkjenningmodell og ansiktsgjenkjenner
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer_prog.yml')

# Navn relatert til ID-er
names = ['Ingen', 'zahra']

def utfør_ansiktsgjenkjenning(frame):
    # Konverter bilde fra BGR til gråskala
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Oppdag ansikter i gråskalabilde
    faces = face_cascade.detectMultiScale(
            frameGray,      # Gråskalabilde for å oppdage ansikter
            scaleFactor=1.1,# Hvor mye bildestørrelsen reduseres ved hver bilde skala - 10% reduksjon
            minNeighbors=5, # Hvor mange naboer hver kandidat rektangel skal ha for å beholde den
            minSize=(150, 150)# Minimum mulig objektstørrelse. Objekter mindre enn denne størrelsen ignoreres.
            )
    
    for(x, y, w, h) in faces:
        namepos = (x + 5, y - 5)  # Posisjon for navn og tillit
        confpos = (x + 5, y + h - 5)  # Posisjon for tillit
        
        # Opprett en rektangel rundt det oppdagede ansiktet
        cv2.rectangle(frame, (x, y), (x + w, y + h), boxColor, 3)

        # Gjenkjenne ansiktet og hent ID og tillit
        id,  confidence = recognizer.predict(frameGray[y:y+h, x:x+w])
        
        # Hvis tilliten er mindre enn 100, anses det som en perfekt kamp
        if confidence < 50:
            id = names[id]
            confidence = f"{100 - confidence:.0f}%"
        else:
            id = "Ukjent"

        # Vis navn og tillit til personen som gjenkjennes
        cv2.putText(frame, str(id), namepos, font, height, nameColor, 2)
        cv2.putText(frame, str(confidence), confpos, font, height, confColor, 1)

    return frame

def start_ansiktsgjenkjenning():
    # Start kamera
    cam.start()

    # Ta opp bilder for ansiktsgjenkjenning
    while True:
        # Ta opp bilde
        frame = cam.capture_array()
        
        # Utfør ansiktsgjenkjenning på bildet
        processed_frame = utfør_ansiktsgjenkning(frame)
        
        # Vis resultatet
        cv2.imshow("Ansiktsgjenkjenning", processed_frame)

        # Sjekk om avslutningsbetingelse
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Stopp kamerapresentasjonen
    cam.stop()

    # Lukk OpenCV-vinduet
    cv2.destroyAllWindows()

def bevegelse_detektert():
    print("Bevegelse oppdaget")
    start_ansiktsgjenkjenning()

def avstand_utløst():
    print("Avstandssensor utløst. Venter på bevegelse...")
    pir.wait_for_motion()
    bevegelse_detektert()

# Tildel funksjoner til hendelser
sensor.when_in_range = avstand_utløst

# Start venting på hendelser
pause()
