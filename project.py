import face_recognition
import cv2
import numpy
import shutil
import datetime
import pandas as pd 
import os
import pickle
import sys
def main():
    #Promting user with option to select
    try:
        while True:
            print("1. Start logging in employees \n2. Enter details of a new employee \n3. Calculate employees pay \n4. Exit the program")
            option=int(input("Enter your input: "))
            if option==1:
                recoiz()
            elif option==2:
                ine()
            elif option==3:
                pay_cal()
            elif option==4:
                sys.exit()    
    except ValueError:
        print("Please choose a valid option.")
        main()
def recoiz():
    # Initialize some variables
    login_in_time=datetime.time(8,30,0)
    log_out_time=datetime.time(16,30,0)
    half_time=datetime.time(12,30,0)
    date_today=datetime.date.today()
    try:
        uid_full,uid_half,uid_ab,uid_temp,uid_late=temp_reader()
    except FileNotFoundError:
        pass
    uid_list=['uid_full','uid_half','uid_ab','uid_temp','uid_late']
    df=pd.read_csv('log.csv')
    #creates a new date column if date_today not equal to the last date
    if df.keys()[-1]!=str(date_today):
         df[date_today]=''
         
         df.to_csv('log.csv',index=False)
         uid_full=[]
         uid_temp=[]
         uid_half=[]
         uid_late=[]
         uid_ab=[]
    # to check the full day ,half day or absent 
    while True:
        
        uid,time_rec=reco()
        if time_rec.time()<=login_in_time:
            uid_temp.append(uid)
        elif time_rec.time()>=login_in_time and time_rec.time()<=half_time:
            if uid in uid_temp:
                uid_ab.append(uid)
                uid_temp.remove(uid)
            else:
                uid_late.append(uid)
            
        elif time_rec.time()>=half_time and time_rec.time()<=log_out_time:
            if uid in uid_temp:
                uid_half.append(uid)
                uid_temp.remove(uid)
            if uid in uid_late:
                uid_ab.append(uid)
                uid_late.remove(uid)
        elif time_rec.time()>=log_out_time:
            if uid in uid_temp:
                uid_full.append(uid)
            if uid in uid_late:
                uid_half.append(uid)
        
        break
    #Writing data into csv file 
    data_writer(uid_full,uid_half,uid_ab,date_today)
    #Writing data to temp folder and the list made above for further usage 
    temp_writer(uid_full,uid_half,uid_ab,uid_temp,uid_late)
    
     

def reco():
    
        
        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(3)

        # Load the sample picture and learn how to recognize it.
        path="D:\\vs code\\"
        known_face_encodings = []
        known_face_names = []
        #using loops to irritate over the photos
        for x in os.listdir(path):
                if x.endswith('.jpg'):
                        y = face_recognition.load_image_file(x)
                        z = face_recognition.face_encodings(y)[0]
                        face_uid=x.rstrip(".jpg")
                        # Create arrays of known face encodings and their names
                        known_face_names.append(face_uid)
                        known_face_encodings.append(z)

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Only process every other frame of video to save time
            if process_this_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = numpy.ascontiguousarray(small_frame[:, :, ::-1])
                
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        uid = known_face_names[first_match_index]
                        now=datetime.datetime.now()
                        return uid,now

                

            process_this_frame = not process_this_frame


            

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


def ine():
    #getting some input 
    name=input("Name of the employee: ")
    target = "D:\\vs code\\"
    
    source=input("Enter the location of the employee's photo(.jpg file only): ")
    
    #writing the name to csv and giving a uid to the name 
    df=pd.read_csv('log.csv')
    last_uid=df.iloc[-1]['uid']
    no_uid=int(last_uid.lstrip("uid"))
    
    no_uid = no_uid + 1
    
    new_uid="uid" + str(no_uid)
    target= target + new_uid + ".jpg"
    #copy the file to the project directory
    shutil.copy2(source,target)
    dict={'uid':new_uid,'name':name}
    #saving the data 
    df=df._append(dict,ignore_index = True)
    df.to_csv('log.csv',index=False)



def data_writer(full,half,ab,date):

    df=pd.read_csv('log.csv')
    df = df.astype(str)
    for z in full:
        y=0
        for i in df['uid']:
            if i==z:
                df.loc[y,str(date)]='P'
            else:
                y+=1
    for z in half:
        y=0
        for i in df['uid']:
            if i==z:
                df.loc[y,str(date)]='H'
            else:
                y+=1 
    for z in ab:
        y=0
        for i in df['uid']:
            if i==z:
                df.loc[y,str(date)]='A'
            else:
                y+=1
    df.to_csv('log.csv',index=False)
    df=pd.read_csv('log.csv')
    y=0
    for i in df[str(date)]:
            if i=='n':
                df.loc[y,str(date)]='A'
            else:
                y+=1
    df.to_csv('log.csv',index=False)
     
def pay_cal():
    df=pd.read_csv('log.csv')
    x,y=df.shape
    pay=int(input("Enter daily wage: "))
    # Present (Full day) counting
    z=0
    list_p=[]
    for _ in range(x):
        q=0
        for b in df.loc[z]:
            if b=='P':
                q+=1
        z+=1
        list_p.append(q)
    z=0
    list_h=[]
    for _ in range(x):
        q=0
        for b in df.loc[z]:
            if b=='H':
                q+=1
        z+=1
        list_h.append(q)
    
    name=[]
    fd=[]
    hd=[]
    pa=[]
    for _ in range(x):
        name.append(df.loc[_]['name'])
        fd.append(list_p[_])
        hd.append(list_h[_])
        pa.append(int((list_p[_]+ (list_h[_]*0.5))*pay))
    dict={'Name':name,'Full Days':fd, 'Half Days':hd,'Calculated Pay':pa}
    pay_df=pd.DataFrame(dict)
    print(pay_df)

def temp_writer(full,half,ab,temp,late):
    list=[full,half,ab,temp,late]
    list1=['full','half','ab','temp','late']
    y=0
    for i in list:
        
        x=r"D:\vs code\temp\ "
        z=list1[y]
        path=x + z + ".dat"
        y+=1
    
        with open(path, 'wb') as f:
            pickle.dump(i, f)


def temp_reader():
    list1=['full','half','ab','temp','late']
    full=[]
    half=[]
    ab=[]
    temp=[]
    late=[]
    list=[full,half,ab,temp,late]
    z=0
    x=r"D:\vs code\temp\ "
    for i in list1:
            y= x+i+".dat"
            with open(y, 'rb') as f:
                d=list[z]
                r= pickle.load(f)
                d.extend(r)
            z+=1
                
    return full,half,ab,temp,late

    
if __name__ == "__main__":
    main()
