# -*- coding: utf-8 -*-
import cv2
#import os
import pymysql
#from PIL import Image
#import numpy as np

conn = pymysql.connect(host="localhost", user="root", passwd="", db="facerecognition")
myCursor = conn.cursor()

def recognize(mirror=False):
    
    
    faceDetect=cv2.CascadeClassifier('clasifier/lbpcascade_frontalface.xml')
    rec = cv2.face.LBPHFaceRecognizer_create();
    rec.read("recognizer\\trainingData.yml")
    cam = cv2.VideoCapture(1);
    cam.open(1)
    fontface = cv2.FONT_HERSHEY_COMPLEX

    def getProfile(id):
        
        
        cmd=("SELECT * FROM `student` WHERE stud_id="+str(id))
        myCursor.execute(cmd)
        profile=None
        for row in myCursor:
            profile=row
        return profile
    
    count = 0
    while True:
        
        check, img=cam.read()
#        img = cv2.imread('img/Angelina.jpg')
        
        if img == None: 
            raise Exception("could not load image !")
        if mirror: 
            img = cv2.flip(img, 1)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5,minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE);
        for(x,y,w,h) in faces:
            count = count + 1
#            print(count)
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h),(205,0,0),2)
            
            profile=getProfile(id)
            if(conf<150):
                cv2.putText(img,str(profile[1]),(x,y-5), fontface,1,(0,255,255),2)
                    
            else:
                cv2.putText(img,str("Unknown "+str(conf)),(x,y-5), fontface,0.6,(0,255,255),2)
                
        cv2.imshow('Face', img);
        
        if cv2.waitKey(1) & 0xff == ord('q'):
            break;
        
    cam.release()
    cv2.destroyAllWindows()

def main():
    recognize(mirror=True)
    
if __name__ =='__main__':
    main()
    
        
