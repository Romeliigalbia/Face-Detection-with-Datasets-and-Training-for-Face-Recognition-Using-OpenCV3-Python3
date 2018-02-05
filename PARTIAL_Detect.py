# -*- coding: cp1252 -*-

#Import of OPENCV 3 Library
import cv2
import pymysql

#Path of Database Directory
path='dataset'

#Show Video Stream 
def show_webcam(mirror=False):
    fontface = cv2.FONT_HERSHEY_COMPLEX
    size=1
    
    #Capture Video Format
    cap = cv2.VideoCapture(1)
    
    #Optional for Opening Camera
    cap.open(1)
    
    #Count Per Frame
    a=0
    
    #Haar Clasifier of OpenCV for Front Face Detection
    faceDetect=cv2.CascadeClassifier('clasifier/haarcascade_frontalface_default.xml')
    
     #Haar Clasifier of OpenCV for Eye Detection
    eyeDetect= cv2.CascadeClassifier('clasifier/haarcascade_eye.xml')

    #Looping Carema 
    while True:
        
        #counting 
        a = a+1
        
        #Read Camera
        check, img = cap.read()
        
        #Convert Camera to Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        #Detects objects of different sizes in the input image. The detected objects are returned as a list of rectangles.
        faces=faceDetect.detectMultiScale(gray,1.3,5,minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)
        
        #for every detected faces, it will create rectangle shape to determine a visible face 
        for f in faces:
            (x, y, w, h) = [v * size for v in f]
            roi_gray = gray[y:y+h, x:x+w]
            eyes =  eyeDetect.detectMultiScale(roi_gray)
            for e in eyes:
                
                
            #Draw Rectangle when face is detected 
#            cv2.rectangle(img, (x,y),(x+w,y+h),(125,255,125),2)
            
            #Save Detected Face in Database Directory
                cv2.putText(img,str("FACE DETECTED"),(x,y-5), fontface,0.6,(0,255,255),2)
                
        #To display Image or Video in a window
        cv2.imshow('frame', img)
        
        #Keyboard binding function
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    
    print(a)
    
    #allow or enable to escape from confinement; set free.
    cap.release()
    #Completely Destroy Running Window/s
    cv2.destroyAllWindows()

def main():
    show_webcam(mirror=True)
    
#'main' is the name of the scope in which top-level code executes. Basically you have two ways of using a Python module: Run it directly as a script, or import it. When a module is run as a script
if __name__=='__main__':
    main()
