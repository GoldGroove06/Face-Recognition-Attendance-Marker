# Face-Recognition-Attendance-Marker
 #### Video Demo:  https://youtu.be/mKfLq9JiYfc
Description:
This project utilizes  face recognition algorithms to automate the attendance marking process. By integrating computer vision technology, the system can accurately identify and verify individuals from a live video feed , ensuring a seamless and reliable attendance management solution.

In this project, we employ libraries such as OpenCV for image processing, and machine learning frameworks like dlib and face_recognition for the facial recognition tasks. By combining these powerful tools, the system not only identifies individuals but also maintains an up-to-date attendance log, which can be exported for administrative use.

In the digital age, the efficiency and accuracy of managing attendance in educational institutions and workplaces have become increasingly important. Traditional methods, such as manual roll calls or swipe cards, are often time-consuming and susceptible to errors or fraudulent entries. To address these challenges, my project presents a Python-based Face Recognition Attendance Marker system.

The Face Recognition Attendance Marker stands as a testament to how modern technology can streamline and enhance routine administrative tasks, paving the way for smarter and more efficient workplaces and educational environments.
 
This project has three main function:
1. To record the login and logout time of the employees by capturing the video feed from the camera. The system creates temp files to store the temporary data and once the employee logs out the temp data is written to the csv file.
2. To enter a new employee to the system. This require user to enter the name and the location of the photo the employee. The system saves the name of the employee in the csv file with its unique uid which is assigned automatically by the system. The image is also copied by the system to its directory for using to match faces.
3. The last function calculates the pay of the employee and automatically accounts for full days and half days the pay is calculated accordingly. The system prints the pay in tabular form displaying the name, full days ,half days and its calculated pay.

This project has multiple function:
1. main()- This function prints the option for the user selection and input. It uses try and except to handle all invalid inputs. The main function calls the function according to the user selected input.

2. recoiz()- This function initialize some variables for the usage of the program and also checks the csv file for last date and creates a new column in the csv file.
This function handles the creation of the temp files and compares the temp files at the user log out time and calls data_writer() to write data to csv and calls temp_writer() to write temp data.

3. reco()- this function captures the video feed from webcam . It creates an array of the known faces by using loops to read the .jpg files .The captured frame is then compared to the array of the known faces and returns the known face uid and the time currently.

4. ine()-This function is responsible of saving the new employee name in csv file , giving unique uid and coping the inputted photo location the project folder.

5. data_writer()-This function writes data to csv file by creating a dataframe with pandas .this function gets input of the temp data from recoiz().

6. pay_cal() - This function reads the csv file for the names and the attendance to calculate the pay according the input of the user in tabular form.

7. temp_writer() - This function uses pickle to write the data in list to a .dat file in the temp folder of the project.

8. temp_reader()- This function uses pickle to read the data from .dat file a list .

