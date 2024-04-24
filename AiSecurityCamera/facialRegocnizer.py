import cv2
import os
import numpy as np
from picamera2 import Picamera2

# Parametere
id = 0
font = cv2.FONT_HERSHEY_COMPLEX
height = 1
boxColor = (0, 255, 0)       # BGR - GRØNN
nameColor = (0, 255, 255)    # BGR - GUL
confColor = (255, 0, 255)    # BGR - MAGENTA

# Laster inn det forhåndstrente ansiktsgjenkjenningsmodellen og ansiktsdetektor
ansikt_gjenkjenner = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
gjenkjenner = cv2.face.LBPHFaceRecognizer_create()
gjenkjenner.read('trainer/trainer_prog.yml')

# Navn relatert til id
navn = ['Ingen', 'zahra']

# Opprett et instans av Picamera2-objektet for å få tilgang til kameraet
cam = Picamera2()

## Initialiser og start sanntids videofangst
# Sett oppløsningen til kameraet
cam.preview_configuration.main.size = (1280, 720)
cam.preview_configuration.main.format = "RGB888"
cam.preview_configuration.controls.FrameRate = 30
cam.preview_configuration.align()
cam.configure("preview")
cam.start()

while True:
    # Fang et bilde fra kameraet
    frame = cam.capture_array()

    # Konverter bilde fra BGR til gråskala
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Oppdag ansikter i gråskala bildet
    ansikt = ansikt_gjenkjenner.detectMultiScale(
            frameGray,      # Gråskala bilde for å oppdage ansikter
            scaleFactor=1.1,# Hvor mye bildestørrelsen reduseres ved hver bilde skala - 10% reduksjon
            minNeighbors=5, # Hvor mange naboer hver kandidat rektangel skal ha for å beholde den
            minSize=(150, 150)# Minimum mulig objektstørrelse. Objekter mindre enn denne størrelsen ignoreres.
            )
    
    for(x, y, w, h) in ansikt:
        namepos = (x + 5, y - 5)  # Posisjon for navn og tillit
        confpos = (x + 5, y + h - 5)  # Posisjon for tillit
        
        # Opprett en boks rundt det oppdagede ansiktet
        cv2.rectangle(frame, (x, y), (x + w, y + h), boxColor, 3)

        # Gjenkjenne ansiktet og hente ID og tillit
        id,  noyaktighet= gjenkjenner.predict(frameGray[y:y+h, x:x+w])
        
        # Hvis tilliten er mindre enn 100, anses det som en perfekt kamp
        if noyaktighet < 50:
            id = navn[id]
            noyaktighet = f"{100 - noyaktighet:.0f}%"
        else:
            id = "ukjent"
            

           
        # Vis navn og tillit til personen som gjenkjennes
        cv2.putText(frame, str(id), namepos, font, height, nameColor, 2)
        cv2.putText(frame, str(noyaktighet), confpos, font, height, confColor, 1)

    # Vis sanntidsfangstresultatet til brukeren
    cv2.imshow('Raspberry Pi AI Security Kamera', frame)

    # Vent i 30 millisekunder på en tastatur hendelse og avslutt hvis 'ESC' eller 'q' trykkes
    key = cv2.waitKey(100) & 0xff
    if key == 27:  # ESCAPE tast
        break
    elif key == 113:  # q tast
        break

# Stopp kameraet og lukk alle vinduer
print("\n Programmet er avsluttet")
cam.stop()
cv2.destroyAllWindows()
