from picamera2 import Picamera2
from gpiozero import DistanceSensor
import cv2
import numpy as np
import os

# Initialize camera
cam = Picamera2()

# Initialize distance sensor
sensor = DistanceSensor(echo=17, trigger=22, max_distance=1)

# Parametere for facial recognition
font = cv2.FONT_HERSHEY_COMPLEX
height = 1
boxColor = (0, 255, 0)       # BGR - GRØNN
navnColor = (0, 255, 255)    # BGR - GUL
noyaColor = (255, 0, 255)    # BGR - MAGENTA

# Laster inn det forhåndstrente ansiktsgjenkjenningsmodellen og ansiktsdetektor
ansikt_gjenkjenner = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#LBPFactor
gjenkjenner = cv2.face.LBPHFaceRecognizer_create()
#les trente bilder i trainer_prog.xml
gjenkjenner.read('trainer/trainer_prog.yml')

# Navn relatert til id
navn = ['Ingen', 'zahra', 'Najah', 'sairah']

def utfør_ansikts_gjenskjenning(frame):
    # Konverterer bilde fra BGR til gråskala
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Oppdag ansikter i gråskala bildet...
    ansikt = ansikt_gjenkjenner.detectMultiScale(
            frameGray,scaleFactor=1.1, minNeighbors=4, minSize=(150, 150))
            
    for(x, y, w, h) in ansikt:
        navn_posi = (x + 5, y - 5)  # Posisjon for navn og tillit
        noya_posi = (x + 5, y + h - 5)  # Posisjon for tillit
        
        # Opprett en boks rundt det oppdagede ansiktet
        cv2.rectangle(frame, (x, y), (x + w, y + h), boxColor, 3)

        # Gjenkjenne ansiktet og hente ID og tillit
        id,  noyaktighet= gjenkjenner.predict(frameGray[y:y+h, x:x+w])
        
        if (noyaktighet < 50):
            id = navn[id]
            noyaktighet = "  {0}%".format(round(100 - noyaktighet))
        else:
            id = "ukjent"
            noyaktighet = "  {0}%".format(round(100 - noyaktighet))
        # Vis navn og tillit til personen som gjenkjennes
        cv2.putText(frame, str(id), navn_posi, font, height, navnColor, 2)
        cv2.putText(frame, str(noyaktighet), noya_posi, font, height, noyaColor, 1)

    return frame

# Start camera preview
cam.preview_configuration.main.size = (1280, 720)

cam.preview_configuration.main.format = "RGB888"

cam.preview_configuration.controls.FrameRate = 30

cam.preview_configuration.align()

cam.configure("preview")

while True:
    # Wait for motion in range
    print('Waiting for motion in range...')
    sensor.wait_for_in_range()
    print('Motion detected in range!')

    # Start camera
    cam.start()

    # fang bilder for ansiktsgjenskenning
    while sensor.distance < 2:  # Keep checking while motion is within range
        # fanger rammerer 
        frame = cam.capture_array()
                # Perform facial recognition on the frame
        processed_frame = utfør_ansikts_gjenskjenning(frame)
        
        # Convert frame for displaying using OpenCV
  # vis resultat
        cv2.imshow("AI security Camera with Facial Recognition", frame)

        # Check for exit condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Stopper camera  preview
    cam.stop()

    # Close OpenCV window
    cv2.destroyAllWindows()

    # Wait for motion out of range before checking again
    print('Waiting for motion out of range...')
    sensor.wait_for_out_of_range()
    
    print("\n motion out of range")
    
    print("\n Programmet er avsluttet")
