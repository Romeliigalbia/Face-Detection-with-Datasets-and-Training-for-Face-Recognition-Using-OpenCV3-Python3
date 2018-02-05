import cv2, os
import numpy as np
from PIL import Image
#import matplotlib.pyplot as plt
#%matplotlib inline

cascadePath = "clasifier/lbpcascade_frontalface.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
recognizer = cv2.face.LBPHFaceRecognizer_create()
path = "datasets"

def get_images_and_labels(path):
    
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    images = []
    labels = []
    print("Training Please Wait...")
    for image_path in image_paths:
        image_pil = Image.open(image_path).convert('L')
        image = np.array(image_pil, 'uint8')
        nbr = int(os.path.split(image_path)[-1].split(".")[1])
        faces = faceCascade.detectMultiScale(image)
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
            cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
        
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
        exit(0)
    
    print("Training complete")
    print("Ready for face recognition")
    return images, labels
    cv2.destroyAllWindows()

if __name__=='__main__':
    get_images_and_labels(path) 