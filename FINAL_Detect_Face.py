import os
import cv2
import numpy as np
import pymysql
from PIL import Image

def detectandtrain(mirror=False):
    fontface = cv2.FONT_HERSHEY_COMPLEX
    size=1
    a=0
    db = pymysql.connect("localhost","root","","facerecognition",charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    print ("Connected to Database!!")
    try:
        print("=========================ADD STUDENT=============================")
        id = input('enter student id: ')
        name = input('enter student first name: ')
        last = input('enter student last name: ')
        print("=================================================================")
        cap = cv2.VideoCapture(1)
        cursor = db.cursor()
        cmd = "SELECT * FROM `student` WHERE stud_id="+str(id)
        cursor.execute(cmd)
        rows = cursor.fetchall()
    #    sqlinsert = """
        isRecordExist=0
        for row in rows:
            isRecordExist=1
        if(isRecordExist==1):
            cursor.execute("UPDATE `student` SET `firstname`='"+str(name)+"' ,`lastname`='"+str(last)+"' WHERE `stud_id` ='"+str(id)+"'")
            db.commit()
            print("|")
            print('Student Already Exist!!')
            print("|")
            print("Firstname:"+str(name)) 
            print( "Lastaname:"+str(last))
            print("|")
        else:
            cmd="INSERT INTO `student` (stud_id,firstname,lastname) VALUES ('"+str(id)+"','"+str(name)+"','"+str(last)+"')"
            print("|")
            print("Successfully Inserted New Student")
            print("|")
        cursor.execute(cmd)
        db.commit()
        cap.open(1)
    finally:
        db.close()
    
    faceDetect=cv2.CascadeClassifier('clasifier/haarcascade_frontalface_default.xml')
#    eyeDetect=cv2.CascadeClassifier('haarcascade_eye.xml')
    sampleNum=0
    print("==========================CONFIGURING============================")
    while True:
        a = a+1
        check, img = cap.read()
#        img = cv2.imread('img/robin.png')
        
        height, width = img.shape[:2]
        max_height = 720
        max_width = 1280
        
        # only shrink if img is bigger than required
        if max_height < height or max_width < width:
            # get scaling factor
            scaling_factor = max_height / float(height)
            if max_width/float(width) < scaling_factor:
                scaling_factor = max_width / float(width)
            # resize image
            img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

        if img == None: 
            raise Exception("could not load image !")
        
        if mirror: 
            img = cv2.flip(img, 1)
        
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5,minSize=(100,100), flags=cv2.CASCADE_SCALE_IMAGE);
        
        #Detecting Faces in Frame
        for f in faces:
            (x, y, w, h) = [v * size for v in f]
            
            sampleNum = sampleNum+1
#            roi_gray = gray[y:y+h, x:x+w]
#            eyes =  eyeDetect.detectMultiScale(roi_gray)
#            for e in eyes:
#                (ex, ey, ew, eh) = [v * size for v in e]
                
                
            #Draw Rectangle when face is detected 
            cv2.rectangle(img, (x,y),(x+w,y+h),(125,255,125),1)
            
            #Save Detected Face in Database Directory
            cv2.putText(img,str("FACE DETECTED"),(x,y-5), fontface,0.6,(0,255,255),2)
            cv2.imwrite("datasets/User."+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
            print(sampleNum)
#            crop_img = img[y:y+h, x:x+w]
        
        #To display Image or Video in a window
        cv2.imshow('frame', img)
        
        #Keyboard binding function
        if cv2.waitKey(100) & 0xff == ord('q'):
            break
        
        #End Window when face was detected 12 times
        elif(sampleNum>10):
            
            print("=========================TRAINING================================")
            print("|")
            print("Scan Datasets Complete")
            break
        
    print("|")
    print("Create Dataset for "+ name)
    print("|")
    print(str(sampleNum)+" Datasets Created!")
    print("|")
    cap.release()
    cv2.destroyAllWindows()
    
    
    cascadePath = "clasifier/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    recognizer=cv2.face.LBPHFaceRecognizer_create();
    
    path='datasets'
    def getImagesWithID(path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path) if not f.endswith('.1.jpg')]
        faces=[]
        IDs=[]
        print("Training Faces Please Wait...")
        print("|")
        print("Training will last 3 to 5 minutes... ")
        print("|")
        for imagePath in imagePaths:
            faceImg=Image.open(imagePath).convert('L');
            faceNp=np.array(faceImg,'uint8')
            ID=int(os.path.split(imagePath)[-1].split('.')[1])
            facess = faceCascade.detectMultiScale(faceNp)
            for (x, y, w, h) in facess:
                faces.append(faceNp[y: y + h, x: x + w])
                IDs.append(ID) 
                cv2.waitKey(1)
        return faces, IDs
    faces,Ids=getImagesWithID(path)
    recognizer.train(faces,np.array(Ids))
    recognizer.write('recognizer/trainingData.yml')
    print("=================================================================")
    print("=========================NEXT PHASE==============================")
    print("|")
    print("Training Complete!!")
    print("|")
    print("Ready For Face Recognition")
    print("|")
    print("=================================================================")
    
    
def main():
    detectandtrain(mirror=True)
    
if __name__=='__main__':
    main()
