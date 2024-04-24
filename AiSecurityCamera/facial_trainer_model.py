import cv2
import os
import numpy as np

# Bruker LBPH (Local Binary Patterns Histograms) for gjenkjenning 
gjenskjenner = cv2.face.LBPHFaceRecognizer_create()
ansikts_gjennskjenner = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
path = 'dataset'

def getImagesAndLabels(path):
    ansiktSamples = []
    ids = []

    for filnavn in os.listdir(path):
        if filnavn.endswith(".jpg"):
            id = int(filnavn.split(".")[1])
            bilde_path = os.path.join(path, filnavn)
            bilde = cv2.imread(bilde_path, cv2.IMREAD_GRAYSCALE)

            ansikt = ansikts_gjennskjenner.detectMultiScale(bilde)

            for (x, y, w, h) in ansikt:
                ansiktSamples.append(bilde[y:y+h, x:x+w])
                ids.append(id)

    return ansiktSamples, ids

def trainGjenskjenner(ansikt, ids):
    gjenskjenner.train(ansikt, np.array(ids))
    # Opprett 'trainer'-mappen hvis den ikke eksisterer
    if not os.path.exists("trainer"):
        os.makedirs("trainer")
    # Lagre modellen i 'trainer/trainer.yml'
    gjenskjenner.write('trainer/trainer_prog.yml')

if __name__ == "__main__":
    print("\n [INFO] Trener ansikter. Dette vil ta noen sekunder. Vennligst vent ...")
    ansikt, ids = getImagesAndLabels(path)
    trainGjenskjenner(ansikt, ids)
    num_ansikt_trained = len(set(ids))
    print("\n [INFO] {} ansikter trent...".format(num_ansikt_trained))
    print("\n [INFO] Programmet avsluttes")
