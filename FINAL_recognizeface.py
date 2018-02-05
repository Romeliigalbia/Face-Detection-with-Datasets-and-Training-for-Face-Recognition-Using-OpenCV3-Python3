# -*- coding: utf-8 -*-
#import datetime
#import os
#from PIL import Image
#import numpy as np
import cv2
import pymysql
from datetime import date
import calendar

my_date = date.today()
daytoday = calendar.day_name[my_date.weekday()]

conn = pymysql.connect(host="localhost", user="root", passwd="", db="facerecognition")
myCursor = conn.cursor()
path = 'datasets'

def recognize(mirror=False):
    
    faceDetect=cv2.CascadeClassifier('clasifier/haarcascade_frontalface_default.xml')
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
  
    x = bytes(",",'utf-8')
    while True:
        check, img=cam.read()
#        img = cv2.imread('img/jason.png')
        if img == None: 
            raise Exception("Could not load video")
        if mirror: 
            img = cv2.flip(img, 1)
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5,minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE);
        for(x,y,w,h) in faces:
            count = count + 1
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            cv2.rectangle(img,(x,y),(x+w,y+h),(205,0,0),2)
            profile=getProfile(id)
            if(conf<180):
                if(profile!=None):
                    cv2.putText(img,str(profile[1]),(x,y-5), fontface,0.6,(0,255,255),2)
                    cmd="SELECT * FROM array_attendance AS a WHERE a.array_stud_id="+str(id)
#                    cmd2="SELECT * FROM attendance AS a JOIN student as s WHERE s.stud_id="+str(id)
                    myCursor.execute(cmd)
                    rowss = myCursor.fetchall()
#                    rowsss = myCursor.fetchall()
                    existdata=0
                    for row in rowss:
                        existdata=1
#                        for rows in rowsss:qq
#                            existdata=1
                    if(existdata==0):
                        cmd="INSERT INTO array_attendance(array_sched_id,array_stud_id,array_attend_status) SELECT s.sched_id, '"+str(profile[0])+"', 'present' From attendance as a JOIN schedule as s JOIN class as c WHERE days=DAYNAME(CURDATE()) AND TIME(CURTIME()<ADDTIME(TIME(start), TIME('00:59:00')))"
                        print("    =PRESENT=     "+str(profile[1]))
                        myCursor.execute(cmd)
                        conn.commit()
                        
                        #INSERT CONDITION: DEPENDS ON THE DAY AND SCHEDULED OF A CLASS AND WHEN THE FACE IS RECOGNIZED IT WILL RECORD THE DATA WHICH INCLUDES HIM/HER AS PRESENT IN THAT CERTAIN DAY AND SCHEDULED CLASS
                        
                    else:
                        print("Already Present" + str(profile[1]))
                        
                        
                else:
                    cv2.putText(img,str("Unknown"),(x,y-5), fontface,0.6,(0,255,255),2)
                
        cv2.imshow('Face', img);
        if cv2.waitKey(1) & 0xff == ord('q'):
            cmd="DELETE FROM array_attendance WHERE NOT EXISTS (SELECT * FROM ( SELECT MIN(array_attendance.array_id) minID FROM array_attendance JOIN schedule GROUP BY array_stud_id HAVING COUNT(*) > 0 )	AS q WHERE minID=array_attendance.array_id)"
            cmd2="INSERT INTO attendance (sched_id, stud_id, attend_status)SELECT aa.array_sched_id, aa.array_stud_id, aa.array_attend_status FROM array_attendance as aa"
            cmd3="TRUNCATE TABLE array_attendance"
            myCursor.execute(cmd)
            myCursor.execute(cmd2)
            myCursor.execute(cmd3)
            conn.commit()
            break
    conn.close()
    cam.release()
    cv2.destroyAllWindows()
    
def main():
    recognize(mirror=True)
    
if __name__ =='__main__':
    main()